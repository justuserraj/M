def get_stock_price(speak, symbol):
    """Fetches and speaks the stock price."""
    try:
        speak("Sorry, I cannot get stock prices right now as I don't have the API key")
    except Exception as e:
        speak("Sorry, I ran into an issue getting the stock price.")
        print(f"Stock API Error: {e}")