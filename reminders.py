import datetime
import pyttsx3
import os

def speak(text):
    """Converts text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def add_reminder(reminder_text, due_date_str):
    """Adds a new reminder to the reminders.txt file."""
    try:
        due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d %H:%M')
        with open("reminders.txt", "a") as file:
            file.write(f"{due_date_str},{reminder_text}\n")
        speak("Reminder added successfully.")
    except ValueError:
        speak("Sorry, I couldn't understand the date. Please use YYYY-MM-DD HH:MM format.")

def check_reminders():
    """Checks for and alerts the user about due reminders."""
    if not os.path.exists("reminders.txt"):
        return
    
    current_time = datetime.datetime.now()
    updated_reminders = []
    
    with open("reminders.txt", "r") as file:
        reminders = file.readlines()
        
    for reminder_line in reminders:
        try:
            due_date_str, reminder_text = reminder_line.strip().split(',', 1)
            due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d %H:%M')
            
            if due_date <= current_time:
                speak(f"Reminder: {reminder_text} is now due.")
            else:
                updated_reminders.append(reminder_line)
        except (ValueError, IndexError):
            # Keep invalid lines to avoid data loss
            updated_reminders.append(reminder_line)
            
    with open("reminders.txt", "w") as file:
        file.writelines(updated_reminders)

def show_reminders():
    """Reads and speaks all active reminders."""
    if not os.path.exists("reminders.txt") or os.stat("reminders.txt").st_size == 0:
        speak("You have no active reminders.")
        return
        
    with open("reminders.txt", "r") as file:
        reminders = file.readlines()
        
    speak("Here are your active reminders:")
    for reminder_line in reminders:
        due_date_str, reminder_text = reminder_line.strip().split(',', 1)
        speak(f"On {due_date_str}, you have: {reminder_text}")