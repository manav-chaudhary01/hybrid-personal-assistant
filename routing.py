from app_open import open_app
from searchAndOpen import search_and_open
from date_day_time import curr_date, curr_time
from local_llm import run_local_llm
from utils import is_internet_available
from open_ai import ask_groq
from open_webbrowser import search_web
from temperature import get_temperature
import time
from tts import speak


def routing(text, intent):
    internet = is_internet_available()
    
    if intent == "app_open":
        open_app(text)

    elif intent == "file_search_open":
        result = search_and_open()
        if result == "exit":
            return
        

    elif intent == "date_query":
        curr_date()
        time.sleep(1)
        return


    elif intent == "time_query":
        curr_time()
        time.sleep(1)
        return


    elif intent == "casual_conversation":
        if internet:
            ask_groq(text)
        else:
            run_local_llm(text)
        time.sleep(1)
        return


    elif intent == "information_query":
        if internet:
            ask_groq(text)
        else:
            run_local_llm(text)
        time.sleep(1)
        return
        

    elif intent == "web_search":
        if internet:
            search_web(text)
            time.sleep(1)
            return
        else:
            speak("Internet Connection is not available",2)
            return
        
    elif intent == "temperature_query":
        get_temperature()
        time.sleep(1)
        return