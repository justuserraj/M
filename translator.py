import pyttsx3
from googletrans import Translator

def speak(text):
    """Converts text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def translate_text(text_to_translate, target_language):
    """Translates text to a specified language."""
    translator = Translator()
    try:
        speak(f"Translating {text_to_translate} to {target_language}.")
        translated_text = translator.translate(text_to_translate, dest=target_language).text
        speak(f"The translation is: {translated_text}")
    except Exception as e:
        speak("Sorry, I'm having trouble translating that right now.")
        print(f"Translation Error: {e}")