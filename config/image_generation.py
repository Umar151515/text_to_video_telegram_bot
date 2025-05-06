from .paths import image_generation_config_path
from .generation_config import GenerationConfig


class ImageGeneration(GenerationConfig):
    config_path = image_generation_config_path