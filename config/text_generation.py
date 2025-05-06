from .paths import text_generation_config_path
from .generation_config import GenerationConfig


class TextGeneration(GenerationConfig):
    config_path = text_generation_config_path