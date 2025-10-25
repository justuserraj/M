# task_automation.py

import time
import os
import re

def execute_macro(macro_name: str, command_steps: list, main_processor_function, speak_function) -> str:
    """
    Executes a list of command steps sequentially.

    Args:
        macro_name (str): The name of the macro being executed.
        command_steps (list): A list of strings, where each string is a command to be executed.
        main_processor_function: A callable function (e.g., process_command) 
                                 that handles and executes a single command string.
        speak_function: A callable function (e.g., speak) to provide audio output.

    Returns:
        str: A summary of the macro execution.
    """
    if not command_steps:
        return f"The macro '{macro_name}' is empty. No actions were performed."

    speak_function(f"Initiating macro: {macro_name}. Executing {len(command_steps)} steps.")
    print(f"--- MACRO START: {macro_name} ---")
    
    successful_steps = 0
    
    for i, command in enumerate(command_steps):
        speak_function(f"Step {i + 1}: Executing: {command}")
        print(f"-> Step {i + 1}: Executing command: {command}")
        
        try:
            # The heart of the macro: pass the command to the main processing logic (process_command)
            result = main_processor_function(command) 
            
            # Speak the result if it's a helpful string summary
            if result and isinstance(result, str) and len(result) > 50:
                speak_function(f"Step {i + 1} complete. Result summary: {result[:50]}...")
            elif result and isinstance(result, str):
                 speak_function(f"Step {i + 1} complete: {result}")
            else:
                speak_function(f"Step {i + 1} complete.")
            
            successful_steps += 1
            time.sleep(1) # Pause slightly between steps
            
        except Exception as e:
            error_message = f"An error occurred during step {i + 1}: {e}. Stopping macro."
            print(f"!!! Error in macro step: {error_message}")
            speak_function(error_message)
            # Break the macro execution on the first error
            break 
            
    final_summary = f"Macro {macro_name} completed. {successful_steps} out of {len(command_steps)} steps executed successfully."
    print(f"--- MACRO END: {macro_name} ---")
    speak_function(final_summary)
    return final_summary


def parse_macro_steps_from_llm(llm_tool_args: dict) -> list:
    """
    This is a utility function, primarily ensuring the 'steps' argument is a list.
    """
    steps_list = llm_tool_args.get("steps")
    if isinstance(steps_list, str):
        # If the LLM returns steps as a comma-separated string, convert it to a list
        steps_list = [step.strip() for step in re.split(r',\s*(?=.*)', steps_list) if step.strip()]
        
    if not isinstance(steps_list, list):
        return []
        
    return steps_list