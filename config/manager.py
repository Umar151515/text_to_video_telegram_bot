from .env_manager import EnvManager
from .generation_settings import GenerationSettings
from .prompts_manager import PromptsManager
from .text_generation import TextGeneration
from .image_generation import ImageGeneration
from .text_to_speech import TextToSpeech


class ConfigManager:
    env: EnvManager = EnvManager()
    generation_settings: GenerationSettings = GenerationSettings()
    prompts: PromptsManager = PromptsManager()
    text: TextGeneration = TextGeneration()
    image: ImageGeneration = ImageGeneration()
    text_to_speech: TextToSpeech = TextToSpeech()

    @classmethod
    def reload_all(cls):
        cls.env = EnvManager()
        cls.settings = GenerationSettings()
        cls.prompts = PromptsManager()
        cls.text = TextGeneration()
        cls.image = ImageGeneration()
        cls.text_to_speech = TextToSpeech()