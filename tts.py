import pyttsx3
import time

engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 180)
engine.setProperty('volume', 1.0)

# 🔥 GLOBAL CONTROL (set from main)
recognizer_ref = None


def set_recognizer(recognizer):
    global recognizer_ref
    recognizer_ref = recognizer


def speak(text, t=0):
    if not text:
        return

    if recognizer_ref:
        recognizer_ref.pause_listening()

    print("Assistant:", text, flush=True)

    engine.say(text)
    engine.runAndWait()

    if t > 0:
        time.sleep(t)

    if recognizer_ref:
        recognizer_ref.resume_listening()