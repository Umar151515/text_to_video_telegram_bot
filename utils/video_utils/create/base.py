from utils.text_utils.generator import generate_text
from config import ConfigManager
from core.models import Messages


async def create_video_from_text(text: str, text_model:str = None, text_selected_tool:str = None):
    slide_split_text = await generate_text(Messages([{"system": ConfigManager.prompts["slide_splitter"]}, {"system": text}]), 
                  text_model, text_selected_tool)
    slide_split = str.split(slide_split_text, "\n\n")

    print(slide_split)