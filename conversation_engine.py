import datetime

def respond_to_greeting(command):
    """Responds to a greeting based on the time of day."""
    hour = datetime.datetime.now().hour
    if "good morning" in command:
        if 5 <= hour < 12:
            return "Good morning! How can I help you today?"
        else:
            return "Good day to you too. You might be a little late to say good morning!"
    elif "good afternoon" in command:
        if 12 <= hour < 17:
            return "Good afternoon! What do you need?"
        else:
            return "It's not afternoon anymore, but hello anyway."
    elif "good evening" in command:
        if 17 <= hour < 22:
            return "Good evening! Hope you had a great day."
        else:
            return "It's a bit late for evening greetings, but I'm here to help."
    elif "hello" in command or "hi" in command:
        return "Hello! How can I help you today?"
    return None

def handle_gratitude(command):
    """Responds to expressions of thanks."""
    if "thank you" in command or "thanks" in command:
        return "You're welcome."
    return None