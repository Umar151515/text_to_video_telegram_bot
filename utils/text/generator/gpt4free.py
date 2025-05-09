import g4f

from config import ConfigManager
from core.models import Messages


async def generate_text_gpt4free(messages: Messages, model: str = None, web_search: bool = False) -> str:
    client = g4f.AsyncClient()

    if web_search:
        query_messages = messages.get_messages() 
        query_messages.add_message("system", ConfigManager.prompts["context_internet"])
        query = await generate_text_gpt4free(query_messages, model)
        tool_calls = [{
            "type": "function",
            "function": {
                "name": "search_tool",
                "arguments": {
                    "query": query,
                    "add_text": True
                }
            }
        }]
    else:
        tool_calls = None

    response = await client.chat.completions.create(
        model=model if model is not None else ConfigManager.text.get_selected_model("gpt4free"),
        messages=messages.messages,
        temperature=ConfigManager.generation_settings["temperature"],
        max_tokens=ConfigManager.generation_settings["max_tokens"],
        frequency_penalty=ConfigManager.generation_settings["repeat_penalty"],
        stop=ConfigManager.generation_settings["stop_words"],
        tool_calls=tool_calls,
        web_search=False
    )

    return response.choices[0].message.content