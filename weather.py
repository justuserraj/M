import pyowm
import pyttsx3
import re

engine = pyttsx3.init()

def speak(text):
    """Converts text to speech."""
    print(f"M: {text}")
    engine.say(text)
    engine.runAndWait()

# This is the API key you already have in m_core.py.
# You can leave this as a placeholder, or copy the key here.
owm = pyowm.OWM('520659376199bc11641b9f131aaa5de6')
weather_mgr = owm.weather_manager()

def get_weather(city):
    """Tells the user the weather for a specific city."""
    if not city:
        speak("Please tell me the name of the city.")
        return

    try:
        observation = weather_mgr.weather_at_place(city)
        w = observation.weather
        temperature = w.temperature('celsius')['temp']
        status = w.status
        speak(f"The weather in {city} is {status} with a temperature of {temperature} degrees Celsius.")
    except pyowm.commons.exceptions.NotFoundError:
        speak(f"Sorry, I couldn't find the weather for {city}.")
    except Exception as e:
        speak("Sorry, I'm having trouble getting the weather right now.")
        print(f"Error: {e}")