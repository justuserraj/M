import pyttsx3
import google.generativeai as genai

def speak(text):
    """Converts text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def ask_gemini(query):
    """Sends a query to the Gemini AI model and speaks the response."""

    genai.configure(api_key="AIzaSyC9cz0o9WvxdHKS0CXI4js5t3Ytpu_WNEQ")  # <-- REPLACE THIS

    # Use the 'gemini-pro' model for text-based queries
    model = genai.GenerativeModel('gemini-pro')
    
    try:
        response = model.generate_content(query)
        speak(response.text)
        print("Gemini: " + response.text)
        
    except Exception as e:
        speak("I'm sorry, I'm having trouble connecting to the AI service right now.")
        print(f"Error communicating with Gemini API: {e}")