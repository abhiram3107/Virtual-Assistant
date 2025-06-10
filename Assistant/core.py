import json
import random
import numpy as np
from pathlib import Path

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VA.settings')
django.setup()


# import speech_recognition as sr   # Commented out speech recognition library
# import pyttsx3   # Commented out text-to-speech library
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize text-to-speech engine 
# engine = pyttsx3.init()
# engine.setProperty('rate', 150)  # Adjust speech speed

# Load pre-trained Sentence-BERT model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Define dataset path using cross-platform compatibility
BASE_DIR = Path(__file__).resolve().parent.parent 
DATASET_PATH = BASE_DIR / "Assistant" / "data" / "dataset.json"

# # Load the navigation data, including basic conversations and navigation paths
# with open(r'Assistant\\data\\dataset.json', 'r', encoding="utf-8") as f:
#     navigation_data = json.load(f)

print(f"Loading dataset from: {DATASET_PATH}")

# Load the navigation data, including basic conversations and navigation paths
with open(DATASET_PATH, 'r', encoding="utf-8") as f:
    navigation_data = json.load(f)

# Extract user queries, responses, and corresponding navigation paths
queries = [entry['user_query'] for entry in navigation_data]
responses = {entry['user_query']: entry.get('response', None) for entry in navigation_data}
navigation_paths = {entry['user_query']: entry.get('navigation_path', None) for entry in navigation_data}

SIMILARITY_THRESHOLD = 0.5

# Function to convert text to speech 
'''def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to get voice input from the user
def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
        try:
            audio = recognizer.listen(source)
            user_input = recognizer.recognize_google(audio)
            print(f"User said: {user_input}")
            return user_input
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand. Please try again.")
            return None
        except sr.RequestError:
            print("Network error. Please check your internet connection.")
            return None'''


# Function to get the best matching navigation path or response
def get_navigation_path(user_input):
    if user_input in responses and responses[user_input]:
        return responses[user_input], 'general'
    
    if user_input in navigation_paths and navigation_paths[user_input]:
        return f"{navigation_paths[user_input]}", 'navigation'
    
    user_query_embedding = model.encode([user_input])
    queries_embeddings = model.encode(queries)
    similarities = cosine_similarity(user_query_embedding, queries_embeddings)
    
    best_match_idx = np.argmax(similarities)
    best_similarity = similarities[0][best_match_idx]
    
    if best_similarity < SIMILARITY_THRESHOLD:
        return "Sorry, I couldn't find a relevant answer. Please enter a valid query or try rephrasing.", 'general'
    
    matched_query = queries[best_match_idx]
    if matched_query in responses and responses[matched_query]:
        return responses[matched_query], 'general'
    elif matched_query in navigation_paths and navigation_paths[matched_query]:
        return f"{navigation_paths[matched_query]}", 'navigation'
    else:
        return "Sorry, I couldn't find a relevant answer. Please enter a valid query or try rephrasing.", 'general'

# Main function to process user input
from Assistant.handlers.router import route_query
from users.models.user import User
from django.core.exceptions import ObjectDoesNotExist

def process_user_input(user_input, username=None):
    if not user_input.strip():
        return "Please enter your query."

    # Try to fetch the user if a username is provided
    user = None
    if username:
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return "No such user found. Please check the username."

    # Step 1: Try matching using direct dataset queries (fast path)
    if user_input in responses and responses[user_input]:
        return responses[user_input]
    if user_input in navigation_paths and navigation_paths[user_input]:
        path = navigation_paths[user_input]
        return random.choice([
            f"You can find it in {path}. Do you want me to assist you in anything else?",
            f"The {path} section has what you're looking for. Do you want me to assist you in anything else?",
            f"Check out the {path} for more details. Do you want me to assist you in anything else?"
        ])

    # Step 2: Try Smart Reply if it's not a known direct query
    smart_reply = route_query(user_input, user=user)
    if smart_reply:
        return smart_reply

    # Step 3: Semantic similarity matching
    result, query_type = get_navigation_path(user_input)
    if query_type == 'navigation':
        return random.choice([
            f"You can find it in {result}. Do you want me to assist you in anything else?",
            f"The {result} section has what you're looking for. Do you want me to assist you in anything else?",
            f"Check out the {result} for more details. Do you want me to assist you in anything else?"
        ])
    else:
        return result



# Main interaction loop
def main():
    while True:
        print("\nType 'exit' to quit.")
        user_input = input("Your query: ")  # Using text input instead of voice input
        
        if user_input.lower() == "exit":
            print("Goodbye!")
            # speak("Goodbye!")  # Commented out speak function
            break
        
        response = process_user_input(user_input)
        print("Assistant:", response)
        # speak(response)  # Commented out speak function

if __name__ == "__main__":
    main()





