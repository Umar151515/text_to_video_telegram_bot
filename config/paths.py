from pathlib import Path


config_folder_path = Path("configs")
env_path = config_folder_path / ".env"
generation_settings_config_path = config_folder_path / "generation_settings_config.json"
image_generation_config_path = config_folder_path / "image_generation_config.json"
prompts_config_path = config_folder_path / "prompts_config.json"
text_generation_config_path = config_folder_path / "text_generation_config.json"

data_folder_path = Path("data")
image_folder_path = data_folder_path / "images"
user_data_path = data_folder_path / "users.pkl"

__all__ = [
    'config_folder_path', 
    'env_path', 
    'generation_settings_config_path', 
    'image_generation_config_path',
    'prompts_config_path', 
    'text_generation_config_path', 
    'data_folder_path', 
    'image_folder_path', 
    'user_data_path'
]