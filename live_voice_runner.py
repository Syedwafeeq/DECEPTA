import sounddevice as sd
import numpy as np
import whisper
import time

from module3_runner import run_module_3_from_text
SAMPLE_RATE = 16000
CHUNK_SECONDS = 8
MODEL_SIZE = "base"

sd.default.device = 1

print("[INFO] Loading Whisper model...")
model = whisper.load_model(MODEL_SIZE)
print("[INFO] Whisper model loaded.")

def live_vishing_detection():
    print("\nLIVE VISHING DETECTION STARTED")
    print("Listening to call audio (speaker).")
    print("Press Ctrl+C to stop.\n")

    transcript_so_far = ""

    try:
        while True:
            print("⏳ Listening...")

            audio = sd.rec(
                int(CHUNK_SECONDS * SAMPLE_RATE),
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype="float32"
            )
            sd.wait()
            audio = audio.flatten()
            max_amp = np.max(np.abs(audio))
            print(f"[DEBUG] Audio amplitude: {max_amp:.4f}")
            if max_amp < 0.005:
                print("[INFO] Silence detected, skipping...")
                continue
            result = model.transcribe(
                audio,
                fp16=False,
                language="en",
                condition_on_previous_text=True
            )

            chunk_text = result.get("text", "").strip()

            if chunk_text:
                transcript_so_far += " " + chunk_text

                print("\n📝 LIVE TRANSCRIPT:")
                print(transcript_so_far.strip())
                analysis = run_module_3_from_text(transcript_so_far)
                decision = analysis["decision_engine"]["decision"]
                risk = analysis["decision_engine"]["final_risk_score"]

                print("\n⚠️ CURRENT DECISION:", decision)
                print("📊 RISK SCORE:", risk)

                if decision == "BLOCK":
                    print("\n🚨 PHISHING DETECTED — TERMINATE CALL 🚨")
                    break

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n🛑 Live detection stopped by user.")


if __name__ == "__main__":
    live_vishing_detection()
