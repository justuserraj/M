import datetime
import pyttsx3

# This speaks function is needed here so the module can speak
engine = pyttsx3.init()

def speak(text):
    """Converts text to speech."""
    print(f"M: {text}")
    engine.say(text)
    engine.runAndWait()

def get_time():
    """Tells the user the current time."""
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    speak(f"The current time is {current_time}.")

def get_date():
    """Tells the user the current date."""
    now = datetime.datetime.now()
    current_date = now.strftime("%A, %B %d, %Y")
    speak(f"Today's date is {current_date}.")