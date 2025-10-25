import pytz
import datetime
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    """Converts text to speech."""
    print(f"M: {text}")
    engine.say(text)
    engine.runAndWait()

def get_city_time(city):
    """Tells the user the current time in a specified city."""
    if not city:
        speak("Please tell me the name of the city or country.")
        return

    # A simple mapping for some common cities and countries to their time zones
    city_timezones = {
        "new york": "America/New_York",
        "london": "Europe/London",
        "tokyo": "Asia/Tokyo",
        "sydney": "Australia/Sydney",
        "dubai": "Asia/Dubai",
        "paris": "Europe/Paris",
        "delhi": "Asia/Kolkata",
        "mumbai": "Asia/Kolkata",
        "beijing": "Asia/Shanghai",
        "moscow": "Europe/Moscow",
        "cairo": "Africa/Cairo"
    }

    # Normalize the city name
    normalized_city = city.lower().strip()

    try:
        if normalized_city in city_timezones:
            tz = pytz.timezone(city_timezones[normalized_city])
            now = datetime.datetime.now(tz)
            current_time = now.strftime("%I:%M %p")
            speak(f"The current time in {city.title()} is {current_time}.")
        else:
            speak("Sorry, I don't know the time zone for that location yet.")
    except Exception as e:
        speak("Sorry, I'm having trouble getting the time right now.")
        print(f"Error: {e}")