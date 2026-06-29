"""fal.ai image generation API client.

Calls fal.ai hosted models (default: Z-Image Turbo, ``fal-ai/z-image/turbo``)
over the public HTTP API. Supports both the synchronous endpoint
(``https://fal.run/<model>``) and the queue endpoint
(``https://queue.fal.run/<model>``) transparently.

Docs: https://fal.ai/models/fal-ai/z-image/turbo
Auth: ``Authorization: Key <FAL_KEY>``
"""

import logging
import os
import time
from typing import Dict, List, Optional

import requests

from .config import Config

DEFAULT_FAL_BASE_URL = "https://fal.run"

# Cap the longer side of generated images to keep fal.ai outputs small (and faster/cheaper).
DEFAULT_MAX_IMAGE_DIMENSION = 768

# Friendly model name (as registered in api_media.IMAGE_MODELS) -> fal endpoint id.
MODEL_ENDPOINT_MAP: Dict[str, str] = {
    "z-image-turbo": "fal-ai/z-image/turbo",
    "z-image/turbo": "fal-ai/z-image/turbo",
}


def normalize_endpoint_id(model: str) -> str:
    """Resolve a registered model name to a fal endpoint id (e.g. ``fal-ai/z-image/turbo``)."""
    if not model:
        return MODEL_ENDPOINT_MAP["z-image-turbo"]
    if model.startswith("fal-ai/"):
        return model
    return MODEL_ENDPOINT_MAP.get(model, model)


def _round_to_multiple(value: int, multiple: int = 16, minimum: int = 256) -> int:
    """Round ``value`` to the nearest multiple of ``multiple`` (diffusion models expect this), with a floor."""
    rounded = int(round(value / multiple)) * multiple
    return max(minimum, rounded)


def _explicit_image_size(size: Optional[str], max_dimension: int = DEFAULT_MAX_IMAGE_DIMENSION) -> dict:
    """Compute an explicit fal ``{width, height}`` from a ``"WIDTH*HEIGHT"`` string.

    The output is downscaled so the longer side does not exceed ``max_dimension``
    while preserving the requested aspect ratio. Dimensions are only scaled down,
    never up. Passing explicit width/height (instead of fal's ~1024px named sizes)
    is what lets us generate smaller images.
    """
    width = height = 0
    if size and "*" in size:
        parts = size.split("*")
        if len(parts) == 2:
            try:
                width, height = int(parts[0]), int(parts[1])
            except ValueError:
                width = height = 0
    if width <= 0 or height <= 0:
        return {"width": max_dimension, "height": max_dimension}

    longest = max(width, height)
    if longest > max_dimension:
        scale = max_dimension / longest
        width = int(round(width * scale))
        height = int(round(height * scale))

    return {"width": _round_to_multiple(width), "height": _round_to_multiple(height)}


