import torch
import numpy
import langid
import scipy.io.wavfile
from TTS.api import TTS

from config import ConfigManager


async def text_to_speech_coqui(text: str, speaker:str = None, output_path:str = None, model:str = None) -> numpy.ndarray:
    device = "cuda" if torch.cuda.is_available() else "cpu"

    if not model:
        model = ConfigManager.text_to_speech.get_selected_model("coqui")
    if not speaker:
        speaker = ConfigManager.text_to_speech.get_selected_speaker("coqui", model)

    tts = TTS(model).to(device)
    language, _ = langid.classify(text)

    if ".wav" in speaker:
        audio = tts.tts(text=text, speaker_wav=speaker, language="ru")
    else:
        audio = tts.tts(text=text, speaker=speaker, language="ru")

    audio = numpy.array(audio, dtype=numpy.float32)

    if output_path:
        sample_rate = getattr(tts.synthesizer, "sample_rate", 22050)
        scipy.io.wavfile.write(output_path, sample_rate, audio)

    return audio