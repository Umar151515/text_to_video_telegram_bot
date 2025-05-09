import numpy

from utils.text.generator import generate_text
from utils.image.generator import generate_image
from utils.text.processing import extract_parts_by_pipe
from utils.audio.TTS import text_to_speech
from config import ConfigManager
from core.models import Messages


async def create_video_from_text(
    text: str,
    text_model: str = None,
    text_tool: str = None,
    image_model: str = None,
    image_tool: str = None,
    speaker: str = None,
    tts_tool: str = None
):
    generated_text = await generate_text(
        Messages([
            {"role": "system", "content": ConfigManager.prompts["slide_splitter"].format(ConfigManager.text_to_speech.get_speakers(tts_tool))}, 
            {"role": "system", "content": text}
        ]), 
        text_model, text_tool
    )

    text_chunks = generated_text.split("\n\n")
    content_parts = text_chunks[0:-1]
    image_style, speaker = [s.strip('[]') for s in extract_parts_by_pipe(text_chunks[-1].strip(), "!config")]

    images: list[bytes] = []
    audio_clips: list[numpy.ndarray] = []

    for content in content_parts:
        images.append(
            await generate_image(
                await generate_text(
                    Messages([
                        {"role": "system", "content": ConfigManager.prompts["image_generation"].format(image_style)}, 
                        {"role": "system", "content": content}
                    ]), 
                    text_model, text_tool
                ),
                image_model, image_tool
            )
        )
        audio_clips.append(await text_to_speech(content, speaker, tts_tool))

    print(generated_text, content_parts, image_style, speaker, sep="\n\n")