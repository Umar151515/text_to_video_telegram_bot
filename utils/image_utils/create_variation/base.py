import asyncio

from config import ConfigManager
from .gpt4free import create_variation_gpt4free


async def create_variation(prompt: str, image_path: str, model: str = "", selected_tool: str = "") -> str:
    await asyncio.sleep(ConfigManager.generation_settings["response_delay"])
    generation_method = selected_tool or ConfigManager.image.selected_tool
    
    if generation_method == "gpt4free":
        return await create_variation_gpt4free(prompt, image_path, model)
    else:
        raise ValueError(f"Такого типа генерации изображения не существует: {generation_method}")