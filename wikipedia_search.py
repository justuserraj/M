import wikipedia

def search_wikipedia(speak, query):
    """Searches Wikipedia and reads the summary."""
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("Searching Wikipedia...")
        speak(f"According to Wikipedia, {results}")
    except wikipedia.exceptions.PageError:
        speak(f"Sorry, I could not find any information on {query}.")
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:5]
        speak(f"Could you be more specific? I found several matches for {query}. The top options are: {', '.join(options)}")