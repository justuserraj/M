import json
import traceback

# NOTE: The actual functions (create_text_file, get_weather, etc.)
# are imported and mapped in m_core.py's main loop where this function is used.

# Tool descriptions are used to prompt the LLM to output the correct JSON format.
# When you prompt your LLM, you will provide this list.
AVAILABLE_TOOL_DESCRIPTIONS = [
    {
        "name": "create_text_file",
        "description": "Create a new text file with optional content. Use this when the user asks to make or write a file. Requires: file_name (str), content (str, optional).",
        "args": {"file_name": "str", "content": "str"},
        "function": None # Placeholder, mapped in m_core.py
    },
    {
        "name": "list_directory",
        "description": "List files and folders in a specified path (default is current directory). Use this when the user asks to see the contents of a folder. Requires: path (str, optional).",
        "args": {"path": "str"},
        "function": None
    },
    {
        "name": "delete_file",
        "description": "Deletes a specific file. Requires: file_name (str).",
        "args": {"file_name": "str"},
        "function": None
    },
    {
        "name": "get_weather",
        "description": "Get the current weather for a specific city. Requires: city (str).",
        "args": {"city": "str"},
        "function": None
    },
    {
        "name": "get_stock_price",
        "description": "Get the current stock price for a ticker symbol (e.g., AAPL). Requires: symbol (str).",
        "args": {"symbol": "str"},
        "function": None
    },
    {
        "name": "search_wikipedia",
        "description": "Search Wikipedia for general information on a topic. Use this for general knowledge queries. Requires: query (str).",
        "args": {"query": "str"},
        "function": None
    },
    {
        "name": "read_unread_emails",
        "description": "Read and summarize unread emails. Use this when the user asks about new messages.",
        "args": {},
        "function": None
    }
    # Add other utility functions like delete_folder here if desired
]


def execute_agent_command(llm_response_text, tool_map):
    """
    Attempts to parse a special JSON command from the LLM's response
    and execute the corresponding M-Core utility function.
    
    :param llm_response_text: The raw string output from the LLM.
    :param tool_map: A dictionary mapping tool_name (str) to the actual function object.
    :return: The final response string (either the executed result or the LLM's text).
    """
    try:
        # 1. Attempt to parse the response as a JSON tool command
        command_data = json.loads(llm_response_text)
        tool_name = command_data.get("tool_name")
        args = command_data.get("args", {})

        # 2. Validate and execute the tool
        if tool_name in tool_map:
            tool_function = tool_map[tool_name]
            
            # --- EXECUTE THE FUNCTION ---
            # Using **args safely unpacks the arguments
            print(f"[Agent] Executing tool: {tool_name} with args: {args}")
            result = tool_function(**args)
            
            return f"Agent executed **{tool_name}** successfully. Result: {result}"
        else:
            return f"The LLM suggested tool '{tool_name}', but it is not a recognized utility command."
    
    except json.JSONDecodeError:
        # If not valid JSON, it's assumed to be a natural language response.
        return llm_response_text
    except Exception as e:
        # An error occurred during function execution (e.g., missing a required arg)
        print(f"[Agent Error] Failed to execute tool: {e}")
        traceback.print_exc()
        return f"Agent execution failed while running the tool due to a program error: {e}"