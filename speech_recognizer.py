import json
import sounddevice as sd
import vosk
import queue
from rapidfuzz import process
import time
import numpy as np


class SpeechRecognizer:
    def __init__(self, model_path="vosk-model-en-in-0.5", samplerate=44100):

        print("Loading Vosk model...")
        self.model = vosk.Model(model_path)
        self.recognizer = vosk.KaldiRecognizer(self.model, samplerate)

        self.q = queue.Queue()
        self.samplerate = samplerate

        self.listening = True

        self.keywords = [
            "open", "spotify", "you", "youtube", "google", "chrome",
            "calculator", "notepad", "music", "mail", "photos", "exit"
        ]
        

    def correct_word(self, word):
        best = process.extractOne(word, self.keywords, score_cutoff=75)
        return best[0] if best else word

    def callback(self, indata, frames, time_info, status):
        if status:
            print(status)
        self.q.put(bytes(indata))

    def get_text(self, silence_threshold=500, silence_time=4.0):

        if not self.listening:
            return ""

        print("Speak now")

        text = ""
        silence_start = time.time()

        self.q.queue.clear()

        with sd.InputStream(
            samplerate=self.samplerate,
            channels=1,
            dtype='int16',
            callback=self.callback
        ):
            while True:

                sd.sleep(30)

                while not self.q.empty():

                    data = self.q.get()
                    audio = np.frombuffer(data, dtype=np.int16)
                    energy = np.sqrt(np.mean(audio ** 2))

                    if energy > silence_threshold:
                        silence_start = time.time()

                    if self.recognizer.AcceptWaveform(data):
                        result = json.loads(self.recognizer.Result())
                        part = result.get("text", "")
                        if part.strip():
                            text += " " + part.strip()

                silence_duration = time.time() - silence_start

                if silence_duration > silence_time and len(text) > 3:
                    break

                if not text and silence_duration > silence_time + 2:
                    break

        final = json.loads(self.recognizer.FinalResult())
        text += " " + final.get("text", "")

        text = text.strip()

        print(f"Final: {text if text else '[silence]'}")
        return text


    def pause_listening(self):
        self.listening = False

    def resume_listening(self):
        self.listening = True