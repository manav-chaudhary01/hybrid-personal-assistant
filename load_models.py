from speech_recognizer import SpeechRecognizer
from sbert import SBERTIntentDetector

recognizer = SpeechRecognizer(model_path="vosk-model-en-in-0.5", samplerate=44100)

detector = SBERTIntentDetector(model_path = "sentence-transformers/all-MiniLM-L6-v2")

print("--Models loaded successfully!--")
