import speech_recognition as sr
import pyttsx3
import time

def speak(text):
    """A simple function to make the program speak."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def test_microphone():
    """Tests the microphone and speech recognition."""
    r = sr.Recognizer()
    
    # Optional: List all microphones to see if yours is detected
    try:
        print("Available microphones:")
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"  {index}: {name}")
    except Exception as e:
        print(f"Could not list microphones: {e}")
        
    speak("Hello! I am going to test your speakers and microphone.")
    time.sleep(1) # Wait a moment for the user to get ready

    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise. Please be silent...")
            # This line is crucial for ignoring background noise
            r.adjust_for_ambient_noise(source, duration=1) 
            print("Listening for your voice. Please say something...")
            
            audio = r.listen(source, timeout=5)
            print("Processing audio...")
            
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            speak(f"I heard you say: {text}")

    except sr.UnknownValueError:
        print("Could not understand audio. You may have spoken too softly or there was too much background noise.")
        speak("I could not understand what you said. Please try again.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        speak("My speech recognition service is not working. Please check your internet connection.")
    except sr.WaitTimeoutError:
        print("Listening timed out. No speech detected.")
        speak("I did not hear anything. The microphone may not be working correctly.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        speak("An unexpected error occurred during the test.")

if __name__ == "__main__":
    test_microphone()