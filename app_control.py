import os
import subprocess
import pyttsx3
import re
from app_aliases import APP_ALIASES

def speak(text):
    """Converts text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def open_application(app_name):
    """Opens an application on the computer."""
    app_name = app_name.lower().strip()

    # Check for aliases first
    if app_name in APP_ALIASES:
        path = APP_ALIASES[app_name]
        try:
            if os.path.exists(path):
                # Use subprocess to handle paths with spaces
                subprocess.Popen(path)
                speak(f"Opening {app_name}.")
                return
            else:
                # If the path doesn't exist, try the name directly
                os.startfile(path)
                speak(f"Opening {app_name}.")
                return
        except FileNotFoundError:
            speak(f"Sorry, I couldn't find the file for {app_name}. Please check the path in the app_aliases.py file.")
        except Exception as e:
            speak(f"Sorry, I ran into an issue trying to open that.")
            print(f"Error opening application: {e}")
            return
            
    # Try opening with the common application name
    try:
        os.startfile(app_name)
        speak(f"Opening {app_name}.")
    except FileNotFoundError:
        speak(f"Sorry, I couldn't find the application {app_name}. Please make sure it is installed and try again.")
    except Exception as e:
        speak(f"Sorry, I ran into an issue trying to open that.")
        print(f"Error opening application: {e}")