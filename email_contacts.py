import json

def load_contacts():
    """Loads contact data from a JSON file."""
    try:
        with open("contacts.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {} # Return an empty dictionary if the file doesn't exist

def save_contacts(data):
    """Saves contact data to a JSON file."""
    with open("contacts.json", "w") as f:
        json.dump(data, f, indent=4)