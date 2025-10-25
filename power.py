import os
import sys
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    """Converts text to speech."""
    print(f"M: {text}")
    engine.say(text)
    engine.runAndWait()

def shutdown_computer():
    """Shuts down the computer."""
    speak("Shutting down the computer now. Goodbye!")
    if sys.platform == "win32":
        os.system("shutdown /s /t 1")
    elif sys.platform == "darwin":  # macOS
        os.system("sudo shutdown -h now")
    elif sys.platform.startswith("linux"):
        os.system("sudo shutdown now")
    else:
        speak("Sorry, I don't know how to shut down your operating system.")

def restart_computer():
    """Restarts the computer."""
    speak("Restarting the computer now. Goodbye!")
    if sys.platform == "win32":
        os.system("shutdown /r /t 1")
    elif sys.platform == "darwin":  # macOS
        os.system("sudo shutdown -r now")
    elif sys.platform.startswith("linux"):
        os.system("sudo reboot")
    else:
        speak("Sorry, I don't know how to restart your operating system.")

def lock_computer():
    """Locks the computer's screen."""
    speak("Locking the computer now.")
    if sys.platform == "win32":
        os.system("Rundll32.exe user32.dll,LockWorkStation")
    elif sys.platform == "darwin":  # macOS
        os.system("osascript -e 'tell application \"System Events\" to keystroke \"q\" using {command down, control down}'")
    elif sys.platform.startswith("linux"):
        os.system("gnome-screensaver-command --lock")
    else:
        speak("Sorry, I don't know how to lock your operating system.")