import wikipedia

def search_wikipedia(speak, query):
    """Searches Wikipedia and provides a summary."""
    try:
        speak("Searching Wikipedia...")
        result = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia, " + result)
    except wikipedia.exceptions.PageError:
        speak("Sorry, I could not find a Wikipedia page for that topic.")
    except wikipedia.exceptions.DisambiguationError as e:
        speak("I found multiple matches. Please be more specific.")
    except Exception as e:
        speak("Sorry, I ran into an issue searching Wikipedia.")
        print(f"Wikipedia Error: {e}")