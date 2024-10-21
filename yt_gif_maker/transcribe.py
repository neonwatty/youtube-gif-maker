from yt_gif_maker.audio_extractor import extract_audio
import whisper_timestamped as whisper
from typing import Tuple
import itertools
import os

os.environ["TOKENIZERS_PARALLELISM"] = "true"


avaliable_models = ["tiny", "base", "small", "medium", "large-v3", "turbo"]


def transcribe(video_file_path: str, model: str = "tiny", device: str = "cpu") -> Tuple[str, dict]:
    assert model in avaliable_models, f"input model '{model}' not a member of available models = {avaliable_models}"
    audio_file_path = video_file_path.replace("mp4", "mp3")
    extract_audio(video_file_path, audio_file_path)
    if model == "turbo":
        model = "openai/whisper-large-v3-turbo"
    model = whisper.load_model(model, device="cpu")
    process_output = whisper.transcribe(model, audio_file_path, verbose=False)
    transcript = process_output["text"].strip()
    timestamped_transcript = process_output["segments"]
    timestamped_words = [timestamped_transcript[i]["words"] for i in range(len(timestamped_transcript))]
    timestamped_words = list(itertools.chain.from_iterable(timestamped_words))
    return transcript, timestamped_words
