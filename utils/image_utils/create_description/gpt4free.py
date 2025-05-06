from __future__ import annotations

import g4f

from config import ConfigManager

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.models import Image


async def create_description_image_gpt4free(image: Image) -> str:
    client = g4f.AsyncClient()

    response = await client.chat.completions.create(
        messages=[{"role": "user", "content": ConfigManager.prompts["image_description_guide"]}],
        temperature=ConfigManager.generation_settings["temperature"],
        max_tokens=ConfigManager.generation_settings["max_tokens"],
        frequency_penalty=ConfigManager.generation_settings["repeat_penalty"],
        stop=ConfigManager.generation_settings["stop_words"],
        web_search=False,
        image=open(image.file_path, "rb")
    )

    return response.choices[0].message.content