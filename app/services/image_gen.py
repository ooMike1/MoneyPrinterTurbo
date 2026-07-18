import os
import random
import tempfile
import threading
import time
import urllib.parse
from uuid import uuid4

import requests
from loguru import logger
from moviepy import ImageClip
from PIL import Image

from app.config import config
from app.models.schema import VideoAspect

_POLLINATIONS_IMAGE_URL = "https://image.pollinations.ai/prompt/{prompt}"
_DEAPI_BASE_URL = "https://api.deapi.ai"

def _get_deapi_i2v_max_concurrent() -> int:
    return int(config.app.get("deapi_i2v_max_concurrent", 1))

_deapi_i2v_max_concurrent = _get_deapi_i2v_max_concurrent()
_deapi_i2v_slots = threading.BoundedSemaphore(value=_deapi_i2v_max_concurrent)


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
        "seed": random.randint(0, 999999),
        "nologo": "true",
        "enhance": "true",
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

    max_concurrent = _get_deapi_i2v_max_concurrent()
    _deapi_i2v_slots.acquire()
    try:
        model = config.app.get("deapi_i2v_model", "Ltx2_19B_Dist_FP8")

        max_dim = 1024
        if target_width > max_dim or target_height > max_dim:
            scale = min(max_dim / target_width, max_dim / target_height)
            target_width = int(target_width * scale)
            target_height = int(target_height * scale)

        fps = 24
        frames_count = fps * 4
        frames_count = max(frames_count, 49)
        frames_count = min(frames_count, 241)

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
            "seed": str(seed),
            "frames": str(frames_count),
            "fps": str(fps),
        }

        logger.info(
            f"submitting I2V job to deAPI.ai: model={model}, "
            f"{target_width}x{target_height}, {frames_count}frames @{fps}fps"
        )

        max_concurrent = _get_deapi_i2v_max_concurrent()
        max_retries = int(config.app.get("deapi_i2v_max_retries", 5))
        base_backoff = int(config.app.get("deapi_i2v_base_backoff", 10))
        for retry in range(max_retries):
            resp = requests.post(
                f"{_DEAPI_BASE_URL}/api/v2/videos/animations",
                headers=headers,
                files=files,
                data=data,
                timeout=120,
            )

            if resp.status_code == 429:
                if retry < max_retries - 1:
                    backoff = base_backoff * (2**retry)
                    logger.warning(
                        f"deAPI I2V rate-limited (429): {resp.text}. "
                        f"Retrying in {backoff}s (attempt {retry + 1}/{max_retries}, concurrency limit: {max_concurrent})"
                    )
                    time.sleep(backoff)
                    continue
                logger.warning(
                    f"deAPI I2V rate-limited (429) after {max_retries} retries: {resp.text}. "
                    f"Consider reducing concurrency (current limit: {max_concurrent})"
                )
                return None

            if resp.status_code not in (200, 201):
                logger.warning(f"deAPI I2V submission failed: {resp.status_code} {resp.text}")
                return None

            break

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
                    logger.warning("deAPI I2V: job done but no URL returned")
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
    finally:
        _deapi_i2v_slots.release()


