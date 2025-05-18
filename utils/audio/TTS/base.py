from __future__ import annotations

import asyncio

import numpy

from config import ConfigManager
from .coqui import text_to_speech_coqui


async def text_to_speech(text: str, speaker:str = None, selected_tool:str = None, language:str = None, output_path:str = None) -> numpy.ndarray:
    await asyncio.sleep(ConfigManager.generation_settings["response_delay"])
    generation_method = selected_tool or ConfigManager.text_to_speech.selected_tool
    
    if generation_method == "coqui":
        return await text_to_speech_coqui(text, speaker, language, output_path)
    else:
        raise TypeError(f"Such a TTS tool does not exist: {generation_method}")
    