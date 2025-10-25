import wikipedia
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    """Converts text to speech."""
    print(f"M: {text}")
    engine.say(text)
    engine.runAndWait()

def tell_fact():
    """Tells a random fact from Wikipedia."""
    try:
        topic = wikipedia.random(pages=1)
        summary = wikipedia.summary(topic, sentences=2)
        speak(f"Here is a random fact: {summary}")
    except wikipedia.exceptions.DisambiguationError as e:
        speak("I found too many results. Can you be more specific?")
        print(e.options)
    except wikipedia.exceptions.PageError:
        speak("Sorry, I couldn't find a fact right now.")
    except Exception as e:
        speak("Sorry, I'm having trouble getting a fact right now.")
        print(f"Error: {e}")