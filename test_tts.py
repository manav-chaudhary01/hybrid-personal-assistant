import pyttsx3

engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 180)
engine.setProperty('volume', 1.0)

engine.say("If you hear this, TTS is working")
engine.runAndWait()