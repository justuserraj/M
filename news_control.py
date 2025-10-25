import requests

def get_news(speak, country='us'):
    """Fetches and reads top news headlines."""
    try:
        url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey=f469235bbaeb43cf9dd914770a3efec4"
        response = requests.get(url)
        data = response.json()
        if data["status"] == "ok" and data["articles"]:
            speak("Here are the top headlines:")
            for article in data["articles"][:5]:
                speak(article["title"])
        else:
            speak("Sorry, I couldn't get the news right now.")
    except Exception as e:
        speak("Sorry, I couldn't get the news right now.")
        print(f"News API Error: {e}")