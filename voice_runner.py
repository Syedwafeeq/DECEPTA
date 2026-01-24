from voice_transcriber import transcribe_voice
from module3_runner import run_module_3_from_text

def run_voice_analysis(audio_path: str):
    """
    Full voice phishing pipeline:
    Voice -> Text -> NLP + Behavioral -> Decision
    """
    transcript = transcribe_voice(audio_path)
    result = run_module_3_from_text(transcript)
    return transcript, result
