import pyttsx3
import requests

def speak(text):
    """Converts text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_stock_price(ticker_symbol):
    """Fetches and speaks the current stock price for a given ticker symbol."""
    API_KEY = "9VLFM024SGHOI83P"  # <-- REPLACE THIS

    try:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker_symbol}&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()

        # Check for API errors or invalid ticker symbol
        if "Global Quote" in data and data["Global Quote"]:
            stock_info = data["Global Quote"]
            price = float(stock_info["05. price"])
            speak(f"The current price of {ticker_symbol} is {price:.2f} US dollars.")
        else:
            speak("Sorry, I couldn't find a stock with that ticker symbol. Please check if the ticker symbol is correct.")

    except requests.exceptions.RequestException:
        speak("Sorry, I'm having trouble connecting to the stock market service right now.")
    except Exception as e:
        speak("An error occurred while fetching the stock price.")
        print(f"Error in stock tracker: {e}")