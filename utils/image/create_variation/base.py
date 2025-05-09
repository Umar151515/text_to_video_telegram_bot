import asyncio

from config import ConfigManager
from .gpt4free import create_variation_gpt4free


async def create_variation(prompt: str, input_image: str | bytes, model:str = None, selected_tool:str = None, output_path:str = None) -> bytes:
    await asyncio.sleep(ConfigManager.generation_settings["response_delay"])
    generation_method = selected_tool or ConfigManager.image.selected_tool
    
    if generation_method == "gpt4free":
        return await create_variation_gpt4free(prompt, input_image, model, output_path)
    else:
        raise ValueError(f"Такого типа генерации изображения не существует: {generation_method}")