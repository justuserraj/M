import pyjokes
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    """Converts text to speech."""
    print(f"M: {text}")
    engine.say(text)
    engine.runAndWait()

def tell_joke():
    """Tells a joke."""
    joke = pyjokes.get_joke()
    speak(joke)