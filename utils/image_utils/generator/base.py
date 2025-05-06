import asyncio

from config import ConfigManager
from .gpt4free import generate_image_gpt4free


async def generate_image(prompt: str, model: str = "", selected_tool: str = "") -> str:
    await asyncio.sleep(ConfigManager.generation_settings["response_delay"])

    generation_method = selected_tool or ConfigManager.image.selected_tool
    
    if generation_method == "gpt4free":
        return await generate_image_gpt4free(prompt, model)
    else:
        raise ValueError(f"Такого типа генерации изображения не существует: {generation_method}")