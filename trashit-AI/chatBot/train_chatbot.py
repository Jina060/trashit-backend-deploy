import json
import os
import dill
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from utils import preprocess_text

# Load question-intents dataset
with open('data/question_intents.json', 'r') as f:
    question_intents = json.load(f)

#prepare dataset
X, y = [], []

for item in question_intents:
    if 'intent' not in item:
        print("Missing 'intent' key in item:", item)
    else:
        intent = item['intent']
    for question in item['questions']:
        X.append(question)
        y.append(intent)

# Create vectorizer with custom preprocessor
vectorizer = TfidfVectorizer(preprocessor=preprocess_text)

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the pipeline
pipeline = Pipeline([
    ('vectorizer', vectorizer),
    ('classifier', LogisticRegression(max_iter=1000))
])

# Train the model
pipeline.fit(X_train, y_train)

# Evaluate
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy * 100:.2f}%")

# Save the model
os.makedirs('model', exist_ok=True)
with open('model/chatbot_model.pkl', 'wb') as f:
    dill.dump(pipeline, f)

print("Training complete. Model saved to model/chatbot_model.pkl.")
