import base64
from io import BytesIO

import g4f
from PIL import Image

from config import ConfigManager


async def generate_image_gpt4free(prompt: str, model:str = None, output_path:str = None) -> bytes:
    try:
        client = g4f.AsyncClient()

        response = await client.images.generate(
            prompt=prompt,
            model=model or ConfigManager.image.get_selected_model("gpt4free"),
            response_format="b64_json"
        )
        
        if not response.data or not hasattr(response.data[0], 'b64_json'):
            raise RuntimeError("Unexpected API response format")
        
        base64_data = response.data[0].b64_json
        image_data = base64.b64decode(base64_data)
        
        if output_path:
            with Image.open(BytesIO(image_data)) as img:
                img.save(f"{output_path}.png", format="PNG")

        return image_data
        
    except Exception as e:
        raise RuntimeError(f"Failed to create image variation: {str(e)}")