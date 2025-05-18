import numpy
from io import BytesIO
from typing import Callable, Awaitable, Any

from utils.text.generator import generate_text
from utils.image.generator import generate_image
from utils.text.processing import extract_parts_by_pipe
from utils.audio.TTS import text_to_speech
from config import ConfigManager
from core.models import Messages
import cv2
import numpy as np
import subprocess
import soundfile as sf
import os

def create_slideshow(
    images: list[bytes],
    audio_clips: list[np.ndarray],
    audio_sample_rate: int,
    output_file: str = "output.mp4",
    fps: int = 30,
    transition_duration: float = 0.5
):
    if len(images) == 0 or len(audio_clips) == 0 or len(images) != len(audio_clips):
        raise ValueError("Images and audio clips must be non-empty and of equal length.")
    
    # Декодирование изображений
    images_np = []
    for img_bytes in images:
        img_np = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
        if img_np is None:
            raise ValueError("Failed to decode image.")
        images_np.append(img_np)
    
    # Проверка и выравнивание размеров изображений
    h, w = images_np[0].shape[:2]
    for i in range(len(images_np)):
        if images_np[i].shape[:2] != (h, w):
            images_np[i] = cv2.resize(images_np[i], (w, h))
    
    # Создание временного видеофайла
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter('temp_video.mp4', fourcc, fps, (w, h))
    if not video_writer.isOpened():
        raise RuntimeError("Failed to create video writer.")
    
    transition_frames = int(transition_duration * fps)
    
    # Генерация кадров с переходами
    for i in range(len(images_np)):
        current_img = images_np[i]
        audio_duration = len(audio_clips[i]) / audio_sample_rate
        total_frames = int(round(audio_duration * fps))
        
        # Распределение кадров между основным показом и переходом
        if i < len(images_np) - 1:
            trans_frames = min(transition_frames, total_frames)
            main_frames = total_frames - trans_frames
        else:
            trans_frames = 0
            main_frames = total_frames
        
        # Основные кадры слайда
        for _ in range(main_frames):
            video_writer.write(current_img)
        
        # Кадры перехода
        if trans_frames > 0 and i < len(images_np) - 1:
            next_img = images_np[i+1]
            for t in range(trans_frames):
                alpha = t / trans_frames
                blended = cv2.addWeighted(current_img, 1-alpha, next_img, alpha, 0)
                video_writer.write(blended)
    
    video_writer.release()
    
    # Создание временной аудиодорожки
    combined_audio = np.concatenate(audio_clips, axis=0)
    sf.write('temp_audio.wav', combined_audio, audio_sample_rate)
    
    # Объединение аудио и видео через ffmpeg
    cmd = [
        'ffmpeg', '-y',
        '-i', 'temp_video.mp4',
        '-i', 'temp_audio.wav',
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        output_file
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg error: {e.stderr.decode()}") from e
    finally:
        if os.path.exists('temp_video.mp4'):
            os.remove('temp_video.mp4')
        if os.path.exists('temp_audio.wav'):
            os.remove('temp_audio.wav')



async def create_video_from_text(
    text: str,
    image_style: str = None,
    text_model: str = None,
    text_tool: str = None,
    image_model: str = None,
    image_tool: str = None,
    speaker: str = None,
    tts_tool: str = None,
    number_slides: int = None,
    on_progress: Callable[[str, Any | None], Awaitable[None]] = None
):
    if on_progress: await on_progress("start", None)

    generated_text = await generate_text(
        Messages([
            {"role": "system", "content": 
                ConfigManager.prompts["slide_splitter"].format(
                    number_slides if number_slides else "", 
                    number_slides if number_slides else "", 
                    ConfigManager.text_to_speech.get_speakers(tts_tool)
                )
            },
            {"role": "system", "content": text},
            {"role": "system", "content": ConfigManager.prompts["ultra_compliant_response"]},
        ]), 
        text_model, text_tool
    )
    no_generate_text = extract_parts_by_pipe(generated_text, "!NO_GENERATE")
    if no_generate_text:
        raise RuntimeError(f"Generation text failed: {no_generate_text[0]}")

    text_chunks = generated_text.split("\n\n")
    text_chunks = [t.strip() for t in text_chunks]
    content_parts = text_chunks[:-1]
    default_image_style, default_speaker, language = extract_parts_by_pipe(text_chunks[-1].strip(), "!config")

    if not content_parts:
        raise ValueError("No content parts found in the generated text.")
    if default_speaker not in ConfigManager.text_to_speech.get_speakers(tts_tool):
        default_speaker = ConfigManager.text_to_speech.get_selected_speaker(tts_tool)
    if not speaker:
        speaker = default_speaker
    if not image_style:
        image_style = default_image_style

    if on_progress: await on_progress("text_generated", {"image_style": image_style, "speaker": speaker, "generated_text": generated_text, "language": language, "number_slides": len(content_parts)})

    images: list[bytes] = []
    audio_clips: list[numpy.ndarray] = []

    for i, content in enumerate(content_parts):
        modified_content_parts = content_parts.copy()
        modified_content_parts[i] = f"|{content}|"

        image_prompt = await generate_text(
            Messages([
                {"role": "system", "content": ConfigManager.prompts["image_generation"].format(image_style)}, 
                {"role": "system", "content": str(modified_content_parts)},
            ]),
            text_model, text_tool
        )
        no_generate_prompt = extract_parts_by_pipe(image_prompt, "!NO_GENERATE")
        if no_generate_prompt:
            raise RuntimeError(f"Generation prompt failed: {no_generate_prompt}")

        image = await generate_image(image_prompt, image_model, image_tool)
        images.append(image)

        audio_clips.append(await text_to_speech(content, speaker, tts_tool, language))

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

    create_slideshow(images, audio_clips, 22050)

    if on_progress: await on_progress("done", None)