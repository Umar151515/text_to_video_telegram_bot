import numpy
from typing import Callable, Awaitable, Any

from utils.text.generator import generate_text
from utils.image.generator import generate_image
from utils.text.processing import extract_parts_by_pipe
from utils.audio.TTS import text_to_speech
from config import ConfigManager
from core.models import Messages

import numpy as np
import cv2
import soundfile as sf
import subprocess
from io import BytesIO

def create_video(images: list[bytes], audio_clips: list[np.ndarray], sample_rate: int, fps: int = 30) -> None:
    """временное решение для создания видео из изображений и аудио"""
    decoded_images = []
    for img_bytes in images:
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Failed to decode image")
        decoded_images.append(img)
    
    if not decoded_images:
        raise ValueError("No images provided")
    
    img_height, img_width, _ = decoded_images[0].shape
    if any(img.shape != (img_height, img_width, 3) for img in decoded_images):
        raise ValueError("All images must have the same dimensions")
    
    video_writer = cv2.VideoWriter(
        'temp_video.mp4',
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (img_width, img_height)
    )
    
    for img, audio in zip(decoded_images, audio_clips):
        duration = len(audio) / sample_rate
        frame_count = int(duration * fps)
        for _ in range(frame_count):
            video_writer.write(img)
    
    video_writer.release()
    
    audio_data = np.concatenate(audio_clips, axis=0)
    
    if audio_data.dtype == np.float32:
        audio_data = (audio_data * 32767).astype(np.int16)
    
    with BytesIO() as audio_buffer:
        sf.write(audio_buffer, audio_data, sample_rate, format='WAV')
        audio_buffer.seek(0)
        with open('temp_audio.wav', 'wb') as f:
            f.write(audio_buffer.read())
    
    subprocess.run([
        'ffmpeg',
        '-y',
        '-i', 'temp_video.mp4',
        '-i', 'temp_audio.wav',
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        'final_output.mp4'
    ], check=True)

    subprocess.run(['rm', 'temp_video.mp4', 'temp_audio.wav'])


async def create_video_from_text(
    text: str,
    image_style: str = None,
    text_model: str = None,
    text_tool: str = None,
    image_model: str = None,
    image_tool: str = None,
    speaker: str = None,
    tts_tool: str = None,
    on_progress: Callable[[str, Any | None], Awaitable[None]] = None
):
    if on_progress: await on_progress("start", None)

    generated_text = await generate_text(
        Messages([
            {"role": "system", "content": ConfigManager.prompts["slide_splitter"].format(ConfigManager.text_to_speech.get_speakers(tts_tool))}, 
            {"role": "system", "content": text}
        ]), 
        text_model, text_tool
    )

    text_chunks = generated_text.split("\n\n")
    content_parts = text_chunks[:-1]
    default_image_style, default_speaker = [s.strip('[]') for s in extract_parts_by_pipe(text_chunks[-1].strip(), "!config")]

    if not speaker:
        speaker = default_speaker
    if speaker not in ConfigManager.text_to_speech.get_speakers(tts_tool):
        speaker = ConfigManager.text_to_speech.get_selected_speaker(tts_tool)
    if not image_style:
        image_style = default_image_style

    if on_progress: await on_progress("text_generated", {"image_style": image_style, "speaker": speaker, "generated_text": generated_text})

    images: list[bytes] = []
    audio_clips: list[numpy.ndarray] = []

    for content in content_parts:
        image_prompt = await generate_text(
            Messages([
                {"role": "system", "content": ConfigManager.prompts["image_generation"].format(image_style)}, 
                {"role": "system", "content": content}
            ]),
            text_model, text_tool
        )

        image = await generate_image(image_prompt, image_model, image_tool)
        images.append(image)

        audio_clips.append(await text_to_speech(content, speaker, tts_tool))

        if on_progress: 
            await on_progress(
                "slide_done", 
                {
                    "index": len(images),
                    "total": len(content_parts),
                    "image_prompt": image_prompt,
                    "content": content
                }
            )

    if on_progress: await on_progress("create_video", None)

    create_video(images, audio_clips, 22050)

    if on_progress: await on_progress("done", None)