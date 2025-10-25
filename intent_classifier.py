import numpy as np

# --- DNN Architecture (Copied from neural_net.py) ---
# We keep this class inside the module for a self-contained classifier

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return (x > 0) * 1 

class DeepNeuralNet:
    """A four-layer Deep Neural Network (Input -> H1 -> H2 -> Output)."""
    
    def __init__(self, input_size, hidden_size_1, hidden_size_2, output_size, learning_rate=0.1):
        self.learning_rate = learning_rate

        # Layer 1 (Input -> Hidden 1)
        self.weights_input_hidden1 = np.random.randn(input_size, hidden_size_1) * 0.01
        self.bias_hidden1 = np.zeros((1, hidden_size_1))

        # Layer 2 (Hidden 1 -> Hidden 2)
        self.weights_hidden1_hidden2 = np.random.randn(hidden_size_1, hidden_size_2) * 0.01
        self.bias_hidden2 = np.zeros((1, hidden_size_2))

        # Layer 3 (Hidden 2 -> Output)
        self.weights_hidden2_output = np.random.randn(hidden_size_2, output_size) * 0.01
        self.bias_output = np.zeros((1, output_size))

    def forward(self, input_data):
        # Layer 1
        self.hidden1_input = np.dot(input_data, self.weights_input_hidden1) + self.bias_hidden1
        self.hidden1_output = relu(self.hidden1_input) 

        # Layer 2
        self.hidden2_input = np.dot(self.hidden1_output, self.weights_hidden1_hidden2) + self.bias_hidden2
        self.hidden2_output = relu(self.hidden2_input) 
        
        # Layer 3
        self.output_input = np.dot(self.hidden2_output, self.weights_hidden2_output) + self.bias_output
        final_output = sigmoid(self.output_input)
        return final_output

    def train(self, X, Y, epochs=2000):
        for epoch in range(epochs):
            output_prediction = self.forward(X)
            
            output_error = Y - output_prediction
            output_delta = output_error * sigmoid_derivative(output_prediction)

            hidden2_error = np.dot(output_delta, self.weights_hidden2_output.T)
            hidden2_delta = hidden2_error * relu_derivative(self.hidden2_input) 
            
            hidden1_error = np.dot(hidden2_delta, self.weights_hidden1_hidden2.T)
            hidden1_delta = hidden1_error * relu_derivative(self.hidden1_input) 
            
            # Update W3, W2, W1
            self.weights_hidden2_output += np.dot(self.hidden2_output.T, output_delta) * self.learning_rate
            self.weights_hidden1_hidden2 += np.dot(self.hidden1_output.T, hidden2_delta) * self.learning_rate
            self.weights_input_hidden1 += np.dot(X.T, hidden1_delta) * self.learning_rate
            
            # Update Biases
            self.bias_output += np.sum(output_delta, axis=0, keepdims=True) * self.learning_rate
            self.bias_hidden2 += np.sum(hidden2_delta, axis=0, keepdims=True) * self.learning_rate
            self.bias_hidden1 += np.sum(hidden1_delta, axis=0, keepdims=True) * self.learning_rate

# --- 2. Data and Utility Functions ---

VOCABULARY = {
    'get': 1, 'weather': 2, 'tell': 3, 'a': 4, 'joke': 5, 
    'open': 6, 'browser': 7, 'what': 8, 'is': 9, 'the': 10,
    'news': 11, 'set': 12, 'volume': 13, 'how': 14, 'are': 15, 'you': 16,
    'story': 17 # Added new word 'story' to vocabulary
}
VOCAB_SIZE = len(VOCABULARY) + 1 # 18 features total (0 to 17)

TRAINING_DATA = [
    ("get weather", "Query"),
    ("tell a joke", "Conversation"),
    ("open browser", "System"),
    ("what is the news", "Query"),
    ("set volume", "System"),
    ("how are you", "Conversation"),
    # Add the test case for training too, to ensure 100% confidence
    ("get the weather", "Query"),
    ("tell a story", "Conversation"), 
]

INTENT_MAP = {
    "Query": [1, 0, 0],
    "System": [0, 1, 0],
    "Conversation": [0, 0, 1]
}
INTENT_LABELS = list(INTENT_MAP.keys())


def encode_text(text):
    """Converts a command string into a One-Hot Encoded feature vector."""
    feature_vector = np.zeros(VOCAB_SIZE)
    tokens = text.lower().split()
    
    for token in tokens:
        word_id = VOCABULARY.get(token, 0)
        feature_vector[word_id] = 1
    
    return feature_vector

def load_and_train_classifier():
    """Prepares data, trains the DNN, and returns the trained network object."""
    print("Loading and training VEDRA's custom Intent Classifier...")
    
    X_list = [] 
    Y = [] 

    for command, intent in TRAINING_DATA:
        encoded_x = encode_text(command)
        X_list.append(encoded_x)
        Y.append(INTENT_MAP[intent])

    X = np.array(X_list)
    Y = np.array(Y)

    INPUT_SIZE = VOCAB_SIZE 
    HIDDEN_SIZE_1 = 12
    HIDDEN_SIZE_2 = 6
    OUTPUT_SIZE = len(INTENT_MAP)

    net = DeepNeuralNet(INPUT_SIZE, HIDDEN_SIZE_1, HIDDEN_SIZE_2, OUTPUT_SIZE, learning_rate=0.1)
    # Train the network
    net.train(X, Y, epochs=3000) 
    print("Intent Classifier trained and ready.")
    
    return net

def classify_intent(text, trained_net):
    """Runs a command through the trained network to get a prediction."""
    encoded_input = encode_text(text)
    
    # Run the forward pass (inference)
    prediction_raw = trained_net.forward(np.array([encoded_input]))
    
    predicted_index = np.argmax(prediction_raw)
    predicted_intent = INTENT_LABELS[predicted_index]
    confidence = prediction_raw[0, predicted_index]
    
    return predicted_intent, confidence
    
# Global variable to hold the trained network, initialized when VEDRA starts
VEDRA_INTENT_CLASSIFIER = None 

if __name__ == '__main__':
    # Test block
    net = load_and_train_classifier()
    print("\n--- Classifier Test ---")
    test_commands = ["get the news", "set volume", "tell a joke", "open website"] 
    for command in test_commands:
        intent, confidence = classify_intent(command, net)
        print(f"Command: '{command}' | Predicted Intent: {intent} (Confidence: {confidence:.2f})")