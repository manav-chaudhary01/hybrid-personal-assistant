import subprocess
import platform
import os
from tts import speak
from rapidfuzz import process


def open_app(query: str):
    query = query.lower()

    # --- NORMALIZATION ---
    query = query.replace("vs code", "virtual studio code")
    query = query.replace("vscode", "virtual studio code")
    query = query.replace("intellij", "intellij idea ce")
    query = query.replace("code", "virtual studio code")

    # --- SUPPORTED APPS ---
    apps = [
        "chrome",
        "virtual studio code",
        "spotify",
        "notepad",
        "calculator",
        "camera",
        "intellij idea ce",
        "whatsapp"
    ]

    match = process.extractOne(query, apps, score_cutoff=60)
    app_name = match[0] if match else None

    if not app_name:
        speak("Sorry, I could not find that app.", 2)
        print("No matching app found for:", query)
        return None

    try:
        system = platform.system()

        if system == "Windows":

            app_paths = {
                "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",

                "virtual studio code": r"C:\Users\Acer\AppData\Local\Programs\Microsoft VS Code\Code.exe",

                "spotify": r"spotify:",

                "notepad": "notepad.exe",

                "calculator": "calc.exe",

                "camera": "start microsoft.windows.camera:",

                "intellij idea ce": r"C:\Program Files\JetBrains\IntelliJ IDEA Community Edition\bin\idea64.exe",

                "whatsapp": r"whatsapp:"
            }

            path = app_paths.get(app_name)

            if not path:
                raise Exception(f"No path configured for {app_name}")

            # handle special commands
            if path.startswith("start"):
                subprocess.Popen(path, shell=True)
            else:
                os.startfile(path)

        elif system == "Darwin":
            subprocess.call(["open", "-a", app_name])

        else:
            raise Exception("Unsupported OS")

        speak(f"Opening {app_name}", 1.5)
        print(f"Opened: {app_name}")
        return app_name

    except Exception as e:
        error_msg = f"Error opening {app_name}: {e}"
        print(error_msg)
        speak("I couldn't open that app.", 2)
        return None