import numpy as np
from neural_net import DeepNeuralNet # <--- IMPORTING THE NEW CLASS

# --- 1. Define Training Data (The XOR Gate) ---
X = np.array([
    [0, 0], 
    [0, 1], 
    [1, 0], 
    [1, 1]  
])
Y = np.array([
    [0],
    [1],
    [1],
    [0]
])

# --- 2. Initialize the Deep Neural Network ---
# Defining the shape of our DNN: Input -> H1 -> H2 -> Output

INPUT_SIZE = 2 
HIDDEN_SIZE_1 = 10 # First Hidden Layer
HIDDEN_SIZE_2 = 10 # Second Hidden Layer (The 'Deep' part!)
OUTPUT_SIZE = 1 

# Create an instance of your custom Deep Network
net = DeepNeuralNet(INPUT_SIZE, HIDDEN_SIZE_1, HIDDEN_SIZE_2, OUTPUT_SIZE, learning_rate=0.5)

# --- 3. Train the Network ---
print("Starting training on the XOR dataset (Deep Network)...")
# We only need 5000 epochs now, as deep networks can learn faster.
net.train(X, Y, epochs=5000) 
print("Training complete!")

# --- 4. Test the Network (Make Predictions) ---
print("\n--- Deep Network Predictions After Training ---")

for i in range(len(X)):
    input_data = X[i]
    prediction = net.forward(input_data) 
    rounded_prediction = np.round(prediction)

    print(f"Input: {input_data} | Target: {Y[i].item()} | Prediction: {prediction.item():.4f} (Rounded: {rounded_prediction.item()})")