import numpy as np

# --- 1. Activation Functions ---

def sigmoid(x):
    """The Sigmoid activation function (used for the final output layer)."""
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    """The derivative of the Sigmoid function."""
    return x * (1 - x)

def relu(x):
    """The Rectified Linear Unit (ReLU) activation function (used for hidden layers)."""
    return np.maximum(0, x)

def relu_derivative(x):
    """The derivative of the ReLU function."""
    return (x > 0) * 1 

# --- 2. Deep Neural Network (DNN) Architecture ---

class DeepNeuralNet:
    """A four-layer Deep Neural Network (Input -> H1 -> H2 -> Output)."""
    
    def __init__(self, input_size, hidden_size_1, hidden_size_2, output_size, learning_rate=0.5):
        
        # Hyperparameters
        self.learning_rate = learning_rate

        # Layer 1 (Input -> Hidden 1) - W1
        # Use small Gaussian weights (crucial for ReLU)
        self.weights_input_hidden1 = np.random.randn(input_size, hidden_size_1) * 0.01
        self.bias_hidden1 = np.zeros((1, hidden_size_1))

        # Layer 2 (Hidden 1 -> Hidden 2) - W2
        self.weights_hidden1_hidden2 = np.random.randn(hidden_size_1, hidden_size_2) * 0.01
        self.bias_hidden2 = np.zeros((1, hidden_size_2))

        # Layer 3 (Hidden 2 -> Output) - W3
        self.weights_hidden2_output = np.random.randn(hidden_size_2, output_size) * 0.01
        self.bias_output = np.zeros((1, output_size))


    def forward(self, input_data):
        """The Forward Pass: Data moves through two hidden layers."""
        
        # --- Layer 1 (Input -> H1) ---
        self.hidden1_input = np.dot(input_data, self.weights_input_hidden1) + self.bias_hidden1
        self.hidden1_output = relu(self.hidden1_input) 

        # --- Layer 2 (H1 -> H2) ---
        self.hidden2_input = np.dot(self.hidden1_output, self.weights_hidden1_hidden2) + self.bias_hidden2
        self.hidden2_output = relu(self.hidden2_input) 
        
        # --- Layer 3 (H2 -> Output) ---
        self.output_input = np.dot(self.hidden2_output, self.weights_hidden2_output) + self.bias_output
        final_output = sigmoid(self.output_input)

        return final_output

    def train(self, X, Y, epochs=1000):
        """The Learning Phase: Backpropagation through two hidden layers."""
        
        for epoch in range(epochs):
            # --- 1. FORWARD PASS ---
            output_prediction = self.forward(X)
            
            # --- 2. BACKPROPAGATION ---
            
            # Step 2a: Calculate Output Layer Error
            output_error = Y - output_prediction
            output_delta = output_error * sigmoid_derivative(output_prediction)

            # Step 2b: Calculate Hidden Layer 2 Error (Propagate W3 error back)
            hidden2_error = np.dot(output_delta, self.weights_hidden2_output.T)
            hidden2_delta = hidden2_error * relu_derivative(self.hidden2_input) 
            
            # Step 2c: Calculate Hidden Layer 1 Error (Propagate W2 error back)
            hidden1_error = np.dot(hidden2_delta, self.weights_hidden1_hidden2.T)
            hidden1_delta = hidden1_error * relu_derivative(self.hidden1_input) 
            
            # Step 2d: Update Weights and Biases 
            
            # W3 (H2 -> Output)
            adjustment_W3 = np.dot(self.hidden2_output.T, output_delta) * self.learning_rate
            self.weights_hidden2_output += adjustment_W3
            
            # W2 (H1 -> H2)
            adjustment_W2 = np.dot(self.hidden1_output.T, hidden2_delta) * self.learning_rate
            self.weights_hidden1_hidden2 += adjustment_W2

            # W1 (Input -> H1)
            adjustment_W1 = np.dot(X.T, hidden1_delta) * self.learning_rate
            self.weights_input_hidden1 += adjustment_W1
            
            # Update Biases
            self.bias_output += np.sum(output_delta, axis=0, keepdims=True) * self.learning_rate
            self.bias_hidden2 += np.sum(hidden2_delta, axis=0, keepdims=True) * self.learning_rate
            self.bias_hidden1 += np.sum(hidden1_delta, axis=0, keepdims=True) * self.learning_rate


            if epoch % 100 == 0:
                mean_error = np.mean(np.abs(output_error))
                print(f"Epoch {epoch}: Error = {mean_error:.4f}")