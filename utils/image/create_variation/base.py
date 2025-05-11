import asyncio
from typing import Callable

from config import ConfigManager
from .gpt4free import create_variation_gpt4free


async def create_variation(
        prompt: str, 
        input_image: str | bytes, 
        model:str = None, 
        selected_tool:str = None, 
        output_path:str = None, 
        max_attempts:int = 3
    ) -> bytes:

    generation_method = selected_tool or ConfigManager.image.selected_tool
    methods: dict[str, Callable[[str, str | bytes, str, str], str]] = {
        "gpt4free": create_variation_gpt4free
    }
    
    for attempt in range(max_attempts):
        await asyncio.sleep(ConfigManager.generation_settings["response_delay"])

        try:
            method = methods.get(generation_method, None)
            if method is None:
                raise TypeError(f"Such a create variation image tool does not exist: {generation_method}")
            return await method(prompt, model, output_path)
        except Exception as e:
            if attempt == max_attempts - 1:
                return f"Failed to create variation image after {max_attempts} attempts. Error: {str(e)}"
                
    return "Unexpected error in create variation image"