import asyncio

import ollama

from config import ConfigManager
from core.models import Messages
from ..search import duckduckgo


async def generate_text_ollama(messages: Messages, model:str = "", web_search:bool = False) -> str:
    if web_search:
        query_messages = messages.get_messages()
        query_messages.add_message("system", ConfigManager.prompts["search_query_generation"])
        query = await generate_text_ollama(query_messages, model)
        search_results = await duckduckgo(query, add_text=True)
        if search_results:
            messages.add_message("system", f"{ConfigManager.prompts['context_internet']}{search_results}")
    response = await asyncio.to_thread(
        ollama.chat,
        model=model or ConfigManager.text.get_selected_model("ollama"),
        messages=messages.messages,
        stream=False,
        options={
            "temperature": ConfigManager.generation_settings["temperature"],
            "num_predict": ConfigManager.generation_settings["max_tokens"],
            "repeat_penalty": ConfigManager.generation_settings["repeat_penalty"],
            "stop": ConfigManager.generation_settings["stop_words"],
        }
    )
    return response['message']['content']