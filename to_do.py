import pyttsx3
import os

engine = pyttsx3.init()

def speak(text):
    """Converts text to speech."""
    print(f"M: {text}")
    engine.say(text)
    engine.runAndWait()

def add_to_do_item(item):
    """Adds a new item to the to-do list."""
    with open("todo.txt", "a") as f:
        f.write(f"- {item}\n")
    speak(f"Added '{item}' to your to-do list.")

def show_to_do_list():
    """Reads and speaks the current to-do list."""
    try:
        with open("todo.txt", "r") as f:
            lines = f.readlines()
        if lines:
            speak("Here are your to-do items:")
            for line in lines:
                speak(line.strip())
        else:
            speak("Your to-do list is empty.")
    except FileNotFoundError:
        speak("You don't have a to-do list yet.")

def remove_to_do_item(item_to_remove):
    """Removes a specific item from the to-do list."""
    try:
        with open("todo.txt", "r") as f:
            lines = f.readlines()
        
        updated_lines = [line for line in lines if item_to_remove.lower() not in line.lower()]
        
        if len(updated_lines) < len(lines):
            with open("todo.txt", "w") as f:
                f.writelines(updated_lines)
            speak(f"Removed '{item_to_remove}' from your to-do list.")
        else:
            speak(f"Sorry, I couldn't find '{item_to_remove}' on your to-do list.")
    except FileNotFoundError:
        speak("You don't have a to-do list yet.")

def clear_to_do_list():
    """Removes all items from the to-do list."""
    try:
        with open("todo.txt", "w") as f:
            f.write("")  # Overwrites the file, effectively clearing it
        speak("Your to-do list has been cleared.")
    except Exception as e:
        speak("Sorry, I'm having trouble clearing the list.")
        print(e)