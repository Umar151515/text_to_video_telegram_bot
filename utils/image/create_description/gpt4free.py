from __future__ import annotations

from io import BytesIO

import g4f

from config import ConfigManager


async def create_description_image_gpt4free(image: str | bytes) -> str:
    client = g4f.AsyncClient()

    if isinstance(image, str):
        image_file = open(image, "rb")
    elif isinstance(image, bytes):
        image_file = BytesIO(image)
    else:
        raise ValueError("image must be either str (path) or bytes")
    
    try:
        response = await client.chat.completions.create(
            messages=[{"role": "user", "content": ConfigManager.prompts["image_description_guide"]}],
            temperature=ConfigManager.generation_settings["temperature"],
            max_tokens=ConfigManager.generation_settings["max_tokens"],
            frequency_penalty=ConfigManager.generation_settings["repeat_penalty"],
            stop=ConfigManager.generation_settings["stop_words"],
            web_search=False,
            image=image_file
        )

        return response.choices[0].message.content
    
    except Exception as e:
        print(f"Unexpected error during image description: {e}")
        return None
    finally:
        if isinstance(image, str):
            image_file.close()