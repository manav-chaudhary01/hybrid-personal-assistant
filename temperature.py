import requests
from tts import speak
import os
import json
from datetime import datetime

CACHE_FILE = "last_temperature.json"


def get_my_location():
    try:
        r = requests.get("https://ipinfo.io/json", timeout=3)
        data = r.json()

        loc = data.get("loc", "")   # latitude, longitude
        if "," in loc:
            lat, lon = loc.split(",")
            return data.get("city"), float(lat), float(lon)

        return None, None, None

    except:
        return None, None, None


def fetch_temperature(lat, lon):
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current_weather=true"
        )

        r = requests.get(url, timeout=4).json()
        temp = r["current_weather"]["temperature"]
        return f"{temp}°C"
    except:
        return None
    

def startup_temp_fetch():
    city, lat, lon = get_my_location()
    if city and lat and lon:
        temperature = fetch_temperature(lat, lon)
        if temperature:
            save_cache(city, temperature)


def save_cache(city, temperature):
    cache = {
        "city": city,
        "temperature": temperature,
        "time": datetime.now().strftime("%I:%M %p")
    }
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return None, None, None

    try:
        with open(CACHE_FILE, "r") as f:
            data = json.load(f)
            return data.get("city"), data.get("temperature"), data.get("time")
    except:
        return None, None, None


def get_temperature():

    city, lat, lon = get_my_location()

    if city and lat and lon:
        temperature = fetch_temperature(lat, lon)
        if temperature:
            save_cache(city, temperature)
            text = f"The temperature in {city} is {temperature}"
            speak(text,4.5)
            return text

    cached_city, cached_temp, cached_time = load_cache()
    if cached_city and cached_temp:
        text = f"Last known temperature in {cached_city} was {cached_temp} at {cached_time}"
        speak(text,5.5)
        return text

    text = "Sorry, the weather service is temporarily unavailable"
    speak(text,4)
    return text