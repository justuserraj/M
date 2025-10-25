def do_local_calculation(speak, expression):
    """Performs basic arithmetic operations locally."""
    try:
        result = eval(expression)
        speak(f"The answer is {result}")
    except (NameError, SyntaxError, ZeroDivisionError) as e:
        speak("Sorry, I couldn't perform that calculation. Please enter a simple math expression.")
        print(f"Calculation Error: {e}")