import sys
from faster_whisper import WhisperModel
try:
    print("Loading model...")
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    print("Model loaded.")
    # We need a dummy audio file
    pass
except Exception as e:
    print("Error:", e)
