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

"""
Style configuration components for web UI (middle column)
"""

import os
from pathlib import Path

import streamlit as st
from loguru import logger

from web.i18n import tr, get_language
from web.utils.async_helpers import run_async
from pixelle_video.config import config_manager
from web.components.style_config import get_voicebox_profiles


def render_style_config(pixelle_video):
    """Render style configuration section (middle column)"""
    # TTS Section (moved from left column)
    # ====================================================================
    with st.container(border=True):
        st.markdown(f"**{tr('section.tts')}**")
        
        with st.expander(tr("help.feature_description"), expanded=False):
            st.markdown(f"**{tr('help.what')}**")
            st.markdown(tr("tts.what"))
            st.markdown(f"**{tr('help.how')}**")
            st.markdown(tr("tts.how"))
        
        # Get TTS config
        comfyui_config = config_manager.get_comfyui_config()
        tts_config = comfyui_config["tts"]
        
        # Inference mode selection
        tts_modes = ["local", "voicebox", "fal", "elevenlabs", "comfyui"]
        tts_mode_labels = {"voicebox": "VoiceBox", "fal": "fal.ai", "elevenlabs": "ElevenLabs"}
        tts_mode = st.radio(
            tr("tts.inference_mode"),
            tts_modes,
            horizontal=True,
            format_func=lambda x: tts_mode_labels.get(x, tr(f"tts.mode.{x}")),
            index=tts_modes.index(tts_config.get("inference_mode", "local")) if tts_config.get("inference_mode", "local") in tts_modes else 0,
            key="digital_tts_inference_mode"
        )

        # Show hint based on mode
        if tts_mode == "local":
            st.caption(tr("tts.mode.local_hint"))
        elif tts_mode == "voicebox":
            st.caption(f"VoiceBox Inference Endpoint: {config_manager.get_voicebox_endpoint()}")
        elif tts_mode == "fal":
            fal_model = tts_config.get("fal", {}).get("model", "fal-ai/minimax-tts")
            st.caption(f"fal.ai TTS Model: {fal_model}")
        elif tts_mode == "elevenlabs":
            el_model = tts_config.get("elevenlabs", {}).get("model", "eleven_multilingual_v2")
            st.caption(f"ElevenLabs Model: {el_model}")
        else:
            st.caption(tr("tts.mode.comfyui_hint"))
        
        # ================================================================
        # Local Mode UI
        # ================================================================
        if tts_mode == "local":
            # Import voice configuration
            from pixelle_video.tts_voices import EDGE_TTS_VOICES, get_voice_display_name
            
            # Get saved voice from config
            local_config = tts_config.get("local", {})
            saved_voice = local_config.get("voice", "zh-CN-YunjianNeural")
            saved_speed = local_config.get("speed", 1.2)
            
            # Build voice options with i18n
            voice_options = []
            voice_ids = []
            default_voice_index = 0
            
            for idx, voice_config in enumerate(EDGE_TTS_VOICES):
                voice_id = voice_config["id"]
                display_name = get_voice_display_name(voice_id, tr, get_language())
                voice_options.append(display_name)
                voice_ids.append(voice_id)
                
                # Set default index if matches saved voice
                if voice_id == saved_voice:
                    default_voice_index = idx
            
            # Two-column layout: Voice | Speed
            voice_col, speed_col = st.columns([1, 1])
            
            with voice_col:
                # Voice selector
                selected_voice_display = st.selectbox(
                    tr("tts.voice_selector"),
                    voice_options,
                    index=default_voice_index,
                    key="digital_tts_local_voice"
                )
                
                # Get actual voice ID
                selected_voice_index = voice_options.index(selected_voice_display)
                selected_voice = voice_ids[selected_voice_index]
            
            with speed_col:
                # Speed slider
                tts_speed = st.slider(
                    tr("tts.speed"),
                    min_value=0.5,
                    max_value=2.0,
                    value=saved_speed,
                    step=0.1,
                    format="%.1fx",
                    key="digital_tts_local_speed"
                )
                st.caption(tr("tts.speed_label", speed=f"{tts_speed:.1f}"))
            
            # Variables for video generation
            tts_workflow_key = None
            ref_audio_path = None
        
        # ================================================================
        # VoiceBox Mode UI
        # ================================================================
        elif tts_mode == "voicebox":
            vb_profiles = get_voicebox_profiles(config_manager.get_voicebox_endpoint())
            vb_config = tts_config.get("voicebox", {})
            saved_vb_voice = vb_config.get("voice", "")
            
            if not vb_profiles:
                st.error("No profiles found or failed to connect to VoiceBox API.")
                selected_voice = ""
            else:
                vb_options = [p["name"] for p in vb_profiles]
                vb_ids = [p["id"] for p in vb_profiles]
                
                default_vb_index = 0
                if saved_vb_voice in vb_ids:
                    default_vb_index = vb_ids.index(saved_vb_voice)
                elif saved_vb_voice in vb_options:
                    default_vb_index = vb_options.index(saved_vb_voice)
                    
                selected_voice_display = st.selectbox(
                    "VoiceBox Profile",
                    vb_options,
                    index=default_vb_index,
                    key="digital_tts_voicebox_profile"
                )
                selected_voice = vb_ids[vb_options.index(selected_voice_display)]
                
            tts_workflow_key = None
            ref_audio_path = None

        # ================================================================
        # fal.ai Mode UI
        # ================================================================
        elif tts_mode == "fal":
            fal_config = tts_config.get("fal", {})
            saved_fal_voice = fal_config.get("voice", "")

            selected_voice = st.text_input(
                "fal.ai Voice",
                value=saved_fal_voice,
                placeholder=(
                    "모델별 음성 ID (선택)" if get_language() == "ko_KR"
                    else ("模型对应的音色 ID（可选）" if get_language() == "zh_CN"
                          else "Model-specific voice id (optional)")
                ),
                help=(
                    "비워두면 모델 기본 음성을 사용합니다. 모델/엔드포인트는 설정에서 변경하세요."
                    if get_language() == "ko_KR"
                    else (
                        "留空则使用模型默认音色。模型/端点请在设置中修改。"
                        if get_language() == "zh_CN"
                        else "Leave blank to use the model default voice. Change the model/endpoint in Settings."
                    )
                ),
                key="digital_tts_fal_voice"
            )

            tts_workflow_key = None
            ref_audio_path = None

        # ================================================================
        # ElevenLabs Mode UI
        # ================================================================
        elif tts_mode == "elevenlabs":
            el_config = tts_config.get("elevenlabs", {})
            saved_el_voice = el_config.get("voice", "21m00Tcm4TlvDq8ikWAM")

            selected_voice = st.text_input(
                "ElevenLabs Voice ID",
                value=saved_el_voice,
                placeholder="21m00Tcm4TlvDq8ikWAM",
                help=(
                    "비워두면 설정의 기본 음성을 사용합니다. 모델/API 키는 설정에서 변경하세요."
                    if get_language() == "ko_KR"
                    else (
                        "留空则使用设置中的默认音色。模型/API Key 请在设置中修改。"
                        if get_language() == "zh_CN"
                        else "Leave blank to use the default voice from Settings. Change the model/API key in Settings."
                    )
                ),
                key="digital_tts_elevenlabs_voice"
            )

            tts_workflow_key = None
            ref_audio_path = None

        # ================================================================
        # ComfyUI Mode UI
        # ================================================================
        else:  # comfyui mode
            tts_workflow_key = "runninghub/tts_index2.json"  # fallback
            
            # Reference audio upload (optional, for voice cloning)
            ref_audio_file = st.file_uploader(
                tr("tts.ref_audio"),
                type=["mp3", "wav", "flac", "m4a", "aac", "ogg"],
                help=tr("tts.ref_audio_help"),
                key="digital_ref_audio_upload"
            )
            
            # Save uploaded ref_audio to temp file if provided
            ref_audio_path = None
            if ref_audio_file is not None:
                # Audio preview player (directly play uploaded file)
                st.audio(ref_audio_file)
                
                # Save to temp directory
                temp_dir = Path("temp")
                temp_dir.mkdir(exist_ok=True)
                ref_audio_path = temp_dir / f"ref_audio_{ref_audio_file.name}"
                with open(ref_audio_path, "wb") as f:
                    f.write(ref_audio_file.getbuffer())
            
            # Variables for video generation
            selected_voice = None
            tts_speed = None
        
        # ================================================================
        # TTS Preview (works for both modes)
        # ================================================================
        with st.expander(tr("tts.preview_title"), expanded=False):
            # Preview text input
            preview_text = st.text_input(
                tr("tts.preview_text"),
                value="안녕하세요. 첫번째 테스트 입니다.",
                placeholder=tr("tts.preview_text_placeholder"),
                key="digital_tts_preview_text"
            )
            
            # Preview button
            if st.button(tr("tts.preview_button"), key="gidital_preview_tts", use_container_width=True):
                with st.spinner(tr("tts.previewing")):
                    try:
                        # Build TTS params based on mode
                        tts_params = {
                            "text": preview_text,
                            "inference_mode": tts_mode
                        }
                        
                        if tts_mode == "local":
                            tts_params["voice"] = selected_voice
                            tts_params["speed"] = tts_speed
                        elif tts_mode in ("voicebox", "fal", "elevenlabs"):
                            tts_params["voice"] = selected_voice
                        else:  # comfyui
                            tts_params["workflow"] = tts_workflow_key
                            if ref_audio_path:
                                tts_params["ref_audio"] = str(ref_audio_path)
                        
                        audio_path = run_async(pixelle_video.tts(**tts_params))
                        
                        # Play the audio
                        if audio_path:
                            st.success(tr("tts.preview_success"))
                            if os.path.exists(audio_path):
                                st.audio(audio_path, format="audio/mp3")
                            elif audio_path.startswith('http'):
                                st.audio(audio_path)
                            else:
                                st.error("Failed to generate preview audio")
                            
                            # Show file path
                            st.caption(f"📁 {audio_path}")
                        else:
                            st.error("Failed to generate preview audio")
                    except Exception as e:
                        st.error(tr("tts.preview_failed", error=str(e)))
                        logger.exception(e)
    
    # Return all style configuration parameters
    return {
        "tts_inference_mode": tts_mode,
        "tts_voice": selected_voice if tts_mode in ["local", "voicebox", "fal", "elevenlabs"] else None,
        "tts_speed": tts_speed if tts_mode == "local" else None,
        "tts_workflow": tts_workflow_key if tts_mode == "comfyui" else None,
        "ref_audio": str(ref_audio_path) if ref_audio_path else None,
    }