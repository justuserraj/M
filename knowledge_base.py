import json
import re

KNOWLEDGE_BASE_FILE = "knowledge_base.json"

def load_knowledge_base():
    """Loads the knowledge base from a JSON file."""
    try:
        with open(KNOWLEDGE_BASE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_knowledge_base(knowledge_base):
    """Saves the knowledge base to a JSON file."""
    with open(KNOWLEDGE_BASE_FILE, "w") as f:
        json.dump(knowledge_base, f, indent=4)

def save_fact(question, answer):
    """Saves a fact to the knowledge base."""
    knowledge_base = load_knowledge_base()
    # Normalize the question for easier lookup
    normalized_question = question.strip().lower()
    knowledge_base[normalized_question] = answer
    save_knowledge_base(knowledge_base)
    return f"Okay, I've learned that '{question}' is '{answer}'."

def find_best_answer(knowledge_base, query):
    """Finds the best answer for a given query from the knowledge base."""
    # First, try to find an exact match
    exact_match = knowledge_base.get(query.lower().strip())
    if exact_match:
        return exact_match

    # If no exact match, try to find a partial match
    for question, answer in knowledge_base.items():
        if re.search(r'\b' + re.escape(query) + r'\b', question, re.IGNORECASE):
            return answer
    
    return None

def save_synonym(new_phrase, canonical_phrase):
    """Saves a new phrase as a synonym for a canonical command."""
    knowledge_base = load_knowledge_base()
    knowledge_base[new_phrase.lower().strip()] = f"command_synonym:{canonical_phrase.lower().strip()}"
    save_knowledge_base(knowledge_base)
    return "Okay, I've learned that."