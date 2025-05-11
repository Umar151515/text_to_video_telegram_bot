from __future__ import annotations

import asyncio
from typing import Callable

from config import ConfigManager

from .gpt4free import create_description_image_gpt4free
from .ollama import create_description_image_ollama


async def create_description_image(
        image: str | bytes, 
        selected_tool:str = "", 
        max_attempts:int = 3
    ) -> bytes:

    generation_method = selected_tool or ConfigManager.image.selected_tool
    methods: dict[str, Callable[[str | bytes], str]] = {
        "gpt4free": create_description_image_gpt4free,
        "ollama": create_description_image_ollama
    }
    
    for attempt in range(max_attempts):
        await asyncio.sleep(ConfigManager.generation_settings["response_delay"])

        try:
            method = methods.get(generation_method, None)
            if method is None:
                raise TypeError(f"Such a create description tool does not exist: {generation_method}")
            return await method(image)
        except Exception as e:
            if attempt == max_attempts - 1:
                return f"Failed to create description after {max_attempts} attempts. Error: {str(e)}"
                
    return "Unexpected error in create description" 