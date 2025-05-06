import json, os

from .paths import prompts_config_path


class PromptsManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PromptsManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'config'):
            self.config: dict[str, str] = None
            self.load()

    def _ensure_loaded(cls):
        if cls.config is None:
            raise RuntimeError("Prompts config not loaded. Call load_prompts_config() first")

    def load(cls):
        if not os.path.exists(prompts_config_path):
            raise FileNotFoundError(f"Prompts config file not found: {prompts_config_path}")
        with open(prompts_config_path, "r", encoding="utf-8") as config_file:
            cls.config = json.load(config_file)

    def has(cls, key: str) -> bool:
        cls._ensure_loaded()
        return key in cls.config

    def get(cls, key: str, default:str|None = None) -> str:
        cls._ensure_loaded()
        value = cls.config.get(key, default)
        if value is None:
            raise ValueError(f"Prompts config '{key}' not set and no default provided")
        return value
    
    def set(cls, key: str, value: str) -> None:
        cls._ensure_loaded()
        cls.config[key] = value
        with open(prompts_config_path, "w", encoding="utf-8") as config_file:
            json.dump(cls.config, config_file, ensure_ascii=False, indent=4)
    
    def __getitem__(self, key: str) -> str:
        return self.get(key)

    def __setitem__(self, key: str, value: str):
        self.set(key, value)