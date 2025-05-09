import base64
from io import BytesIO

import g4f
from PIL import Image

from config import ConfigManager


async def create_variation_gpt4free(prompt: str, input_image: str | bytes, model:str = None, output_path:str = None) -> bytes:
    client = g4f.AsyncClient()

    if isinstance(input_image, str):
        image_file = open(input_image, "rb")
    elif isinstance(input_image, bytes):
        image_file = BytesIO(input_image)
    else:
        raise ValueError("input_image must be either str (path) or bytes")

    try:
        response = await client.images.create_variation(
            prompt=prompt,
            image=image_file,
            model=model or ConfigManager.image.get_selected_model("gpt4free"),
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
    finally:
        if isinstance(input_image, str):
            image_file.close()