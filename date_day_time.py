from datetime import datetime
from tts import speak

def curr_date():
    now = datetime.now()
    now2 = datetime.now()
    text = f"Today's date is {now.day} {now.strftime('%B')} {now.year} and day is {now2.strftime('%A')}"
    print(text)
    speak(text, 4)
    return text

def curr_time():
    now = datetime.now()
    text = f"The current time is {now.strftime('%I:%M %p')}"
    print(text)
    speak(text, 3)
    return text
