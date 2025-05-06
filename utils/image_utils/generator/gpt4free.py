import base64
import re
from datetime import datetime

import g4f

from config import ConfigManager, image_folder_path


async def generate_image_gpt4free(prompt: str, model: str = "") -> str:
    client = g4f.AsyncClient()

    response = await client.images.generate(
        prompt=prompt,
        model=model or ConfigManager.image.get_selected_model("gpt4free"),
        response_format="b64_json"
    )
    
    base64_data = response.data[0].b64_json
    image_data = base64.b64decode(base64_data)
    
    clean_prompt = re.sub(r'[^\w\s-]', '', prompt)[:25].strip().replace(' ', '_')
    time_part = datetime.now().strftime("%H%M%S")
    file_name = f"{clean_prompt}_{time_part}"
    
    with open(image_folder_path / f"{file_name}.png", "wb") as file:
        file.write(image_data)
    return file_name