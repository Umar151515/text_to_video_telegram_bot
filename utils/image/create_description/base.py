from __future__ import annotations

import asyncio

from config import ConfigManager

from .gpt4free import create_description_image_gpt4free
from .ollama import create_description_image_ollama


async def create_description_image(image: str | bytes, selected_tool:str = "") -> str:
    await asyncio.sleep(ConfigManager.generation_settings["response_delay"])
    generation_method = selected_tool or ConfigManager.text.selected_tool
    
    if generation_method == "ollama":
        return await create_description_image_ollama(image)
    elif generation_method == "gpt4free":
        return await create_description_image_gpt4free(image)
    else:
        raise TypeError(f"Such a text generation tool does not exist: {generation_method}")
    