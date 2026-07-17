import os
import random
import re
import threading
from typing import List
from urllib.parse import urlencode

import requests
from loguru import logger
from moviepy.video.io.VideoFileClip import VideoFileClip

from app.config import config
from app.models.schema import MaterialInfo, VideoAspect, VideoConcatMode
from app.services import image_gen, twelvelabs
from app.utils import utils

# Thread-safe counter for API key rotation
_api_key_counter = 0
_api_key_lock = threading.Lock()


def _get_tls_verify() -> bool:
    # 默认开启 TLS 证书校验，防止素材搜索和下载过程被中间人篡改。
    # 仅在企业代理、自签证书等明确需要的场景下，允许用户通过
    # `config.toml` 显式设置 `tls_verify = false` 临时关闭。
    tls_verify = config.app.get("tls_verify", True)
    if isinstance(tls_verify, str):
        tls_verify = tls_verify.strip().lower() not in ("0", "false", "no", "off")

    if not tls_verify:
        logger.warning(
            "TLS certificate verification is disabled by config.app.tls_verify=false. "
            "Only use this in trusted proxy environments."
        )

    return bool(tls_verify)


def get_api_key(cfg_key: str):
    api_keys = config.app.get(cfg_key)
    if not api_keys:
        raise ValueError(
            f"\n\n##### {cfg_key} is not set #####\n\nPlease set it in the config.toml file: {config.config_file}\n\n"
            f"{utils.to_json(config.app)}"
        )

    # if only one key is provided, return it
    if isinstance(api_keys, str):
        return api_keys

    global _api_key_counter
    with _api_key_lock:
        _api_key_counter += 1
        return api_keys[_api_key_counter % len(api_keys)]


def search_videos_pexels(
    search_term: str,
    minimum_duration: int,
    video_aspect: VideoAspect = VideoAspect.portrait,
) -> List[MaterialInfo]:
    aspect = VideoAspect(video_aspect)
    video_orientation = aspect.name
    video_width, video_height = aspect.to_resolution()
    api_key = get_api_key("pexels_api_keys")
    headers = {
        "Authorization": api_key,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    }
    # Build URL
    params = {"query": search_term, "per_page": 20, "orientation": video_orientation}
    query_url = f"https://api.pexels.com/videos/search?{urlencode(params)}"
    logger.info(f"searching videos: {query_url}, with proxies: {config.proxy}")

    try:
        r = requests.get(
            query_url,
            headers=headers,
            proxies=config.proxy,
            verify=_get_tls_verify(),
            timeout=(30, 60),
        )
        response = r.json()
        video_items = []
        if "videos" not in response:
            logger.error(f"search videos failed: {response}")
            return video_items
        videos = response["videos"]
        # loop through each video in the result
        for v in videos:
            duration = v["duration"]
            # check if video has desired minimum duration
            if duration < minimum_duration:
                continue
            video_files = v["video_files"]
            # loop through each url to determine the best quality
            for video in video_files:
                w = int(video["width"])
                h = int(video["height"])
                if w == video_width and h == video_height:
                    item = MaterialInfo()
                    item.provider = "pexels"
                    item.url = video["link"]
                    item.duration = duration
                    item.width = w
                    item.height = h
                    item.tags = v.get("url", "").rstrip("/").split("/")[-1].replace("-", " ") if v.get("url") else ""
                    video_items.append(item)
                    break
        return video_items
    except Exception as e:
        logger.error(f"search videos failed: {str(e)}")

    return []


def search_videos_pixabay(
    search_term: str,
    minimum_duration: int,
    video_aspect: VideoAspect = VideoAspect.portrait,
) -> List[MaterialInfo]:
    aspect = VideoAspect(video_aspect)

    video_width, video_height = aspect.to_resolution()

    api_key = get_api_key("pixabay_api_keys")
    # Build URL
    params = {
        "q": search_term,
        "video_type": "all",  # Accepted values: "all", "film", "animation"
        "per_page": 50,
        "key": api_key,
    }
    query_url = f"https://pixabay.com/api/videos/?{urlencode(params)}"
    logger.info(f"searching videos: {query_url}, with proxies: {config.proxy}")

    try:
        r = requests.get(
            query_url, proxies=config.proxy, verify=_get_tls_verify(), timeout=(30, 60)
        )
        response = r.json()
        video_items = []
        if "hits" not in response:
            logger.error(f"search videos failed: {response}")
            return video_items
        videos = response["hits"]
        # loop through each video in the result
        for v in videos:
            duration = v["duration"]
            # check if video has desired minimum duration
            if duration < minimum_duration:
                continue
            video_files = v["videos"]
            # loop through each url to determine the best quality
            for video_type in video_files:
                video = video_files[video_type]
                w = int(video["width"])
                h = int(video.get("height", 0))
                if w < video_width or h <= 0:
                    continue
                clip_ratio = w / h
                target_ratio = video_width / video_height
                if abs(clip_ratio - target_ratio) / max(target_ratio, 0.01) > 0.15:
                    logger.debug(f"  pixabay: skipping clip with ratio {clip_ratio:.3f} (target {target_ratio:.3f})")
                    continue
                item = MaterialInfo()
                item.provider = "pixabay"
                item.url = video["url"]
                item.duration = duration
                item.width = w
                item.height = h
                item.tags = v.get("tags", "")
                item.description = v.get("pageURL", "").rstrip("/").split("/")[-1].replace("-", " ") if v.get("pageURL") else v.get("tags", "")
                video_items.append(item)
                break
        return video_items
    except Exception as e:
        logger.error(f"search videos failed: {str(e)}")

    return []


