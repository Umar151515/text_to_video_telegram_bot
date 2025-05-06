from __future__ import annotations

import asyncio

import ollama

from config import ConfigManager

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.models import Image


async def create_description_image_ollama(image: Image) -> str:
    response = await asyncio.to_thread(
        ollama.chat,
        model=ConfigManager.text.get_tool_config("ollama")["models_supporting_image"][0],
        messages=[{"role": "system", "content": ConfigManager.prompts["image_description_guide"], "images": [image.file_path]}],
        stream=False,
        options={
            "temperature": ConfigManager.generation_settings["temperature"],
            "num_predict": ConfigManager.generation_settings["max_tokens"],
            "repeat_penalty": ConfigManager.generation_settings["repeat_penalty"],
            "stop": ConfigManager.generation_settings["stop_words"],
        }
    )

    return response['message']['content']