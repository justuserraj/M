# weather_control.py

import requests

def get_weather(city, api_key):
    """
    Fetches the current weather for a specified city and returns the result as a string.
    
    Args:
        city (str): The city name to get the weather for.
        api_key (str): The weather API key.
        
    Returns:
        str: A report of the weather conditions or an error message.
    """
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric' # or 'imperial' for Fahrenheit
    }
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code == 200:
            main = data['main']
            weather = data['weather'][0]
            
            temp = main['temp']
            humidity = main['humidity']
            description = weather['description']
            
            report = (
                f"The weather in {city} is {description}. "
                f"The current temperature is {temp:.1f} degrees Celsius with a humidity of {humidity}%."
            )
            return report
        else:
            return f"Could not find weather data for {city}. Status code: {response.status_code}."
            
    except requests.exceptions.RequestException as e:
        return f"A connection error occurred while fetching the weather: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# NOTE: No need to run this file directly for the agent.
# The main assistant file (m_core.py) will call this function.