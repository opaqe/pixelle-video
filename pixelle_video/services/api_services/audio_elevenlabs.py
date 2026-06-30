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

"""ElevenLabs text-to-speech (TTS) API client.

Calls the native ElevenLabs HTTP API
(``POST https://api.elevenlabs.io/v1/text-to-speech/<voice_id>``). The endpoint
returns raw audio bytes (``audio/mpeg`` by default), which are written straight
to the output file.

Docs: https://elevenlabs.io/docs/api-reference/text-to-speech
Auth: ``xi-api-key: <API_KEY>``
"""

import logging
import os
import time
from typing import Dict, Optional

import requests

DEFAULT_ELEVENLABS_BASE_URL = "https://api.elevenlabs.io"
DEFAULT_ELEVENLABS_MODEL = "eleven_multilingual_v2"
# Long-standing premade voice ("Rachel"), available to all accounts.
DEFAULT_ELEVENLABS_VOICE = "21m00Tcm4TlvDq8ikWAM"
DEFAULT_OUTPUT_FORMAT = "mp3_44100_128"


class ElevenLabsTTSClient:
    """ElevenLabs text-to-speech client."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        local_proxy: Optional[str] = None,
        timeout: int = 300,
    ) -> None:
        self.api_key = api_key or ""
        self.base_url = (base_url or DEFAULT_ELEVENLABS_BASE_URL).rstrip("/")
        self.model = model or DEFAULT_ELEVENLABS_MODEL
        self.local_proxy = local_proxy
        self.timeout = timeout

        if not self.api_key:
            logging.warning("ElevenLabsTTSClient missing api_key. Set the ElevenLabs API key.")

    @property
    def _headers(self) -> Dict[str, str]:
        return {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        }

    @property
    def _proxies(self):
        if self.local_proxy:
            return {"http": self.local_proxy, "https": self.local_proxy}
        return None

    def generate_speech(
        self,
        text: str,
        voice: Optional[str] = None,
        model: Optional[str] = None,
        output_path: Optional[str] = None,
        save_dir: Optional[str] = None,
        session_id: Optional[str] = None,
        output_format: str = DEFAULT_OUTPUT_FORMAT,
        print_input: bool = False,
        **kwargs,
    ) -> str:
        """Synthesize ``text`` to speech and return the local audio file path.

        Args:
            text: Text to convert to speech.
            voice: ElevenLabs voice id (defaults to a premade voice).
            model: ElevenLabs model id (defaults to the client model).
            output_path: Exact output file path. Takes precedence over ``save_dir``.
            save_dir: Directory to save the generated audio into.
            session_id: Used to organize the download directory when no path is given.
            output_format: ElevenLabs ``output_format`` query value (e.g. ``mp3_44100_128``).
        """
        if not self.api_key:
            raise RuntimeError("ElevenLabs API key not set. Configure it in Settings > Voice Model Settings.")

        if not text or not text.strip():
            raise ValueError("ElevenLabs TTS requires non-empty text.")

        voice_id = (voice or DEFAULT_ELEVENLABS_VOICE).strip()
        model_id = (model or self.model or DEFAULT_ELEVENLABS_MODEL).strip()

        payload: Dict[str, object] = {"text": text, "model_id": model_id}
        for key, value in kwargs.items():
            if value is not None:
                payload[key] = value

        if print_input:
            print(f"[ElevenLabs] voice={voice_id} model={model_id} output_format={output_format}")

        url = f"{self.base_url}/v1/text-to-speech/{voice_id}"
        logging.info(f"ElevenLabsTTSClient requesting voice={voice_id} model={model_id}")

        resp = requests.post(
            url,
            json=payload,
            headers=self._headers,
            params={"output_format": output_format} if output_format else None,
            timeout=self.timeout,
            proxies=self._proxies,
        )
        if resp.status_code >= 400:
            body = ""
            try:
                body = resp.text[:1000]
            except Exception:
                body = ""
            raise RuntimeError(f"ElevenLabs error {resp.status_code} (POST {url}): {body}")

        audio_bytes = resp.content
        if not audio_bytes:
            raise RuntimeError("ElevenLabs returned an empty audio response.")

        ext = "mp3" if output_format.startswith("mp3") else ("wav" if output_format.startswith("pcm") else "mp3")
        target_path = self._resolve_output_path(output_path, save_dir, session_id, ext)
        with open(target_path, "wb") as f:
            f.write(audio_bytes)
        return target_path

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

        return os.path.join(target_dir, f"elevenlabs_{int(time.time())}.{audio_ext}")


if __name__ == "__main__":
    import sys

    print("=== ElevenLabs TTS availability test ===")
    api_key = os.getenv("ELEVENLABS_API_KEY") or os.getenv("ELEVEN_API_KEY") or ""
    if not api_key:
        print("✗ ELEVENLABS_API_KEY not set, skipping")
        sys.exit(1)
    print(f"  API Key: {api_key[:6]}***{api_key[-4:]}")

    client = ElevenLabsTTSClient(api_key=api_key)
    t0 = time.time()
    try:
        path = client.generate_speech(
            text="안녕하세요. 일레븐랩스 음성 합성 테스트입니다.",
            session_id="elevenlabs_test",
        )
        elapsed = time.time() - t0
        print(f"✓ Generated audio ({elapsed:.1f}s): {path}")
    except Exception as exc:
        print(f"✗ Generation failed: {exc}")
