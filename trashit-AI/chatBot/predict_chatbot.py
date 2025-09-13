import json
import dill  
import re
import string
import numpy as np
from sentence_transformers import SentenceTransformer, util
import random

def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Load trained intent classification model
with open("model/chatbot_model.pkl", "rb") as f:
    pipeline = dill.load(f)

# Load question-intents data
with open("data/question_intents.json", "r") as f:
    question_intents = json.load(f)

# Load separate answers file
with open("data/intents_responses.json", "r") as f:
    response_data = json.load(f)  # Dictionary: intent -> list of answers

# Load sentence-transformers model
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

# Prepare embeddings and question texts
intent_question_embeddings = {}
intent_question_texts = {}

for item in question_intents:
    intent = item["intent"]
    questions = item["questions"]
    
    processed_questions = [preprocess_text(q) for q in questions]
    question_embeddings = sbert_model.encode(processed_questions, convert_to_tensor=True)
    
    intent_question_embeddings[intent] = question_embeddings
    intent_question_texts[intent] = questions

def get_response(user_input):
    cleaned_input = preprocess_text(user_input)
    
    # Predict intent using the trained classifier
    probs = pipeline.predict_proba([cleaned_input])[0]
    predicted_intent = pipeline.classes_[probs.argmax()]
    confidence = probs.max()
    
    if confidence < 0.1:
        return "Sorry, I didn't quite get that. Could you rephrase?"

    # Use sentence similarity to find best matching question
    questions = intent_question_texts.get(predicted_intent, [])
    embeddings = intent_question_embeddings.get(predicted_intent, [])
    
    if not questions or len(embeddings) == 0:
        return "Hmm, I understand the intent but don’t have any related questions for it."

    user_embedding = sbert_model.encode(cleaned_input, convert_to_tensor=True)
    similarities = util.cos_sim(user_embedding, embeddings)[0]
    
    best_match_idx = int(np.argmax(similarities))

    # Get matching answer from separate responses file
    answers = response_data.get(predicted_intent, ["Sorry, I don’t have a good answer for that."])
    
    return random.choice(answers)

# Run chatbot interaction loop
print("🟢 TrashIt Chatbot is online! (type 'quit' to exit)")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit", "bye"]:
        print("TrashBot: Goodbye! 👋")
        break
    response = get_response(user_input)
    print("TrashBot:", response)
