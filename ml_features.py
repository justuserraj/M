import spacy

# Load the spaCy model once when the module is imported
# This is the model you successfully downloaded: en_core_web_sm
try:
    # IMPORTANT: Loading the model is resource-intensive. Do this only once.
    NLP_MODEL = spacy.load("en_core_web_sm")
except OSError as e:
    # This should not happen since you successfully downloaded the model
    NLP_MODEL = None
    print(f"ERROR: spaCy model 'en_core_web_sm' could not be loaded: {e}")
    # Consider telling the user to run 'python -m spacy download en_core_web_sm'


def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text using the spaCy NLP model.
    Returns a score (0.0 to 1.0) where 0.5 is neutral.
    """
    if NLP_MODEL:
        # Process the text using the loaded spaCy model
        doc = NLP_MODEL(text)
        
        # -----------------------------------------------------------------
        # NOTE: The 'en_core_web_sm' model does not include a direct 
        # sentiment component by default. This section is a PLACEHOLDER.
        # 
        # You will need to either install a dedicated sentiment extension
        # (like spacytextblob) or implement your own sentiment logic 
        # based on words, dependency parsing, or POS tags from the 'doc'.
        # -----------------------------------------------------------------
        
        # Simple placeholder heuristic to ensure the function works and returns a float:
        text_lower = text.lower()
        if "good" in text_lower or "best" in text_lower or "love" in text_lower:
            return 0.9  # Positive
        elif "bad" in text_lower or "worst" in text_lower or "hate" in text_lower:
            return 0.1  # Negative
        
        return 0.5 # Neutral fallback
    
    # If the model failed to load, return 0.0 (matching original error return)
    return 0.0