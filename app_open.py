import subprocess
import platform
import os
from tts import speak


def open_app(query, app_path_windows=None):
    
    apps = ["chrome", "photoshop", "virtual studio code", "spotify", "notes", "calculator","photo booth","intellij idea ce"]
    
    query = query.lower()
    query = query.replace("vs code","virtual studio code")
    query = query.replace("intellij","intellij idea ce")
    query = query.replace("camera","photo booth")


    # Extract app name
    app_name = next((app for app in apps if app in query), None)

    if not app_name:
        speak("Sorry, I could not find that app.",2)
        print("Not found anything")
        return None

    try:
        if platform.system() == "Darwin":
            subprocess.call(["open", "-a", app_name])
        elif platform.system() == "Windows":
            if app_path_windows:
                os.startfile(app_path_windows)
            else:
                subprocess.Popen(app_name)
        speak(f"Opened {app_name}",1.5)
        return app_name
    except Exception as e:
        speak(f"Error opening {app_name}",2)
        print(f"Error opening {app_name}: {e}")
        return None

