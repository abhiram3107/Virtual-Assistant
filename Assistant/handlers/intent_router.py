# Assistant/handlers/intent_router.py

from sentence_transformers import SentenceTransformer, util
import torch

model = SentenceTransformer("all-MiniLM-L6-v2")

INTENTS = {
    # Student intents
    "get_progress": [
        "what's my progress", "how am I doing", "show my performance", 
        "give me a report card", "how did I perform"
    ],
    "get_advice": [
        "what should I improve", "where am I weak", "give me advice",
        "how can I do better", "suggest improvements"
    ],
    "get_attendance": [
        "what's my attendance", "show my attendance", "attendance summary",
        "how many classes did I attend", "how often was I present"
    ],


    # Teacher intents
    "teacher_progress": [
        "how is my class doing", "class performance", "analyze my students",
        "how are students performing", "subject-wise performance"
    ],
    "teacher_advice": [
        "how can my students improve", "teaching advice", "suggest improvements for class",
        "which topics need more attention", "class weaknesses"
    ],
    "teacher_attendance": [
        "show student attendance", "class attendance", "who attended classes",
        "how many sessions were held", "student attendance summary"
    ],



    # HOD intents
    "hod_progress": [
        "analyze department", "how is the department doing", "department performance",
        "subject wise accuracy", "branch performance"
    ],
    "hod_advice": [
        "how can department improve", "suggest improvements for department",
        "what's lacking in branch", "department weaknesses", 
        "what to improve at branch level"
    ],
    "hod_attendance": [
        "show department attendance", "department attendance summary", 
        "how are teachers and students attending classes", "attendance report"
    ]
}

def identify_intent(user_input, threshold=0.6):
    query_emb = model.encode(user_input, convert_to_tensor=True)
    best_score = 0
    best_intent = None

    for intent, phrases in INTENTS.items():
        intent_embs = model.encode(phrases, convert_to_tensor=True)
        score = torch.max(util.cos_sim(query_emb, intent_embs)).item()

        if score > best_score:
            best_score = score
            best_intent = intent

    return best_intent if best_score >= threshold else None