class FalImageClient:
    """fal.ai text-to-image client."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        local_proxy: Optional[str] = None,
        timeout: int = 300,
        poll_interval: float = 2.0,
        max_dimension: int = DEFAULT_MAX_IMAGE_DIMENSION,
    ) -> None:
        self.api_key = api_key or Config.FAL_API_KEY
        self.base_url = (base_url or Config.FAL_BASE_URL or DEFAULT_FAL_BASE_URL).rstrip("/")
        self.local_proxy = local_proxy
        self.timeout = timeout
        self.poll_interval = poll_interval
        self.max_dimension = max_dimension

        if not self.api_key:
            logging.warning("FalImageClient missing api_key. Set fal.ai API key (FAL_KEY).")

    @property
    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Key {self.api_key}",
            "Content-Type": "application/json",
        }

    @property
    def _proxies(self):
        if self.local_proxy:
            return {"http": self.local_proxy, "https": self.local_proxy}
        return None

    def generate_image(
        self,
        prompt: str,
        model: str = "z-image-turbo",
        size: Optional[str] = None,
        session_id: Optional[str] = None,
        save_dir: Optional[str] = None,
        image_paths: Optional[List[str]] = None,
        num_images: int = 1,
        **kwargs,
    ) -> List[str]:
        """Generate image(s) and return the local file paths of the downloads.

        Args:
            prompt: Text prompt.
            model: Registered model name (e.g. ``z-image-turbo``).
            size: ``"WIDTH*HEIGHT"`` string used to derive the fal ``image_size``.
            session_id: Used to organize the download directory when ``save_dir`` is not given.
            save_dir: Directory to save generated images into.
            image_paths: Reference images (ignored; Z-Image Turbo is text-to-image only).
            num_images: Number of images to generate.
        """
        if not self.api_key:
            raise RuntimeError("fal.ai API key not set. Configure it in Settings > API Media Models.")

        if image_paths:
            logging.warning("fal.ai z-image/turbo is text-to-image only; ignoring reference images.")

        endpoint_id = normalize_endpoint_id(model)
        payload = {
            "prompt": prompt,
            "image_size": kwargs.get("image_size") or _explicit_image_size(size, self.max_dimension),
            "num_images": int(num_images or 1),
            "output_format": kwargs.get("output_format", "png"),
            "enable_safety_checker": kwargs.get("enable_safety_checker", True),
        }
        if kwargs.get("num_inference_steps") is not None:
            payload["num_inference_steps"] = int(kwargs["num_inference_steps"])
        if kwargs.get("seed") is not None:
            payload["seed"] = kwargs["seed"]
        if kwargs.get("acceleration"):
            payload["acceleration"] = kwargs["acceleration"]

        if Config.PRINT_MODEL_INPUT:
            print(f"[fal.ai] endpoint={endpoint_id} payload={payload}")

        logging.info(f"FalImageClient requesting {endpoint_id} (image_size={payload['image_size']})")
        result = self._run(endpoint_id, payload)

        images = result.get("images") or []
        if not images:
            raise RuntimeError(f"fal.ai returned no images: {str(result)[:500]}")

        save_dir = self._resolve_save_dir(save_dir, session_id)
        generated_paths: List[str] = []
        for idx, image in enumerate(images):
            url = image.get("url") if isinstance(image, dict) else None
            if not url:
                continue
            local_path = self._download_image(url, save_dir, idx, payload["output_format"])
            if local_path:
                generated_paths.append(local_path)

        return generated_paths

    def _run(self, endpoint_id: str, payload: dict) -> dict:
        """Submit a request and return the result dict, handling sync and queue responses."""
        url = f"{self.base_url}/{endpoint_id}"
        resp = requests.post(
            url, json=payload, headers=self._headers, timeout=self.timeout, proxies=self._proxies
        )
        data = self._json_or_raise(resp, context=f"POST {url}")

        # Synchronous endpoint (fal.run) returns the result inline.
        if isinstance(data, dict) and data.get("images"):
            return data

        # Queue endpoint returns request handles to poll.
        response_url = data.get("response_url") if isinstance(data, dict) else None
        status_url = data.get("status_url") if isinstance(data, dict) else None
        if not response_url:
            raise RuntimeError(f"fal.ai returned an unexpected response: {str(data)[:500]}")

        deadline = time.time() + self.timeout
        while time.time() < deadline:
            if status_url:
                status_data = self._json_or_raise(
                    requests.get(status_url, headers=self._headers, timeout=self.timeout, proxies=self._proxies),
                    context=f"GET {status_url}",
                )
                status = (status_data or {}).get("status")
                if status == "COMPLETED":
                    break
                if status in ("FAILED", "ERROR", "CANCELED", "CANCELLED"):
                    raise RuntimeError(f"fal.ai request {status}: {str(status_data)[:500]}")
            time.sleep(self.poll_interval)
        else:
            raise TimeoutError(f"fal.ai request timed out after {self.timeout}s: {endpoint_id}")

        return self._json_or_raise(
            requests.get(response_url, headers=self._headers, timeout=self.timeout, proxies=self._proxies),
            context=f"GET {response_url}",
        )

    def _json_or_raise(self, resp: "requests.Response", context: str) -> dict:
        """Return parsed JSON, surfacing the server's error body on failure."""
        if resp.status_code >= 400:
            body = ""
            try:
                body = resp.text[:1000]
            except Exception:
                body = ""
            raise RuntimeError(f"fal.ai error {resp.status_code} ({context}): {body}")
        try:
            return resp.json()
        except Exception as exc:
            raise RuntimeError(f"fal.ai returned non-JSON response ({context}): {resp.text[:500]}") from exc

    def _resolve_save_dir(self, save_dir: Optional[str], session_id: Optional[str]) -> str:
        if save_dir:
            os.makedirs(save_dir, exist_ok=True)
            return save_dir
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        result_dir = os.path.join(base_dir, "code", "result", "image", str(session_id or "default"))
        os.makedirs(result_dir, exist_ok=True)
        return result_dir

    def _download_image(self, url: str, save_dir: str, idx: int, output_format: str) -> Optional[str]:
        ext = output_format if output_format in ("png", "jpeg", "jpg", "webp") else "png"
        file_name = f"fal_{int(time.time())}_{idx}.{ext}"
        file_path = os.path.join(save_dir, file_name)
        try:
            resp = requests.get(url, timeout=self.timeout, proxies=self._proxies)
            resp.raise_for_status()
            with open(file_path, "wb") as f:
                f.write(resp.content)
            return file_path
        except Exception as exc:
            logging.error(f"Failed to download fal.ai image from {url}: {exc}")
            return None


if __name__ == "__main__":
    import sys

    print("=== fal.ai Z-Image Turbo availability test ===")
    api_key = os.getenv("FAL_KEY") or os.getenv("FAL_API_KEY") or ""
    if not api_key:
        print("✗ FAL_KEY not set, skipping")
        sys.exit(1)
    print(f"  API Key: {api_key[:6]}***{api_key[-4:]}")

    client = FalImageClient(api_key=api_key)
    t0 = time.time()
    try:
        paths = client.generate_image(
            prompt="A serene mountain lake at sunrise, photorealistic, cinematic lighting",
            model="z-image-turbo",
            size="1080*1920",
            session_id="fal_test",
        )
        elapsed = time.time() - t0
        if paths:
            print(f"✓ Generated {len(paths)} image(s) ({elapsed:.1f}s): {paths}")
        else:
            print(f"✗ Returned empty list ({elapsed:.1f}s)")
    except Exception as exc:
        print(f"✗ Generation failed: {exc}")
