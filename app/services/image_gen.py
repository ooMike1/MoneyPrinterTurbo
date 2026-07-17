import os
import random
import tempfile
import time
import urllib.parse
from uuid import uuid4

import requests
from loguru import logger
from moviepy import ImageClip

from app.config import config
from app.models.schema import VideoAspect

_POLLINATIONS_IMAGE_URL = "https://image.pollinations.ai/prompt/{prompt}"
_DEAPI_BASE_URL = "https://api.deapi.ai"


def _download_image(
    prompt: str,
    width: int,
    height: int,
    save_dir: str,
    model: str = "flux",
) -> str | None:
    url = _POLLINATIONS_IMAGE_URL.format(prompt=urllib.parse.quote(prompt))
    params = {
        "width": width,
        "height": height,
        "model": model,
        "seed": random.randint(0, 99999),
        "nologo": "true",
    }
    url = f"{url}?{urllib.parse.urlencode(params)}"
    logger.info(f"generating image via Pollinations.ai: prompt='{prompt}'")

    try:
        resp = requests.get(url, timeout=60)
        if resp.status_code != 200:
            logger.warning(f"Pollinations.ai returned {resp.status_code}")
            return None
        ext = "jpg"
        img_path = os.path.join(save_dir, f"ai_img_{uuid4().hex}.{ext}")
        with open(img_path, "wb") as f:
            f.write(resp.content)
        if os.path.getsize(img_path) == 0:
            os.remove(img_path)
            return None
        logger.info(f"image saved: {img_path}")
        return img_path
    except requests.Timeout:
        logger.warning("Pollinations.ai image generation timed out")
    except Exception as e:
        logger.warning(f"Pollinations.ai image generation failed: {e}")
    return None


def _get_deapi_key() -> str:
    return config.app.get("deapi_api_key", "").strip()


def _deapi_animate_image(
    image_path: str,
    prompt: str,
    output_path: str,
    target_width: int = 1080,
    target_height: int = 1920,
) -> str | None:
    api_key = _get_deapi_key()
    if not api_key:
        logger.warning("deAPI API key not configured, cannot use I2V")
        return None

    try:
        model = config.app.get("deapi_i2v_model", "Ltxv_13B_0_9_8_Distilled_FP8")
        fps = 10
        duration = 4
        frames_count = fps * duration
        steps = 25

        with open(image_path, "rb") as f:
            image_data = f.read()

        seed = random.randint(0, 999999)
        headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
        files = {"first_frame_image": ("image.jpg", image_data, "image/jpeg")}
        data = {
            "prompt": prompt,
            "model": model,
            "width": str(target_width),
            "height": str(target_height),
            "guidance": "5.0",
            "steps": str(steps),
            "seed": str(seed),
            "frames": str(frames_count),
            "fps": str(fps),
        }

        logger.info(
            f"submitting I2V job to deAPI.ai: model={model}, "
            f"{target_width}x{target_height}, {frames_count}frames @{fps}fps"
        )

        resp = requests.post(
            f"{_DEAPI_BASE_URL}/api/v2/videos/animations",
            headers=headers,
            files=files,
            data=data,
            timeout=120,
        )

        if resp.status_code not in (200, 201):
            logger.warning(f"deAPI I2V submission failed: {resp.status_code} {resp.text}")
            return None

        result_data = resp.json()
        request_id = result_data.get("data", {}).get("request_id")
        if not request_id:
            logger.warning(f"deAPI I2V: no request_id in response: {result_data}")
            return None

        logger.info(f"deAPI I2V job submitted: {request_id}")

        max_polls = 60
        poll_interval = 5

        for attempt in range(max_polls):
            time.sleep(poll_interval)

            status_resp = requests.get(
                f"{_DEAPI_BASE_URL}/api/v2/jobs/{request_id}",
                headers=headers,
                timeout=30,
            )

            if status_resp.status_code != 200:
                logger.warning(
                    f"deAPI job status check failed: "
                    f"{status_resp.status_code} {status_resp.text}"
                )
                continue

            status_data = status_resp.json().get("data", {})
            job_status = status_data.get("status", "")
            progress = status_data.get("progress", 0)

            if attempt % 4 == 0:
                logger.info(
                    f"deAPI I2V job {request_id}: status={job_status}, "
                    f"progress={progress}"
                )

            if job_status == "done":
                result_url = (
                    status_data.get("result_url")
                    or status_data.get("result", {}).get("url", "")
                )
                if not result_url:
                    logger.warning("deAPI I2V: job done but no result URL")
                    return None

                video_resp = requests.get(result_url, timeout=120)
                if video_resp.status_code != 200:
                    logger.warning(
                        f"deAPI I2V: failed to download result: "
                        f"{video_resp.status_code}"
                    )
                    return None

                with open(output_path, "wb") as f:
                    f.write(video_resp.content)

                if os.path.getsize(output_path) > 0:
                    logger.info(f"deAPI I2V clip saved: {output_path}")
                    return output_path
                return None

            elif job_status in ("failed", "error"):
                logger.warning(f"deAPI I2V job failed: {status_data}")
                return None

        logger.warning(f"deAPI I2V job timed out after {max_polls * poll_interval}s")
        return None

    except Exception as e:
        logger.warning(f"deAPI I2V failed: {e}")
        return None


