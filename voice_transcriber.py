import whisper
import os

# Explicitly set ffmpeg path (CRITICAL FOR WINDOWS)
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg-8.0.1-essentials_build\bin"

# Load Whisper model once
model = whisper.load_model("small")

def transcribe_voice(audio_path: str) -> str:
    """
    Transcribes audio files (.wav, .mp3, .mp4) to text
    """
    result = model.transcribe(audio_path)
    return result["text"]
