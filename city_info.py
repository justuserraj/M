import wikipedia
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    """Converts text to speech."""
    print(f"M: {text}")
    engine.say(text)
    engine.runAndWait()

def tell_me_about(topic):
    """Tells the user about a specified topic from Wikipedia."""
    if not topic:
        speak("Please tell me what you want to know about.")
        return

    try:
        summary = wikipedia.summary(topic, sentences=2)
        speak(f"According to Wikipedia, {summary}")
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"I found a few things about {topic}. Can you be more specific?")
        print(f"Options are: {e.options}")
    except wikipedia.exceptions.PageError:
        speak(f"Sorry, I couldn't find any information about {topic}.")
    except Exception as e:
        speak("Sorry, I'm having trouble getting that information right now.")
        print(f"Error: {e}")