def _animate_image_to_video(
    image_path: str,
    output_path: str,
    duration: int = 5,
    fps: int = 24,
    target_width: int = 1080,
    target_height: int = 1920,
) -> str | None:
    try:
        clip = ImageClip(image_path).with_duration(duration)

        clip_ratio = clip.w / clip.h
        target_ratio = target_width / target_height
        if clip_ratio > target_ratio:
            clip = clip.resized(height=target_height)
        else:
            clip = clip.resized(width=target_width)

        cx = clip.w / 2
        cy = clip.h / 2
        clip = clip.cropped(x_center=cx, y_center=cy, width=target_width, height=target_height)

        zoom_fn = lambda t: 1.0 + 0.05 * (t / duration)
        clip = clip.resized(zoom_fn)

        clip.write_videofile(
            output_path,
            codec="libx264",
            audio=False,
            logger=None,
            fps=fps,
            preset="medium",
            ffmpeg_params=["-pix_fmt", "yuv420p"],
        )
        clip.close()

        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            logger.info(f"animated clip saved: {output_path}")
            return output_path
    except Exception as e:
        logger.warning(f"failed to animate image: {e}")
    return None


def generate_ai_clip(
    prompt: str,
    save_dir: str,
    video_aspect: VideoAspect = VideoAspect.portrait,
    duration: int = 5,
    model: str = "flux",
) -> str:
    aspect = VideoAspect(video_aspect) if not isinstance(video_aspect, VideoAspect) else video_aspect
    target_width, target_height = aspect.to_resolution()

    img_path = _download_image(prompt, target_width, target_height, save_dir, model)
    if not img_path:
        return ""

    output_path = os.path.join(save_dir, f"ai_clip_{uuid4().hex}.mp4")

    provider = config.app.get("ai_i2v_provider", "moviepy")
    result = None

    if provider == "deapi":
        i2v_prompt = f"natural gentle motion, {prompt}"
        result = _deapi_animate_image(
            img_path, i2v_prompt, output_path,
            target_width=target_width, target_height=target_height,
        )

    if not result:
        result = _animate_image_to_video(
            img_path, output_path, duration,
            target_width=target_width, target_height=target_height,
        )

    if img_path and os.path.exists(img_path):
        try:
            os.remove(img_path)
        except Exception:
            pass

    return result or ""


def generate_ai_clips(
    prompts: list[str],
    save_dir: str,
    video_aspect: VideoAspect = VideoAspect.portrait,
    clip_duration: int = 5,
    max_clips: int = 2,
) -> list[str]:
    cfg_enabled = config.app.get("ai_image_clips_enabled", True)
    if not cfg_enabled:
        logger.info("AI image clips are disabled, skipping generation")
        return []

    if not save_dir:
        save_dir = tempfile.mkdtemp()
    os.makedirs(save_dir, exist_ok=True)

    count = min(max_clips, len(prompts))
    if count == 0:
        return []

    chosen = random.sample(prompts, min(count, len(prompts)))

    ai_paths: list[str] = []
    for prompt in chosen:
        if len(ai_paths) >= max_clips:
            break
        path = generate_ai_clip(
            prompt=prompt,
            save_dir=save_dir,
            video_aspect=video_aspect,
            duration=clip_duration,
        )
        if path:
            ai_paths.append(path)

    if ai_paths:
        logger.success(f"generated {len(ai_paths)} AI image-based clips")
    else:
        logger.info("no AI image clips were generated")
    return ai_paths


def interleave_clips(
    stock_paths: list[str],
    ai_paths: list[str],
    every_n: int = 4,
) -> list[str]:
    if not ai_paths or not stock_paths:
        return stock_paths

    result: list[str] = []
    ai_idx = 0
    for i, path in enumerate(stock_paths):
        if i > 0 and i % every_n == 0 and ai_idx < len(ai_paths):
            result.append(ai_paths[ai_idx])
            ai_idx += 1
        result.append(path)

    while ai_idx < len(ai_paths):
        result.append(ai_paths[ai_idx])
        ai_idx += 1

    return result
