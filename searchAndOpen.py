import os
import subprocess
import re
from load_models import recognizer
from tts import speak
import time

SEARCH_PATHS = [
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Downloads")
]

def extract_filename(command: str) -> str:
    pattern = r"(?:named|file|document|called)\s+([A-Za-z0-9_\-\.]+)"
    matches = re.findall(pattern, command, re.IGNORECASE)
    if matches:
        return matches[-1].strip()
    return command.strip()

def best_match(filename, files_list):
    import difflib
    matches = difflib.get_close_matches(
        filename.lower(), [f.lower() for f in files_list], n=1, cutoff=0.6
    )
    return matches[0] if matches else None

def search_file(filename: str):
    name_only, ext_input = os.path.splitext(filename.lower())
    has_ext = ext_input != ""

    for path in SEARCH_PATHS:
        for root, dirs, files in os.walk(path):
            if has_ext and filename.lower() in [f.lower() for f in files]:
                return os.path.join(root, filename)
            for f in files:
                fname, _ = os.path.splitext(f.lower())
                if fname == name_only:
                    return os.path.join(root, f)
            match = best_match(filename, files)
            if match:
                return os.path.join(root, match)
    return None

def search_and_open():
    speak("Please say the file name you want to open.",2.5)
    
    while True:
        print("Listening File Name....")
        command = recognizer.get_text()
        if not command:
            continue
        command = command.lower().replace(" dot ", ".")


        print("Command:", repr(command))

        if command.lower() in ["exit", "quit", "stop"]:
            speak("Exiting file search.",1.5)
            return

        filename = extract_filename(command)
        found = search_file(filename)

        if found:
            speak(f"Opening {os.path.basename(found)}",5)
            subprocess.run(["open", found])
            return found
        else:
            speak("Sorry, I could not find that file. Please try again.",4)
            print("--File not found:", filename,"--")
