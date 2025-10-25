import yfinance as yf

def get_stock_price(speak, symbol):
    """Fetches the current stock price for a given symbol."""
    try:
        stock_info = yf.Ticker(symbol).info
        price = stock_info.get("currentPrice")
        if price:
            speak(f"The current stock price of {symbol} is {price}.")
        else:
            speak(f"Sorry, I could not find the stock price for {symbol}.")
    except Exception as e:
        speak("I'm sorry, an error occurred while trying to get the stock price.")
        print(f"Stock price error: {e}")