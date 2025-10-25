import requests
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    """Converts text to speech."""
    print(f"M: {text}")
    engine.say(text)
    engine.runAndWait()

def get_news_headlines(api_key, country="us"):
    """Fetches and speaks top headlines from a specific country."""
    # Dictionary to map country names to two-letter codes
    country_codes = {
        "usa": "us", "us": "us", "united states": "us",
        "india": "in", "ind": "in",
        "uk": "gb", "united kingdom": "gb",
        "canada": "ca", "can": "ca",
        "australia": "au", "aus": "au"
    }

    country_code = country_codes.get(country.lower(), "us") # Default to 'us' if not found

    try:
        url = f"https://newsapi.org/v2/top-headlines?country={country_code}&apiKey={api_key}"
        response = requests.get(url)
        data = response.json()

        if data["status"] == "ok":
            speak(f"Here are the top headlines from {country.title()}:")
            headlines = data["articles"]
            for article in headlines[:3]:  # Read the first 3 headlines
                speak(article["title"])
        else:
            speak("Sorry, I couldn't fetch the news right now.")
            print(f"News API error: {data.get('message', 'Unknown error')}")

    except requests.exceptions.RequestException as e:
        speak("Sorry, I'm having trouble connecting to the internet to get the news.")
        print(f"Connection error: {e}")
    except Exception as e:
        speak("Sorry, something went wrong.")
        print(f"Error: {e}")