def _animate_image_to_video(
    image_path: str,
    output_path: str,
    duration: int = 5,
    fps: int = 24,
    target_width: int = 1080,
    target_height: int = 1920,
    ken_burns_strength: float = 0.08,
) -> str | None:
    """
    Create a smooth Ken Burns style animation from a static image.

    Improvements over the old version:
    - Uses PIL for high-quality resampling (LANCZOS) instead of MoviePy's repeated resize
    - Maintains aspect ratio with letterboxing instead of forced cropping
    - Applies a single smooth transform per frame rather than compounding resize operations
    - Configurable zoom/pan strength to avoid excessive distortion
    """
    try:
        with Image.open(image_path) as img:
            img.load()
            src_w, src_h = img.size
            src_ratio = src_w / src_h
            target_ratio = target_width / target_height

            # Calculate the canvas size that preserves the full image
            # with letterboxing/pillarboxing to target aspect ratio
            if src_ratio > target_ratio:
                # Source is wider: fit to width, letterbox top/bottom
                canvas_w = target_width
                canvas_h = int(target_width / src_ratio)
            else:
                # Source is taller: fit to height, pillarbox left/right
                canvas_h = target_height
                canvas_w = int(target_height * src_ratio)

            # Create a high-res canvas for the animation (2x target for quality)
            # We animate at 2x and downscale at the end for anti-aliasing
            super_w = canvas_w * 2
            super_h = canvas_h * 2

            # Pre-resize the source image to the super-resolution canvas once
            img_resized = img.resize((super_w, super_h), Image.Resampling.LANCZOS)

            # Ken Burns parameters: gentle zoom + optional slow pan
            # Zoom from 1.0 to 1.0 + ken_burns_strength
            zoom_start = 1.0
            zoom_end = 1.0 + ken_burns_strength

            # Pan range: up to 10% of the canvas in each direction
            pan_range_x = (super_w - target_width * 2) * 0.1
            pan_range_y = (super_h - target_height * 2) * 0.1
            pan_start_x = random.uniform(-pan_range_x, pan_range_x)
            pan_start_y = random.uniform(-pan_range_y, pan_range_y)
            pan_end_x = random.uniform(-pan_range_x, pan_range_x)
            pan_end_y = random.uniform(-pan_range_y, pan_range_y)

            frames = []
            total_frames = fps * duration

            logger.debug(f"Generating {total_frames} frames for Ken Burns animation")

            for frame_idx in range(total_frames):
                t = frame_idx / max(total_frames - 1, 1)
                # Smooth easing (ease-in-out)
                progress = t * t * (3 - 2 * t)

                # Interpolate zoom and pan
                zoom = zoom_start + (zoom_end - zoom_start) * progress
                pan_x = pan_start_x + (pan_end_x - pan_start_x) * progress
                pan_y = pan_start_y + (pan_end_y - pan_start_y) * progress

                # Calculate crop box on the super-res canvas
                crop_w = super_w / zoom
                crop_h = super_h / zoom
                center_x = super_w / 2 + pan_x
                center_y = super_h / 2 + pan_y

                left = center_x - crop_w / 2
                top = center_y - crop_h / 2
                right = left + crop_w
                bottom = top + crop_h

                # Clamp to image bounds
                left = max(0, min(left, super_w - crop_w))
                top = max(0, min(top, super_h - crop_h))
                right = left + crop_w
                bottom = top + crop_h

                # Crop and downscale to target resolution in one step
                frame = img_resized.crop((left, top, right, bottom))
                frame = frame.resize((target_width, target_height), Image.Resampling.LANCZOS)
                frames.append(frame)

            # Write frames to video using ffmpeg directly for best quality
            import subprocess
            import tempfile

            with tempfile.TemporaryDirectory() as tmpdir:
                # Save frames as PNG sequence
                for i, frame in enumerate(frames):
                    frame.save(os.path.join(tmpdir, f"frame_{i:06d}.png"))

                # Encode with ffmpeg using high-quality settings
                cmd = [
                    "ffmpeg", "-y",
                    "-framerate", str(fps),
                    "-i", os.path.join(tmpdir, "frame_%06d.png"),
                    "-c:v", "libx264",
                    "-preset", "medium",
                    "-crf", "18",
                    "-pix_fmt", "yuv420p",
                    "-vf", "format=yuv420p",
                    output_path
                ]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                if result.returncode != 0:
                    logger.warning(f"ffmpeg encoding failed: {result.stderr}")
                    return None

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
        i2v_prompt = f"natural gentle motion, cinematic, high quality, {prompt}"
        result = _deapi_animate_image(
            img_path, i2v_prompt, output_path,
            target_width=target_width, target_height=target_height,
        )

    if not result:
        # Use improved Ken Burns animation with configurable strength
        ken_burns_strength = float(config.app.get("ai_ken_burns_strength", 0.08))
        result = _animate_image_to_video(
            img_path, output_path, duration,
            target_width=target_width, target_height=target_height,
            ken_burns_strength=ken_burns_strength,
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