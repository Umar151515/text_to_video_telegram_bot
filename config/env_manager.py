import os

from dotenv import load_dotenv

from .paths import env_path


class EnvManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EnvManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_loaded'):
            self._loaded = False
            self.load()

    def load(self):
        if not os.path.exists(env_path):
            raise FileNotFoundError(f"Env file not found: {env_path}")
        load_dotenv(env_path)
        self._loaded = True

    def _ensure_loaded(self):
        if not self._loaded:
            raise RuntimeError("Environment variables not loaded. Call load() first")

    def has(self, key: str) -> bool:
        self._ensure_loaded()
        return os.getenv(key) is not None

    def get(self, key: str, default:str|None = None) -> str:
        self._ensure_loaded()
        value = os.getenv(key, default)
        if value is None:
            raise ValueError(f"Environment variable '{key}' not set and no default provided")
        return value
    
    def set(self, key: str, value: str):
        self._ensure_loaded()
        os.environ[key] = value
    
    def __getitem__(self, key: str) -> str:
        return self.get(key)

    def __setitem__(self, key: str, value: str):
        self.set(key, value)