import asyncio, re

from core.models import Messages
from config import ConfigManager
from .ollama import generate_text_ollama
from .gpt4free import generate_text_gpt4free
from .openrouter import generate_text_openrouter


async def generate_text(messages: Messages, model:str = None, selected_tool:str = None, web_search:bool = False) -> str:
    await asyncio.sleep(ConfigManager.generation_settings["response_delay"])
    generation_method = selected_tool or ConfigManager.text.selected_tool
    
    if generation_method == "ollama":
        message = await generate_text_ollama(messages, model, web_search)
    elif generation_method == "gpt4free":
        message = await generate_text_gpt4free(messages, model, web_search)
    elif generation_method == "openrouter":
        message = await generate_text_openrouter(messages, model)
    else:
        raise TypeError(f"Такого типа генерации текста не существует: {generation_method}")
    
    message = re.sub(r'<think>.*?</think>', '', message, flags=re.DOTALL).strip()
    max_retries = 3
    for _ in range(max_retries):
        if not message:
            message = await generate_text(messages, model, selected_tool)
        else:
            break
    return message