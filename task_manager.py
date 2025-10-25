def set_reminder(speak, reminders, time, reminder_text):
    """Sets a reminder."""
    reminders[time] = reminder_text
    speak(f"Okay, I'll remind you to {reminder_text} at {time}.")

def add_to_do(speak, tasks, item):
    """Adds a task to the to-do list."""
    tasks.append(item)
    speak(f"Okay, I've added {item} to your to-do list.")

def get_to_do(speak, tasks):
    """Reads the to-do list."""
    if not tasks:
        speak("Your to-do list is empty.")
    else:
        speak("Here are your tasks:")
        for i, task in enumerate(tasks):
            speak(f"Task {i + 1}: {task}")

def delete_to_do(speak, tasks, item):
    """Deletes a task from the to-do list."""
    if item in tasks:
        tasks.remove(item)
        speak(f"Okay, I've removed {item} from your to-do list.")
    else:
        speak(f"I couldn't find {item} in your to-do list.")