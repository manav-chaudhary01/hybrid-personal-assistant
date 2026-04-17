# tts.py
import pyttsx3
import threading
import queue
import time

engine = pyttsx3.init()
engine.setProperty('rate', 180)
time.sleep(1)
engine.say("")
engine.runAndWait()

speech_queue = queue.Queue()

def speech_worker():
    while True:
        text = speech_queue.get()
        if text is None:
            break
        engine.say(text)
        engine.runAndWait()
        print(text, flush=True)
        speech_queue.task_done()

threading.Thread(target=speech_worker, daemon=True).start()

def speak(text, t = 1.5):
    if text:
        speech_queue.put(text)

    time.sleep(t)

def speak_async(text):
    speak(text)
