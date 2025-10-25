import pyttsx3
import requests
import pint

# Initialize Pint's Unit Registry
ureg = pint.UnitRegistry()

def speak(text):
    """Converts text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def convert_units(value, from_unit, to_unit):
    """Converts a value from one unit to another."""
    try:
        # Create a Quantity object
        q = ureg(f"{value} {from_unit}")
        # Convert to the target unit
        result = q.to(to_unit)
        speak(f"{value} {from_unit} is equal to {result:.2f} {to_unit}.")
    except pint.errors.UndefinedUnitError:
        speak("Sorry, one of those units is not a valid unit of measurement.")
    except Exception as e:
        speak("Sorry, I couldn't perform that unit conversion.")
        print(f"Error in unit conversion: {e}")

def convert_currency(amount, from_currency, to_currency):
    """Converts an amount from one currency to another using a free API."""
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency.upper()}"
        response = requests.get(url)
        data = response.json()
        
        rate = data['rates'].get(to_currency.upper())
        if rate:
            result = float(amount) * rate
            speak(f"{amount} {from_currency} is equal to {result:.2f} {to_currency}.")
        else:
            speak("Sorry, I couldn't find a conversion rate for that currency.")
            
    except requests.exceptions.RequestException:
        speak("Sorry, I'm having trouble connecting to the currency service right now.")
    except Exception as e:
        speak("Sorry, I couldn't perform that currency conversion.")
        print(f"Error in currency conversion: {e}")