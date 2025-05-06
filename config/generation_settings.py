import json, os
from typing import Any

from .paths import generation_settings_config_path


class GenerationSettings:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GenerationSettings, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'config'):
            self.config: dict[str, Any] = None
            self.load()

    def _ensure_loaded(self):
        if self.config is None:
            raise RuntimeError("Generation settings not loaded. Call load() first")

    def load(self):
        if not os.path.exists(generation_settings_config_path):
            raise FileNotFoundError(f"Generation settings file not found: {generation_settings_config_path}")
        with open(generation_settings_config_path, "r", encoding="utf-8") as config_file:
            self.config = json.load(config_file)

    def has(self, key: str) -> bool:
        self._ensure_loaded()
        return key in self.config

    def get(self, key: str, default:str|None = None) -> Any:
        self._ensure_loaded()
        value = self.config.get(key, default)
        if value is None:
            raise ValueError(f"Generation settings '{key}' not set and no default provided")
        return value
    
    def set(self, key: str, value: Any) -> None:
        self._ensure_loaded()
        self.config[key] = value
        with open(generation_settings_config_path, "w", encoding="utf-8") as config_file:
            json.dump(self.config, config_file, ensure_ascii=False, indent=4)
    
    def __getitem__(self, key: str) -> Any:
        return self.get(key)

    def __setitem__(self, key: str, value: Any):
        self.set(key, value)