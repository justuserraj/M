# Import the specific "brain" or model we want to use.
# A Decision Tree is great because it learns by creating "if-then" rules.
from sklearn.tree import DecisionTreeClassifier

# Step 1: Provide the Data (The "Experience")
# Features for our training emails: [count of "free", contains_link (1 for yes, 0 for no)]
# For example, [2, 1] means the word "free" appeared twice and it had a link.
features = [
    [2, 1],  # Has "free" twice, has a link -> Spam
    [1, 1],  # Has "free" once, has a link  -> Spam
    [0, 0],  # No "free", no link          -> Not Spam
    [0, 1],  # No "free", has a link       -> Not Spam
    [1, 0]   # Has "free" once, no link    -> Not Spam
]

# Labels: 1 means "Spam", 0 means "Not Spam". These correspond to the features above.
labels = [1, 1, 0, 0, 0]

# Step 2: Create the Model (The "Brain")
# We are creating a new, untrained Decision Tree model.
classifier = DecisionTreeClassifier()

# Step 3: Train the Model (The "Learning" Process)
# The .fit() method is the "learning" command.
# It analyzes the features and labels to find patterns.
classifier.fit(features, labels)

# --- The program has now learned! Let's test it. ---

# Create a new email to test:
# It has the word "free" 3 times and contains a link.
new_email_features = [[3, 1]]

# Ask the trained model to make a prediction.
prediction = classifier.predict(new_email_features)

# Print the result
if prediction[0] == 1:
    print("Prediction for the new email: This is SPAM! 🚫")
else:
    print("Prediction for the new email: This is not spam. ✅")

# Let's try another one: no "free", no link.
another_email = [[0, 0]]
prediction2 = classifier.predict(another_email)

if prediction2[0] == 1:
    print("Prediction for the second email: This is SPAM! 🚫")
else:
    print("Prediction for the second email: This is not spam. ✅")