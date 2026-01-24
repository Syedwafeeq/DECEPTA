import whisper
import os

#explicitly set ffmpeg path (CRITICAL FOR WINDOWS)
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg-8.0.1-essentials_build\bin"
model = whisper.load_model("small")

def transcribe_voice(audio_path: str) -> str:
    result = model.transcribe(audio_path)
    return result["text"]
