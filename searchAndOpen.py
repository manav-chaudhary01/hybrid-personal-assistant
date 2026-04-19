import os
import subprocess
import re
import platform
import difflib
from load_models import recognizer
from tts import speak

# Folders to search in
SEARCH_PATHS = [
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Downloads")
]


def extract_filename(command: str) -> str:
    """
    Extract filename from voice command.
    """
    pattern = r"(?:named|file|document|called)\s+([A-Za-z0-9_\-\.]+)"
    matches = re.findall(pattern, command, re.IGNORECASE)

    if matches:
        return matches[-1].strip()

    # fallback cleanup
    command = command.lower()
    command = command.replace("open", "")
    command = command.replace("file", "")
    command = command.replace("document", "")
    return command.strip()


def best_match(filename, files_list):
    """
    Find closest match using fuzzy matching.
    """
    matches = difflib.get_close_matches(
        filename.lower(),
        [f.lower() for f in files_list],
        n=1,
        cutoff=0.75
    )
    return matches[0] if matches else None


def search_file(filename: str):
    """
    Search for file in predefined directories.
    """
    name_only, ext_input = os.path.splitext(filename.lower())
    has_ext = ext_input != ""

    for path in SEARCH_PATHS:
        for root, dirs, files in os.walk(path):

            # Exact match with extension
            if has_ext:
                for f in files:
                    if f.lower() == filename.lower():
                        return os.path.join(root, f)

            # Match without extension
            for f in files:
                fname, _ = os.path.splitext(f.lower())
                if fname == name_only:
                    return os.path.join(root, f)

            # Fuzzy match
            match = best_match(filename, files)
            if match:
                return os.path.join(root, match)

    return None


def open_file(filepath):
    """
    Open file cross-platform.
    """
    try:
        if platform.system() == "Windows":
            os.startfile(filepath)
        elif platform.system() == "Darwin":
            subprocess.run(["open", filepath])
        else:
            subprocess.run(["xdg-open", filepath])
    except Exception as e:
        print("Error opening file:", e)
        speak("I couldn't open the file.", 2)


def search_and_open():
    """
    Main function to handle voice-based file search and open.
    """
    speak("Please say the file name you want to open.", 2.5)

    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        print("Listening File Name....")
        command = recognizer.get_text()

        if not command:
            attempts += 1
            speak("I didn't catch that, please repeat.", 2)
            continue

        command = command.lower().replace(" dot ", ".")
        print("Command:", repr(command))

        if command in ["exit", "quit", "stop"]:
            speak("Exiting file search.", 1.5)
            return None

        filename = extract_filename(command)
        found = search_file(filename)

        if found:
            speak(f"Opening {os.path.basename(found)}", 2)
            open_file(found)
            return found

        else:
            speak("File not found. Try again.", 2)
            print("-- File not found:", filename, "--")
            attempts += 1

    speak("I couldn't find the file after multiple attempts.", 2)
    return None