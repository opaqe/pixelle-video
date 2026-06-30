# Copyright (C) 2025 AIDC-AI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""fal.ai text-to-speech (TTS) API client.

Calls fal.ai hosted TTS models (default: ``fal-ai/minimax-tts``) over the
public HTTP API. Supports both the synchronous endpoint
(``https://fal.run/<model>``) and the queue endpoint
(``https://queue.fal.run/<model>``) transparently.

The client targets the common fal TTS contract — request ``{"text", "voice"}``
and a response carrying an audio URL under ``audio.url`` (or a handful of
common variants) — so most fal TTS endpoints work without code changes. Pass
any registered fal model id; voice ids are model-specific.

Auth: ``Authorization: Key <FAL_KEY>``
"""

import logging
import os
import time
from typing import Dict, Optional

import requests

from .config import Config

DEFAULT_FAL_BASE_URL = "https://fal.run"
DEFAULT_FAL_TTS_MODEL = "fal-ai/minimax-tts"


def normalize_endpoint_id(model: str) -> str:
    """Resolve a model name to a fal endpoint id (e.g. ``fal-ai/minimax-tts``)."""
    return model.strip() if model and model.strip() else DEFAULT_FAL_TTS_MODEL


class FalTTSClient:
    """fal.ai text-to-speech client."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        local_proxy: Optional[str] = None,
        timeout: int = 300,
        poll_interval: float = 2.0,
    ) -> None:
        self.api_key = api_key or Config.FAL_API_KEY
        self.base_url = (base_url or Config.FAL_BASE_URL or DEFAULT_FAL_BASE_URL).rstrip("/")
        self.local_proxy = local_proxy
        self.timeout = timeout
        self.poll_interval = poll_interval

        if not self.api_key:
            logging.warning("FalTTSClient missing api_key. Set fal.ai API key (FAL_KEY).")

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

    def generate_speech(
        self,
        text: str,
        model: str = DEFAULT_FAL_TTS_MODEL,
        voice: Optional[str] = None,
        output_path: Optional[str] = None,
        save_dir: Optional[str] = None,
        session_id: Optional[str] = None,
        **kwargs,
    ) -> str:
        """Synthesize ``text`` to speech and return the local audio file path.

        Args:
            text: Text to convert to speech.
            model: Registered fal model id (e.g. ``fal-ai/minimax-tts``).
            voice: Model-specific voice id/name (optional).
            output_path: Exact output file path. Takes precedence over ``save_dir``.
            save_dir: Directory to save the generated audio into.
            session_id: Used to organize the download directory when no path is given.
            **kwargs: Extra request fields forwarded to the fal model verbatim
                (e.g. ``speed``, ``language``). ``None`` values are dropped.
        """
        if not self.api_key:
            raise RuntimeError("fal.ai API key not set. Configure it in Settings > API Media Models.")

        if not text or not text.strip():
            raise ValueError("fal.ai TTS requires non-empty text.")

        endpoint_id = normalize_endpoint_id(model)
        payload: Dict[str, object] = {"text": text}
        if voice:
            payload["voice"] = voice
        for key, value in kwargs.items():
            if value is not None:
                payload[key] = value

        if Config.PRINT_MODEL_INPUT:
            print(f"[fal.ai TTS] endpoint={endpoint_id} payload={payload}")

        logging.info(f"FalTTSClient requesting {endpoint_id} (voice={voice!r})")
        result = self._run(endpoint_id, payload)

        audio_url, audio_ext = self._extract_audio(result)
        if not audio_url:
            raise RuntimeError(f"fal.ai returned no audio: {str(result)[:500]}")

        target_path = self._resolve_output_path(output_path, save_dir, session_id, audio_ext)
        self._download_audio(audio_url, target_path)
        return target_path

    def _run(self, endpoint_id: str, payload: dict) -> dict:
        """Submit a request and return the result dict, handling sync and queue responses."""
        url = f"{self.base_url}/{endpoint_id}"
        resp = requests.post(
            url, json=payload, headers=self._headers, timeout=self.timeout, proxies=self._proxies
        )
        data = self._json_or_raise(resp, context=f"POST {url}")

        # Synchronous endpoint (fal.run) returns the result inline.
        if isinstance(data, dict) and self._extract_audio(data)[0]:
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

    @staticmethod
    def _extract_audio(data: object) -> tuple[Optional[str], str]:
        """Pull an audio URL (and file extension) out of a fal response.

        Handles the common shapes: ``{"audio": {"url": ...}}``,
        ``{"audio_url": ...}``, ``{"audio": "http..."}``, ``{"url": ...}`` and
        ``{"audios": [{"url": ...}]}``.
        """
        if not isinstance(data, dict):
            return None, "mp3"

        candidate = None
        audio = data.get("audio")
        if isinstance(audio, dict):
            candidate = audio.get("url")
        elif isinstance(audio, str):
            candidate = audio
        if not candidate:
            candidate = data.get("audio_url") or data.get("url")
        if not candidate:
            audios = data.get("audios")
            if isinstance(audios, list) and audios:
                first = audios[0]
                candidate = first.get("url") if isinstance(first, dict) else first

        if not isinstance(candidate, str) or not candidate:
            return None, "mp3"

        ext = "mp3"
        lowered = candidate.split("?")[0].lower()
        for known in ("wav", "mp3", "flac", "ogg", "m4a", "aac", "pcm"):
            if lowered.endswith(f".{known}"):
                ext = known
                break
        return candidate, ext

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

    def _resolve_output_path(
        self,
        output_path: Optional[str],
        save_dir: Optional[str],
        session_id: Optional[str],
        audio_ext: str,
    ) -> str:
        if output_path:
            parent = os.path.dirname(output_path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            return output_path

        if save_dir:
            os.makedirs(save_dir, exist_ok=True)
            target_dir = save_dir
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            target_dir = os.path.join(base_dir, "code", "result", "audio", str(session_id or "default"))
            os.makedirs(target_dir, exist_ok=True)

        return os.path.join(target_dir, f"fal_tts_{int(time.time())}.{audio_ext}")

    def _download_audio(self, url: str, file_path: str) -> str:
        resp = requests.get(url, timeout=self.timeout, proxies=self._proxies)
        resp.raise_for_status()
        with open(file_path, "wb") as f:
            f.write(resp.content)
        return file_path


if __name__ == "__main__":
    import sys

    print("=== fal.ai TTS availability test ===")
    api_key = os.getenv("FAL_KEY") or os.getenv("FAL_API_KEY") or ""
    if not api_key:
        print("✗ FAL_KEY not set, skipping")
        sys.exit(1)
    print(f"  API Key: {api_key[:6]}***{api_key[-4:]}")

    client = FalTTSClient(api_key=api_key)
    t0 = time.time()
    try:
        path = client.generate_speech(
            text="안녕하세요. fal.ai 음성 합성 테스트입니다.",
            model=DEFAULT_FAL_TTS_MODEL,
            session_id="fal_test",
        )
        elapsed = time.time() - t0
        print(f"✓ Generated audio ({elapsed:.1f}s): {path}")
    except Exception as exc:
        print(f"✗ Generation failed: {exc}")
