import spacy

# Load the language model
nlp = spacy.load("en_core_web_sm")

def process_command(command_text):
    """Processes a command using spaCy to find its intent and entities."""
    doc = nlp(command_text)
    
    # Check for intent based on a broader list of keywords
    intent = "unrecognized"
    if any(token.lemma_ in ["weather", "rain", "forecast", "temperature"] for token in doc):
        intent = "get_weather"
    elif any(token.lemma_ in ["joke", "jokes", "funny"] for token in doc):
        intent = "tell_joke"
    elif any(token.lemma_ in ["time", "timing"] for token in doc):
        intent = "get_time"
        
    # Simple logic to find entities (e.g., location)
    location = None
    for ent in doc.ents:
        if ent.label_ == "GPE": # GPE stands for Geopolitical Entity (cities, states)
            location = ent.text
            
    return {"intent": intent, "location": location}