import numpy as np
from neural_net import DeepNeuralNet 

# --- 1. Define Vocabulary and Command Data (UNCHANGED) ---

# The vocabulary defines the total number of features (columns) in our OHE array.
VOCABULARY = {
    'get': 1, 'weather': 2, 'tell': 3, 'a': 4, 'joke': 5, 
    'open': 6, 'browser': 7, 'what': 8, 'is': 9, 'the': 10,
    'news': 11, 'set': 12, 'volume': 13, 'how': 14, 'are': 15, 'you': 16
}
# We need to account for the 'Unknown' word ID (0) and map them to columns
VOCAB_SIZE = len(VOCABULARY) + 1 # 17 features total (0 to 16)

TRAINING_DATA = [
    ("get weather", "Query"),
    ("tell a joke", "Conversation"),
    ("open browser", "System"),
    ("what is the news", "Query"),
    ("set volume", "System"),
    ("how are you", "Conversation"),
]

INTENT_MAP = {
    "Query": [1, 0, 0],
    "System": [0, 1, 0],
    "Conversation": [0, 0, 1]
}

# --- 2. Text Encoding Function (CHANGED TO ONE-HOT ENCODING) ---

def encode_text(text, vocab, vocab_size):
    """Converts a command string into a One-Hot Encoded feature vector."""
    
    # Initialize a wide array of zeros, one column for every word in the vocabulary
    feature_vector = np.zeros(vocab_size)
    
    # Simple tokenization
    tokens = text.lower().split()
    
    for token in tokens:
        # Get the word ID, defaulting to 0 for unknown words
        word_id = vocab.get(token, 0)
        
        # Mark the corresponding column in the feature vector as 1
        # Example: if 'get' is ID 1, feature_vector[1] = 1
        feature_vector[word_id] = 1
    
    return feature_vector

# --- 3. Prepare Training Arrays ---

X_list = [] 
Y = [] 

for command, intent in TRAINING_DATA:
    # Use the new OHE encoder
    encoded_x = encode_text(command, VOCABULARY, VOCAB_SIZE)
    X_list.append(encoded_x)
    Y.append(INTENT_MAP[intent])

# Convert lists to NumPy arrays
X = np.array(X_list)
Y = np.array(Y)

# --- 4. Initialize and Train the Deep Neural Network ---

# The INPUT_SIZE is now the total size of the vocabulary, not the sentence length
INPUT_SIZE = VOCAB_SIZE # 17 features
HIDDEN_SIZE_1 = 12      # Adjusting hidden sizes to suit the wider input
HIDDEN_SIZE_2 = 6
OUTPUT_SIZE = 3         # Number of intents (Query, System, Conversation)

print("Starting Deep Neural Network training for Intent Classification (OHE)...")

# Instantiate your custom DNN
net = DeepNeuralNet(INPUT_SIZE, HIDDEN_SIZE_1, HIDDEN_SIZE_2, OUTPUT_SIZE, learning_rate=0.1)

# Train again with the new input representation
net.train(X, Y, epochs=2000) 
print("Training complete!")

# --- 5. Test the Intent Classifier ---

def classify_intent(text):
    """Encodes a command and runs it through the trained network."""
    # Encode with the OHE function
    encoded_input = encode_text(text, VOCABULARY, VOCAB_SIZE)
    
    # Run the forward pass (inference)
    prediction_raw = net.forward(np.array([encoded_input]))
    
    # Find the index with the highest probability
    predicted_index = np.argmax(prediction_raw)
    
    # Map the index back to the Intent string
    intent_labels = list(INTENT_MAP.keys())
    predicted_intent = intent_labels[predicted_index]
    
    # Get the confidence level
    confidence = prediction_raw[0, predicted_index]
    
    return predicted_intent, confidence

print("\n--- Testing Intent Classifier (OHE) ---")

test_commands = [
    "what is the news",    
    "get weather",         
    "open browser",        
    "tell a joke",         
    "how are you",         
    "get the weather",     # Crucial Test 1: Should now correctly classify as Query
    "tell a story",        # Crucial Test 2: Should now correctly classify as Conversation
]

for command in test_commands:
    intent, confidence = classify_intent(command)
    print(f"Command: '{command}' | Predicted Intent: {intent} (Confidence: {confidence:.2f})")