from django.shortcuts import render

# Create your views here.
import json
import dill as pickle
import random
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from utils import preprocess_text
from sentence_transformers import SentenceTransformer, util

# Load model
with open("chatbot/model/chatbot_model.pkl", "rb") as f:
    pipeline = pickle.load(f)

# Load questions and responses
with open("chatbot/data/question_intents.json", "r") as f:
    question_data = json.load(f)

with open("chatbot/data/intents_responses.json", "r") as f:
    response_data = json.load(f)

# Build intent/questions and answers mappings
intent_question_texts = {}
intent_question_embeddings = {}
intent_answers = {}

sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

# map: intent/list of responses
response_dict = response_data

for item in question_data:
    intent = item["intent"]
    questions = item["questions"]
    responses = response_dict.get(intent, ["Sorry, I don't have a response for that."])

    processed_questions = [preprocess_text(q) for q in questions]
    question_embeddings = sbert_model.encode(processed_questions, convert_to_tensor=True)

    intent_question_texts[intent] = questions
    intent_question_embeddings[intent] = question_embeddings
    intent_answers[intent] = responses

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_input = data.get('message', '')
        cleaned_input = preprocess_text(user_input)

        # Predict intent
        probs = pipeline.predict_proba([cleaned_input])[0]
        predicted_intent = pipeline.classes_[np.argmax(probs)]
        confidence = np.max(probs)

        if confidence < 0.1:
            return JsonResponse({'response': "Sorry, I didn't quite get that. Could you rephrase?"})

        # SBERT Similarity Matching
        questions = intent_question_texts[predicted_intent]
        answers = intent_answers[predicted_intent]
        embeddings = intent_question_embeddings[predicted_intent]

        user_embedding = sbert_model.encode(cleaned_input, convert_to_tensor=True)
        similarities = util.cos_sim(user_embedding, embeddings)[0]
        best_idx = int(np.argmax(similarities))

        reply = answers[best_idx] if best_idx < len(answers) else answers[0]
        return JsonResponse({'response': reply})

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)