def search_videos_comfyui(
    search_term: str,
    minimum_duration: int,
    video_aspect: VideoAspect = VideoAspect.portrait,
) -> List[MaterialInfo]:
    """
    ComfyUI local video-generation provider.

    Talks to a minimal OpenAPI-style search endpoint exposed by your own
    ComfyUI bridge (or any local generation server). The bridge is responsible
    for queueing a generation workflow, waiting for completion, and serving the
    rendered clip over HTTP. This function only performs the search step and
    returns MaterialInfo items whose ``url`` points back to the bridge.

    Expected bridge contract (single endpoint, GET):

        GET <base_url>/search?query=<term>&orientation=<orientación>&per_page=20

        200 OK
        Content-Type: application/json
        {
          "videos": [
            {
              "duration": <int, seconds, >= minimum_duration>,
              "url": "<absolute http(s) URL that save_video can GET and download>",
              "width": <int>,   # optional, used only for aspect matching
              "height": <int>
            },
            ...
          ]
        }

    The bridge may pre-generate clips (so the search returns instantly and the
    url is a static file) or generate them on demand (the url blocks until the
    clip is ready). Either model works; save_video treats the url as an opaque
    downloadable resource.

    Configuration in config.toml:

        [comfyui]
        base_url = "http://127.0.0.1:8188"
        api_key = ""                 # optional, sent as Authorization: Bearer
        timeout = 600                # seconds for the search request itself
        clips_per_term = 20           # how many results to ask for per keyword

    A minimal bridge can be implemented as a small FastAPI service that maps
    each query to a ComfyUI workflow (e.g. Wan 2.1, AnimateDiff, SVD) and caches
    clips on disk under a static file server.
    """
    comfy = config.comfyui
    base_url = str(comfy.get("base_url", "") or "").strip().rstrip("/")
    if not base_url:
        logger.error("ComfyUI base_url is not set, skip video search")
        return []

    api_key = str(comfy.get("api_key", "") or "").strip()
    timeout = int(comfy.get("timeout", 600) or 600)
    per_page = int(comfy.get("clips_per_term", 20) or 20)

    aspect = VideoAspect(video_aspect)
    params = {
        "query": search_term,
        "orientation": aspect.name,
        "per_page": per_page,
    }
    query_url = f"{base_url}/search?{urlencode(params)}"
    headers = {"User-Agent": "MoneyPrinterTurbo/1.0"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    logger.info(f"searching videos on ComfyUI: {query_url}, with proxies: {config.proxy}")

    try:
        r = requests.get(
            query_url,
            headers=headers,
            proxies=config.proxy,
            verify=_get_tls_verify(),
            timeout=(30, timeout),
        )
        response = r.json()
        video_items: List[MaterialInfo] = []
        if not isinstance(response, dict) or "videos" not in response:
            logger.error(f"ComfyUI search videos failed: {response}")
            return video_items

        endpoint_host = base_url.split("/", 3)[2] if "/" in base_url else base_url
        for v in response["videos"]:
            try:
                duration = int(v.get("duration") or 0)
            except (TypeError, ValueError):
                continue
            if duration < minimum_duration:
                continue
            url = str(v.get("url") or "").strip()
            if not url:
                continue
            # Allow relative URLs (served from the bridge) by resolving them
            # against the configured base_url. Absolute http(s) URLs are kept
            # as-is so the bridge can redirect to a CDN or separate file host.
            if not url.startswith(("http://", "https://")):
                url = f"{base_url.rstrip('/')}/{url.lstrip('/')}"
                # Basic guard against an authority smuggling via query string.
                if url.split("/", 3)[2] != endpoint_host:
                    logger.warning(f"skip ComfyUI clip with unexpected host: {url}")
                    continue
            item = MaterialInfo()
            item.provider = "comfyui"
            item.url = url
            item.duration = duration
            video_items.append(item)
        return video_items
    except Exception as e:
        logger.error(f"ComfyUI search videos failed: {str(e)}")

    return []


def search_videos_coverr(
    search_term: str,
    minimum_duration: int,
    video_aspect: VideoAspect = VideoAspect.portrait,
) -> List[MaterialInfo]:
    """
    Coverr (https://coverr.co) - free HD/4K stock videos,
    subject to Coverr license terms (https://coverr.co/license).

    Coverr API notes (based on official docs at api.coverr.co/docs/):
      - 鉴权: Authorization: Bearer <api_key>
      - 搜索端点: GET /videos?query=...,响应结构 {"hits": [...], ...}
      - 加 ?urls=true 在搜索响应里直接返回 mp4 直链
      - URL 是 signed JWT(绑定 API key,无过期时间)
      - Coverr 库以 16:9 横屏为主,9:16 portrait 占比极低(约 1%)
        因此本函数不做 aspect_ratio 过滤,由下游 video.py 的
        resize + letterbox 逻辑统一处理
      - duration 字段同时存在 number 和 string 两种形态,本函数都接受

    本函数使用 urls.mp4_download 字段作为下载地址 —— 按 Coverr 官方文档
    (https://api.coverr.co/docs/videos/#download-a-video) 的说法,
    GET 这个 URL 本身就被 Coverr 当作一次合法的 download 事件计入统计,
    无需再调用 PATCH /videos/:id/stats/downloads。
    """
    api_key = get_api_key("coverr_api_keys")
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {
        "query": search_term,
        "page_size": 20,
        "urls": "true",
        "sort": "popular",
    }
    query_url = f"https://api.coverr.co/videos?{urlencode(params)}"
    logger.info(f"searching videos: {query_url}, with proxies: {config.proxy}")

    try:
        r = requests.get(
            query_url,
            headers=headers,
            proxies=config.proxy,
            verify=_get_tls_verify(),
            timeout=(30, 60),
        )
        response = r.json()
        video_items: List[MaterialInfo] = []

        if not isinstance(response, dict) or "hits" not in response:
            logger.error(f"search videos failed: {response}")
            return video_items

        for v in response["hits"]:
            # duration 在不同响应里可能是 number(11.625) 或 string("10.500000")
            try:
                duration = int(float(v.get("duration") or 0))
            except (TypeError, ValueError):
                continue
            if duration < minimum_duration:
                continue

            video_id = v.get("id")
            mp4_download_url = (v.get("urls") or {}).get("mp4_download")
            if not video_id or not mp4_download_url:
                continue

            width = int(v.get("width", 0) or 0)
            height = int(v.get("height", 0) or 0)
            if width > 0 and height > 0:
                clip_ratio = width / height
                target_ratio = video_width / video_height
                if abs(clip_ratio - target_ratio) / max(target_ratio, 0.01) > 0.15:
                    logger.debug(f"  coverr: skipping clip with ratio {clip_ratio:.3f} (target {target_ratio:.3f})")
                    continue

            item = MaterialInfo()
            item.provider = "coverr"
            item.url = mp4_download_url
            item.duration = duration
            item.width = width
            item.height = height
            item.tags = ", ".join(v.get("tags", []) or []) if isinstance(v.get("tags"), list) else str(v.get("tags", ""))
            item.description = v.get("description", "") or v.get("name", "") or ""
            video_items.append(item)
        return video_items
    except Exception as e:
        logger.error(f"search videos failed: {str(e)}")

    return []


def _score_clip_quality(
    item: MaterialInfo,
    target_width: int,
    target_height: int,
) -> float:
    """
    Score a video clip by resolution and aspect-ratio match.

    Higher score = better fit for the final video.
    Factors:
      - Total pixel count (prefer higher resolution)
      - Aspect ratio proximity to target (prefer less letterboxing)
    Combined as a 0-100 score for sorting.
    """
    score = 50.0  # baseline

    if target_width and target_height:
        target_ratio = target_width / target_height
        if item.width and item.height and item.width > 0 and item.height > 0:
            clip_ratio = item.width / item.height
            ratio_diff = abs(clip_ratio - target_ratio)
            ratio_score = max(0, 30 * (1 - min(ratio_diff / 2.0, 1.0)))
            score += ratio_score

            pixels = item.width * item.height
            target_pixels = target_width * target_height
            pixel_ratio = min(pixels / max(target_pixels, 1), 2.0)
            res_score = 20 * min(pixel_ratio, 1.0)
            score += res_score

    score += min(item.duration / 10.0, 10.0)

    return score


_LOW_INFORMATION_WORDS = frozenset({
    "stock", "footage", "video", "videos", "background", "royalty", "free",
    "hd", "4k", "motion", "loop", "animation", "template", "after", "effects",
    "download", "clip", "clips", "media", "file", "files", "pro", "premium",
    "videvo", "videezy", "mixkit", "coverr", "pexels", "pixabay",
    "footage", "videohive", "shutterstock", "getty",
})


def _calculate_relevance_score(item: MaterialInfo, search_term: str) -> float:
    """
    Score a clip by how relevant its metadata is to the search term.

    Uses keyword overlap between the search term and clip tags/description.
    Penalises clips whose metadata consists mostly of generic/low-information
    words (e.g. "stock", "background", "4k") that don't describe actual content.
    Returns 0-100 score.
    """
    if not search_term:
        return 0.0

    term_words = set(search_term.lower().split())
    if not term_words:
        return 0.0

    metadata_text = f"{item.tags} {item.description}".lower()
    if not metadata_text.strip():
        return 0.0

    matches = sum(1 for word in term_words if word in metadata_text)
    coverage = matches / len(term_words)
    score = coverage * 100.0

    metadata_words = set(metadata_text.split())
    content_words = metadata_words - _LOW_INFORMATION_WORDS
    if len(metadata_words) > 0:
        info_ratio = len(content_words) / len(metadata_words)
        if info_ratio < 0.3:
            score *= 0.5

    return min(score, 100.0)


def _is_clip_relevant(item: MaterialInfo, search_term: str, min_relevance: float = 0.4) -> bool:
    """
    Check if a clip's metadata is at least minimally relevant to the search term.

    Uses word-boundary keyword overlap. Clips without tags/description are rejected
    because we cannot verify their relevance to the topic.
    """
    if not item.tags and not item.description:
        return False
    if not search_term:
        return False

    term_words = search_term.lower().split()
    metadata_text = f"{item.tags} {item.description}".lower()
    if not metadata_text.strip():
        return False

    matches = 0
    for word in term_words:
        if re.search(rf"\b{re.escape(word)}\b", metadata_text):
            matches += 1
    score = matches / len(term_words)
    return score >= min_relevance


def _verify_clip_with_twelvelabs(item: MaterialInfo, search_term: str) -> bool:
    """
    Verify clip relevance using TwelveLabs Pegasus (opt-in via API key).

    Returns True if:
      - TwelveLabs is not configured (graceful degradation)
      - The model confirms the clip matches the search term
    Returns False if the model indicates the clip is not relevant.
    """
    if not twelvelabs.is_enabled():
        return True
    if not item.url:
        return True

    try:
        prompt = (
            f"Does this video clip match the description '{search_term}'? "
            f"Answer only 'yes' or 'no'."
        )
        result = twelvelabs.analyze_clip(video_url=item.url, prompt=prompt)
        if result is None:
            return True
        is_relevant = result.strip().lower().startswith("yes")
        if not is_relevant:
            logger.warning(
                f"TwelveLabs rejected clip {item.url} for term '{search_term}': {result[:100]}"
            )
        return is_relevant
    except Exception as e:
        logger.warning(f"TwelveLabs verification failed for {item.url}: {e}")
        return True


def download_videos_by_paragraphs(
    task_id: str,
    paragraph_terms: List[List[str]],
    source: str = "auto",
    video_aspect: VideoAspect = VideoAspect.portrait,
    audio_duration: float = 0.0,
    max_clip_duration: int = 5,
    paragraph_audio_durations: List[float] | None = None,
    use_comfyui_fallback: bool = False,
) -> List[str]:
    """
    Download video clips for each script paragraph independently.

    Each paragraph gets its own time budget and search terms. This ensures
    that the visuals change with the narration topic, not randomly.

    Returns a flat list of video paths in paragraph order: [p1_clip1, p1_clip2, p2_clip1, ...]
    """
    aspect_enum = VideoAspect(video_aspect) if not isinstance(video_aspect, VideoAspect) else video_aspect
    target_width, target_height = aspect_enum.to_resolution()
    material_directory = config.app.get("material_directory", "").strip()
    if material_directory == "task":
        material_directory = utils.task_dir(task_id)
    elif material_directory and not os.path.isdir(material_directory):
        material_directory = ""
    if not material_directory:
        material_directory = utils.storage_dir("cache_videos")
    os.makedirs(material_directory, exist_ok=True)

    if paragraph_audio_durations is None:
        num_paragraphs = max(len(paragraph_terms), 1)
        per_para_duration = audio_duration / num_paragraphs
        paragraph_audio_durations = [per_para_duration] * len(paragraph_terms)

    search_fn = search_videos_auto
    if source == "pexels":
        search_fn = search_videos_pexels
    elif source == "pixabay":
        search_fn = search_videos_pixabay
    elif source == "coverr":
        search_fn = search_videos_coverr
    elif source == "comfyui":
        search_fn = search_videos_comfyui

    all_video_paths: List[str] = []
    total_paragraphs = len(paragraph_terms)

    for para_idx, terms in enumerate(paragraph_terms):
        if not terms:
            logger.warning(f"paragraph {para_idx + 1} has no search terms, skipping")
            continue

        para_budget = paragraph_audio_durations[para_idx]
        logger.info(
            f"paragraph {para_idx + 1}/{total_paragraphs}: "
            f"budget={para_budget:.1f}s, terms={terms}"
        )

        para_downloaded: List[str] = []
        para_duration = 0.0
        seen_urls: set = set()

        term_pairs = _normalize_search_terms(terms)

        for normalized_term, original_term in term_pairs:
            if para_duration >= para_budget:
                break

            try:
                items = search_fn(
                    search_term=normalized_term,
                    minimum_duration=max_clip_duration,
                    video_aspect=video_aspect,
                )
            except Exception as e:
                logger.warning(f"search failed for '{normalized_term}': {e}")
                continue

            scored = []
            for item in items:
                if item.url in seen_urls:
                    continue
                if not _is_clip_relevant(item, original_term):
                    continue
                seen_urls.add(item.url)
                score = _score_clip_quality(item, target_width, target_height)
                scored.append((score, item))

            scored.sort(key=lambda x: x[0], reverse=True)

            for score, item in scored:
                if para_duration >= para_budget:
                    break
                if not _verify_clip_with_twelvelabs(item, original_term):
                    logger.debug(f"  skipping clip (TwelveLabs rejected): {item.url}")
                    continue
                try:
                    saved = save_video(video_url=item.url, save_dir=material_directory)
                    if saved:
                        para_downloaded.append(saved)
                        para_duration += min(max_clip_duration, item.duration)
                        logger.debug(
                            f"  para {para_idx + 1}: added clip "
                            f"({para_duration:.1f}/{para_budget:.1f}s)"
                        )
                except Exception as e:
                    logger.warning(f"failed to download '{original_term}' clip: {e}")

        if para_duration < para_budget * 0.5 and use_comfyui_fallback:
            logger.info(
                f"paragraph {para_idx + 1}: only {para_duration:.1f}s of "
                f"{para_budget:.1f}s, trying ComfyUI fallback"
            )
            for pair in term_pairs[:2]:
                if para_duration >= para_budget:
                    break
                term = pair[0]
                try:
                    generated = generate_video_comfyui(
                        prompt=term,
                        video_aspect=video_aspect,
                        duration=max_clip_duration * 2,
                    )
                    if generated:
                        saved = save_video(video_url=generated.url, save_dir=material_directory)
                        if saved:
                            para_downloaded.append(saved)
                            para_duration += min(max_clip_duration, generated.duration)
                except Exception as e:
                    logger.warning(f"ComfyUI fallback failed for '{term}': {e}")

        logger.info(
            f"paragraph {para_idx + 1}: downloaded {len(para_downloaded)} clips "
            f"({para_duration:.1f}s / {para_budget:.1f}s budget)"
        )
        all_video_paths.extend(para_downloaded)

    logger.success(
        f"downloaded {len(all_video_paths)} total clips across "
        f"{total_paragraphs} paragraphs"
    )

    all_terms = [t for terms in paragraph_terms for t in terms]
    ai_paths = image_gen.generate_ai_clips(
        prompts=all_terms,
        save_dir=material_directory,
        video_aspect=video_aspect,
        clip_duration=max_clip_duration,
        max_clips=config.app.get("ai_image_clips_count", 2),
    )
    if ai_paths:
        all_video_paths = image_gen.interleave_clips(
            stock_paths=all_video_paths,
            ai_paths=ai_paths,
            every_n=config.app.get("ai_clip_interleave_every", 4),
        )

    return all_video_paths


def _normalize_search_terms(search_terms: List[str]) -> List[tuple[str, str]]:
    """
    Expand short/generic search terms to improve stock API results.

    Short queries (1 word) often return poor results. This adds a visual
    modifier to help the API return usable footage.

    Returns list of (normalized_term, original_term) pairs so callers can
    use the original term for relevance checking.
    """
    visual_modifiers = ["footage", "video", "scene"]
    result: list[tuple[str, str]] = []
    for term in search_terms:
        original = term.strip()
        normalized = original
        word_count = len(normalized.split())
        if word_count <= 2:
            has_modifier = any(m in normalized.lower() for m in visual_modifiers)
            if not has_modifier:
                normalized = f"{normalized} stock video footage"
        result.append((normalized, original))
    return result


def search_videos_auto(
    search_term: str,
    minimum_duration: int,
    video_aspect: VideoAspect = VideoAspect.portrait,
) -> List[MaterialInfo]:
    """
    Search ALL configured providers simultaneously and return merged,
    deduplicated, quality-scored results.

    This gives the widest pool of clips. Each provider is tried in order;
    failures in one provider don't affect others.
    """
    aspect = VideoAspect(video_aspect)
    target_width, target_height = aspect.to_resolution()
    all_items: List[MaterialInfo] = []
    seen_urls: set = set()

    providers = []

    pexels_keys = config.app.get("pexels_api_keys")
    if pexels_keys:
        providers.append(("pexels", search_videos_pexels))

    pixabay_keys = config.app.get("pixabay_api_keys")
    if pixabay_keys:
        providers.append(("pixabay", search_videos_pixabay))

    coverr_keys = config.app.get("coverr_api_keys")
    if coverr_keys:
        providers.append(("coverr", search_videos_coverr))

    if not providers:
        logger.error("no video providers configured for auto mode (need at least one API key)")
        return []

    for provider_name, search_fn in providers:
        try:
            items = search_fn(
                search_term=search_term,
                minimum_duration=minimum_duration,
                video_aspect=video_aspect,
            )
            for item in items:
                if item.url and item.url not in seen_urls:
                    seen_urls.add(item.url)
                    q_score = _score_clip_quality(item, target_width, target_height)
                    r_score = _calculate_relevance_score(item, search_term)
                    item.tags = f"{item.tags} _quality_{q_score:.0f}_relevance_{r_score:.0f}"
                    all_items.append(item)
            logger.info(
                f"auto provider '{provider_name}' returned {len(items)} items "
                f"({len([i for i in items if i.url not in seen_urls])} new)"
            )
        except Exception as e:
            logger.warning(f"auto provider '{provider_name}' failed: {e}")

    all_items.sort(
        key=lambda x: (
            float(x.tags.split("_quality_")[1].split("_")[0]) if "_quality_" in x.tags else 0
        ) * 0.5
        + (
            float(x.tags.split("_relevance_")[1].split("_")[0]) if "_relevance_" in x.tags else 0
        ) * 0.5,
        reverse=True,
    )

    logger.info(
        f"auto search for '{search_term}': {len(all_items)} total "
        f"unique clips across {len(providers)} providers"
    )
    return all_items


def generate_video_comfyui(
    prompt: str,
    video_aspect: VideoAspect = VideoAspect.portrait,
    duration: int = 8,
) -> MaterialInfo | None:
    """
    Generate a custom video clip via ComfyUI bridge.

    Calls a `/generate` endpoint on the ComfyUI bridge (separate from `/search`).
    The bridge is expected to:
      1. Queue a ComfyUI workflow (e.g. Wan 2.1, AnimateDiff, SVD)
      2. Wait for completion
      3. Return the rendered clip URL

    POST /generate
    {
      "prompt": "...",
      "orientation": "portrait",
      "duration": 8
    }

    200 OK
    {
      "url": "http://bridge/clips/generated_123.mp4",
      "duration": 8,
      "width": 1080,
      "height": 1920
    }

    Returns MaterialInfo on success, None on failure or when not configured.
    """
    comfy = config.comfyui
    base_url = str(comfy.get("base_url", "") or "").strip().rstrip("/")
    if not base_url:
        logger.info("ComfyUI base_url not set, skip generation")
        return None

    api_key = str(comfy.get("api_key", "") or "").strip()
    timeout = int(comfy.get("timeout", 600) or 600)
    aspect = VideoAspect(video_aspect)

    headers = {"User-Agent": "MoneyPrinterTurbo/1.0"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "prompt": prompt,
        "orientation": aspect.name,
        "duration": max(4, min(duration, 30)),
    }
    generate_url = f"{base_url}/generate"

    logger.info(f"generating video via ComfyUI: {generate_url}, prompt={prompt}")
    try:
        r = requests.post(
            generate_url,
            json=payload,
            headers=headers,
            proxies=config.proxy,
            verify=_get_tls_verify(),
            timeout=(30, timeout),
        )
        if r.status_code != 200:
            logger.warning(f"ComfyUI generation failed: {r.status_code} {r.text[:200]}")
            return None

        resp = r.json()
        video_url = str(resp.get("url") or "").strip()
        if not video_url:
            logger.warning("ComfyUI generation returned no URL")
            return None

        if not video_url.startswith(("http://", "https://")):
            endpoint_host = base_url.split("/", 3)[2] if "/" in base_url else base_url
            video_url = f"{base_url.rstrip('/')}/{video_url.lstrip('/')}"
            if video_url.split("/", 3)[2] != endpoint_host:
                logger.warning(f"skip ComfyUI generated clip with unexpected host: {video_url}")
                return None

        item = MaterialInfo()
        item.provider = "comfyui_generated"
        item.url = video_url
        item.duration = int(resp.get("duration", duration))
        item.width = int(resp.get("width", 0) or 0)
        item.height = int(resp.get("height", 0) or 0)
        logger.success(f"ComfyUI generated clip: {video_url}")
        return item
    except requests.Timeout:
        logger.warning(f"ComfyUI generation timed out after {timeout}s")
    except Exception as e:
        logger.warning(f"ComfyUI generation failed: {e}")

    return None


def save_video(video_url: str, save_dir: str = "") -> str:
    if not save_dir:
        save_dir = utils.storage_dir("cache_videos")

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    url_without_query = video_url.split("?")[0]
    url_hash = utils.md5(url_without_query)
    video_id = f"vid-{url_hash}"
    video_path = f"{save_dir}/{video_id}.mp4"

    # if video already exists, return the path
    if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
        logger.info(f"video already exists: {video_path}")
        return video_path

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    # if video does not exist, download it
    with open(video_path, "wb") as f:
        f.write(
            requests.get(
                video_url,
                headers=headers,
                proxies=config.proxy,
                verify=_get_tls_verify(),
                timeout=(60, 240),
            ).content
        )

    if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
        clip = None
        try:
            clip = VideoFileClip(video_path)
            duration = clip.duration
            fps = clip.fps
            if duration > 0 and fps > 0:
                return video_path
        except Exception as e:
            logger.warning(f"invalid video file: {video_path} => {str(e)}")
            try:
                os.remove(video_path)
            except Exception as remove_error:
                logger.warning(
                    f"failed to remove invalid video file: {video_path}, error: {str(remove_error)}"
                )
        finally:
            if clip is not None:
                try:
                    clip.close()
                except Exception as close_error:
                    logger.warning(
                        f"failed to close video clip: {video_path}, error: {str(close_error)}"
                    )
    return ""


def download_videos(
    task_id: str,
    search_terms: List[str],
    source: str = "pexels",
    video_aspect: VideoAspect = VideoAspect.portrait,
    video_concat_mode: VideoConcatMode = VideoConcatMode.random,
    audio_duration: float = 0.0,
    max_clip_duration: int = 5,
    match_script_order: bool = False,
    use_comfyui_fallback: bool = False,
) -> List[str]:
    search_videos = search_videos_pexels
    if source == "pixabay":
        search_videos = search_videos_pixabay
    elif source == "coverr":
        search_videos = search_videos_coverr
    elif source == "comfyui":
        search_videos = search_videos_comfyui
    elif source == "auto":
        search_videos = search_videos_auto

    material_directory = config.app.get("material_directory", "").strip()
    if material_directory == "task":
        material_directory = utils.task_dir(task_id)
    elif material_directory and not os.path.isdir(material_directory):
        material_directory = ""

    if match_script_order and source != "auto":
        return _download_videos_by_script_order(
            task_id=task_id,
            search_terms=search_terms,
            search_videos=search_videos,
            video_aspect=video_aspect,
            audio_duration=audio_duration,
            max_clip_duration=max_clip_duration,
            material_directory=material_directory,
        )

    aspect_enum = VideoAspect(video_aspect) if not isinstance(video_aspect, VideoAspect) else video_aspect
    target_width, target_height = aspect_enum.to_resolution()

    normalized_pairs = _normalize_search_terms(search_terms)

    term_groups = []
    valid_video_urls = set()
    found_duration = 0.0
    for normalized_term, original_term in normalized_pairs:
        video_items = search_videos(
            search_term=normalized_term,
            minimum_duration=max_clip_duration,
            video_aspect=video_aspect,
        )
        logger.info(f"found {len(video_items)} videos for '{normalized_term}'")

        scored_items = []
        for item in video_items:
            if item.url in valid_video_urls:
                continue
            if not _is_clip_relevant(item, original_term):
                logger.debug(f"  skipping clip (not relevant): {item.url}")
                continue
            if not _verify_clip_with_twelvelabs(item, search_term):
                logger.debug(f"  skipping clip (TwelveLabs rejected): {item.url}")
                continue
            valid_video_urls.add(item.url)
            score = _score_clip_quality(item, target_width, target_height)
            scored_items.append((score, item))
            found_duration += item.duration

        scored_items.sort(key=lambda x: x[0], reverse=True)

        if scored_items:
            term_groups.append((search_term, scored_items))

    logger.info(
        f"found total videos across {len(term_groups)} term groups, "
        f"required duration: {audio_duration} seconds, found duration: {found_duration} seconds"
    )
    video_paths = []

    concat_mode_value = getattr(video_concat_mode, "value", video_concat_mode)

    round_robin_pool = []
    max_rounds = max((len(items) for _, items in term_groups), default=0)
    for round_idx in range(max_rounds):
        for _, items in term_groups:
            if round_idx < len(items):
                round_robin_pool.append(items[round_idx][1])

    if concat_mode_value == VideoConcatMode.random.value:
        random.shuffle(round_robin_pool)

    total_duration = 0.0
    for item in round_robin_pool:
        try:
            logger.info(f"downloading video: {item.url}")
            saved_video_path = save_video(
                video_url=item.url, save_dir=material_directory
            )
            if saved_video_path:
                logger.info(f"video saved: {saved_video_path}")
                video_paths.append(saved_video_path)
                seconds = min(max_clip_duration, item.duration)
                total_duration += seconds
                if total_duration > audio_duration:
                    logger.info(
                        f"total duration of downloaded videos: {total_duration} seconds, skip downloading more"
                    )
                    break
        except Exception as e:
            logger.error(f"failed to download video: {utils.to_json(item)} => {str(e)}")

    # ComfyUI fallback: if we got few or no clips, try generating custom ones
    if use_comfyui_fallback and (len(video_paths) < 2 or total_duration < audio_duration * 0.5):
        comfy_generated = 0
        for search_term in search_terms:
            if total_duration >= audio_duration:
                break
            logger.info(f"ComfyUI fallback: generating video for '{search_term}'")
            try:
                generated = generate_video_comfyui(
                    prompt=search_term,
                    video_aspect=video_aspect,
                    duration=max_clip_duration * 2,
                )
                if generated:
                    saved = save_video(video_url=generated.url, save_dir=material_directory)
                    if saved:
                        video_paths.append(saved)
                        total_duration += min(max_clip_duration, generated.duration)
                        comfy_generated += 1
                        logger.success(f"ComfyUI fallback generated clip {comfy_generated}: {saved}")
            except Exception as e:
                logger.warning(f"ComfyUI fallback failed for '{search_term}': {e}")

        if comfy_generated:
            logger.success(f"ComfyUI fallback generated {comfy_generated} additional clips")

    ai_paths = image_gen.generate_ai_clips(
        prompts=search_terms,
        save_dir=material_directory,
        video_aspect=video_aspect,
        clip_duration=max_clip_duration,
        max_clips=config.app.get("ai_image_clips_count", 2),
    )
    if ai_paths:
        video_paths = image_gen.interleave_clips(
            stock_paths=video_paths,
            ai_paths=ai_paths,
            every_n=config.app.get("ai_clip_interleave_every", 4),
        )

    logger.success(f"downloaded {len(video_paths)} videos")
    return video_paths


def _download_videos_by_script_order(
    task_id: str,
    search_terms: List[str],
    search_videos,
    video_aspect: VideoAspect,
    audio_duration: float,
    max_clip_duration: int,
    material_directory: str,
) -> List[str]:
    """
    按脚本文案顺序下载素材。

    默认下载逻辑会把所有关键词的候选素材合并成一个大列表；如果第一个
    关键词返回很多结果，最终下载时可能一直消耗这个关键词的素材，后续
    脚本主题就排不上时间线。这里按关键词分组后轮询下载：
    第 1 轮取每个关键词的第 1 个候选，第 2 轮取每个关键词的第 2 个候选。
    这样在不重写视频合成引擎的前提下，尽量保证素材顺序贴近文案顺序。
    """
    logger.info("downloading videos with script-order material matching")
    candidate_groups = []
    valid_video_urls = set()
    found_duration = 0.0

    for search_term in search_terms:
        video_items = search_videos(
            search_term=search_term,
            minimum_duration=max_clip_duration,
            video_aspect=video_aspect,
        )
        logger.info(f"found {len(video_items)} videos for '{search_term}'")

        term_items = []
        for item in video_items:
            if item.url in valid_video_urls:
                continue
            if not _is_clip_relevant(item, search_term):
                logger.debug(f"  skipping clip (not relevant): {item.url}")
                continue
            if not _verify_clip_with_twelvelabs(item, search_term):
                logger.debug(f"  skipping clip (TwelveLabs rejected): {item.url}")
                continue
            term_items.append(item)
            valid_video_urls.add(item.url)
            found_duration += item.duration

        if term_items:
            candidate_groups.append((search_term, term_items))

    logger.info(
        f"found total ordered video candidates: {sum(len(items) for _, items in candidate_groups)}, "
        f"required duration: {audio_duration} seconds, found duration: {found_duration} seconds"
    )

    video_paths = []
    total_duration = 0.0
    candidate_index = 0
    while candidate_groups and total_duration <= audio_duration:
        has_candidate = False
        for search_term, term_items in candidate_groups:
            if candidate_index >= len(term_items):
                continue

            has_candidate = True
            item = term_items[candidate_index]
            try:
                logger.info(
                    f"downloading ordered video for '{search_term}': {item.url}"
                )
                saved_video_path = save_video(
                    video_url=item.url, save_dir=material_directory
                )
                if saved_video_path:
                    logger.info(f"video saved: {saved_video_path}")
                    video_paths.append(saved_video_path)
                    total_duration += min(max_clip_duration, item.duration)
                    if total_duration > audio_duration:
                        logger.info(
                            f"total duration of downloaded videos: {total_duration} seconds, skip downloading more"
                        )
                        break
            except Exception as e:
                logger.error(
                    f"failed to download ordered video: {utils.to_json(item)} => {str(e)}"
                )

        if not has_candidate:
            break
        candidate_index += 1

    logger.success(f"downloaded {len(video_paths)} ordered videos")
    return video_paths


if __name__ == "__main__":
    download_videos(
        "test123", ["Money Exchange Medium"], audio_duration=100, source="pixabay"
    )
