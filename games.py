import random
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    """Converts text to speech."""
    print(f"M: {text}")
    engine.say(text)
    engine.runAndWait()

def toss_coin():
    """Tosses a coin and tells the user the result."""
    result = random.choice(["heads", "tails"])
    speak(f"The coin landed on {result}.")

def roll_dice():
    """Rolls a six-sided die and tells the user the result."""
    result = random.randint(1, 6)
    speak(f"The die landed on {result}.")