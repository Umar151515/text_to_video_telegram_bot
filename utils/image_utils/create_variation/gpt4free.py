import base64
import re
from datetime import datetime

import g4f

from config import ConfigManager, image_folder_path


async def create_variation_gpt4free(prompt: str, image_path: str, model: str = ""):
    client = g4f.AsyncClient()

    response = await client.images.create_variation(
        prompt=prompt,
        image=open(image_path, "rb"),
        model=model or ConfigManager.image.get_selected_model("gpt4free"),
    )
    
    base64_data = response.data[0].b64_json
    image_data = base64.b64decode(base64_data)
    
    clean_prompt = re.sub(r'[^\w\s-]', '', prompt)[:25].strip().replace(' ', '_')
    time_part = datetime.now().strftime("%H%M%S")
    file_name = f"{clean_prompt}_{time_part}"
    
    with open(image_folder_path / f"{file_name}.png", "wb") as file:
        file.write(image_data)
    return file_name