# llm_brain.py
import re
import json
import webbrowser
from typing import Dict, Any, Callable

# --- Core LLM Function (Placeholder) ---

def get_llm_response(prompt: str, tool_descriptions: str) -> str:
    """
    Simulates a call to the LLM Agent. 
    It returns a simulated tool call or a direct text response.
    In a real application, this would use an external API like Google's Gemini.
    """
    # Simple logic to simulate LLM deciding to use a tool or answer directly
    
    # 1. Simulate tool call logic
    if "weather" in prompt.lower() and "get_weather" in tool_descriptions:
        # LLM decides to use get_weather tool
        city_match = re.search(r'in\s+([a-zA-Z\s]+)', prompt)
        city = city_match.group(1).strip() if city_match else "default_city"
        return f"TOOL_CALL: get_weather(city='{city}')"
    
    if "news" in prompt.lower() and "get_news" in tool_descriptions:
        return "TOOL_CALL: get_news()"
        
    if "stock price" in prompt.lower() and "get_stock_price" in tool_descriptions:
        # LLM decides to use get_stock_price tool
        stock_match = re.search(r'price of (.+)', prompt)
        stock = stock_match.group(1).strip() if stock_match else "GOOG"
        return f"TOOL_CALL: get_stock_price(ticker='{stock}')"
        
    if ("search for" in prompt.lower() or "look up" in prompt.lower()) and "web_search" in tool_descriptions:
        # LLM decides to use web_search tool for general queries
        query = prompt.replace("search for", "").replace("look up", "").strip()
        return f"TOOL_CALL: web_search(query='{query}')"
        
    if ("wikipedia" in prompt.lower() or "learn about" in prompt.lower()) and "search_wikipedia" in tool_descriptions:
        topic = prompt.split("about")[-1].strip()
        return f"TOOL_CALL: search_wikipedia(query='{topic}')"
        
    # 2. Simulate direct answer logic (for conversation)
    if any(phrase in prompt.lower() for phrase in ["who are you", "what are you"]):
        return "I am VEDRA, your customized virtual assistant, optimized for speed and local control. I can manage your files, search the web, and run local system commands."
    
    # 3. Default or complex question fallback
    return "I do not have a specific tool for that, but based on your query, I believe the answer is highly context-dependent. How about a joke instead? Why don't scientists trust atoms? Because they make up everything!"


# --- Tool Execution Core ---

def execute_agent_command(llm_output: str, tool_function_map: Dict[str, Callable]) -> str:
    """
    Parses the LLM's output string and executes the specified tool function.
    """
    # Regex to find the TOOL_CALL pattern: TOOL_CALL: func_name(arg1='value1', arg2='value2')
    match = re.match(r"TOOL_CALL:\s*([a-zA-Z0-9_]+)\s*\((.*)\)", llm_output)
    
    if not match:
        # If no tool call, return the LLM's direct text response
        return llm_output

    function_name = match.group(1)
    args_str = match.group(2)
    args = {}

    # Parse arguments from the string (simple key='value' parsing)
    for arg_match in re.finditer(r"([a-zA-Z0-9_]+)='([^']*)'", args_str):
        key = arg_match.group(1)
        value = arg_match.group(2)
        args[key] = value

    # Execute the function
    if function_name in tool_function_map:
        try:
            func = tool_function_map[function_name]
            result = func(**args) # Unpack arguments and call the function
            
            # Special handling for web_search since it returns None (opens browser)
            if function_name == "web_search":
                 return f"Opening your web browser for the query: {args.get('query', 'search results')}."
                 
            return result
        except Exception as e:
            return f"Error executing tool '{function_name}': {e}"
    else:
        return f"LLM attempted to call unknown tool: {function_name}"


# --- New Tool Definitions ---

def web_search(query: str):
    """Opens the user's default web browser to search for a query."""
    # This function is a simple proxy to open the browser, 
    # as the actual search happens outside the Python environment.
    webbrowser.open(f"https://www.google.com/search?q={query}")


# --- Available Tools for LLM Prompt ---

AVAILABLE_TOOL_DESCRIPTIONS = """
AVAILABLE TOOLS:
- get_weather(city: str) -> str: Get the current weather for a specified city. Requires a city name.
- get_news() -> str: Fetch the latest general news headlines.
- get_stock_price(ticker: str) -> str: Get the current stock price for a given ticker symbol (e.g., 'GOOG' for Google).
- search_wikipedia(query: str) -> str: Search Wikipedia for a topic and return a summary.
- web_search(query: str): Open the default web browser to search for a general query.
"""