# Copyright (C) 2025 AIDC-AI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

"""Shared output-language directive for generation prompts.

Forces the LLM to write narration/title text in the UI's language instead of
guessing from the (often short) topic input.
"""

from typing import Optional

# Locale code (or short code) -> human language name used in prompts.
LANGUAGE_NAMES = {
    "ko_KR": "Korean (한국어)", "ko": "Korean (한국어)",
    "en_US": "English", "en": "English",
    "zh_CN": "Chinese (简体中文)", "zh": "Chinese (简体中文)",
    "zh_TW": "Traditional Chinese (繁體中文)",
    "ja_JP": "Japanese (日本語)", "ja": "Japanese (日本語)",
    "es_ES": "Spanish", "fr_FR": "French", "de_DE": "German",
}


def language_directive(language: Optional[str]) -> str:
    """Return a high-priority output-language instruction, or '' when unknown."""
    if not language:
        return ""
    name = LANGUAGE_NAMES.get(language) or LANGUAGE_NAMES.get(language.split("_")[0]) or language
    return (
        "# OUTPUT LANGUAGE (HIGHEST PRIORITY)\n"
        f"You MUST write ALL output text in {name}. This requirement OVERRIDES any "
        "language inferred from the input topic/content. Even if the input is in another "
        f"language, the output must be in {name}. Do not mix languages.\n\n"
    )
