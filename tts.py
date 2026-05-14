try:
    import win32com.client
    speaker = win32com.client.Dispatch('SAPI.SpVoice')
    USE_WIN32COM = True
    print("Using win32com for TTS")
except ImportError:
    import pyttsx3
    speaker = pyttsx3.init('sapi5')
    speaker.setProperty('rate', 180)
    speaker.setProperty('volume', 1.0)
    voices = speaker.getProperty('voices')
    if len(voices) > 1:
        speaker.setProperty('voice', voices[1].id)
        print(f"Set voice to: {voices[1].name}")
    USE_WIN32COM = False
    print("Using pyttsx3 for TTS")

import time

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

    if USE_WIN32COM:
        speaker.Speak(text)
    else:
        speaker.say(text)
        speaker.runAndWait()

    if t > 0:
        time.sleep(t)

    if recognizer_ref:
        recognizer_ref.resume_listening()