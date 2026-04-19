from load_models import recognizer, detector
from routing import routing
from temperature import startup_temp_fetch
import time
from tts import speak, set_recognizer

set_recognizer(recognizer)


startup_temp_fetch() 
speak("Hello! I am ready to assist you.",3)


while True:

    speak("Listening",1.5)
    print(" ")


    text = recognizer.get_text()

    if not text.strip():
        speak("No input detected. Listening again...", 4)
        continue

    speak(f"You said: {text}",2)

    intent = detector.detect_intent(text)
    print(f"Detected intent: {intent}")

    if intent == "exit_program":
        speak("Closing the program. Goodbye!",1.5)
        time.sleep(1)
        break

    routing(text, intent)
