#!pip install streamlit

import streamlit as st
from transformers import pipeline
import random

# Load the emotion classification model once
@st.cache_resource
def load_model():
    return pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=False)

emotion_model = load_model()

# Response dictionary
dynamic_parts = {
    "bored": {
        "prefix": [
            "Feeling stuck or uninspired is okay.",
            "Boredom can be a gentle nudge for change.",
            "It's alright to feel a bit off or uninterested."
        ],
        "guidance": [
            "Try something playful — maybe doodle or dance to one song.",
            "How about starting a tiny project, even if it’s silly?",
            "Call a friend or write down three weird ideas — just for fun.",
            "Even a small change of environment — like moving to a window — can shift things.",
            "Think of one thing you’ve always wanted to try — maybe today’s the day to explore it!"
        ]
    },
    "anger": {
        "prefix": [
            "That sounds really frustrating.",
            "I hear your anger — it's valid.",
            "You're allowed to feel upset."
        ],
        "guidance": [
            "Let's pause for a slow breath together.",
            "Try unclenching your jaw and taking a breath.",
            "We don’t need to fix it — just be with it a moment."
        ]
    },
    "sadness": {
        "prefix": [
            "That feels heavy, I can tell.",
            "You sound really down right now.",
            "I’m here with you — even in this quiet sadness."
        ],
        "guidance": [
            "Let’s sit with this gently, no pressure to change it.",
            "Place a hand on your chest and just breathe with me.",
            "This feeling won’t last forever — but it’s okay for now."
        ]
    },
    "fear": {
        "prefix": [
            "That sounds overwhelming.",
            "It’s okay to feel scared sometimes.",
            "You’re safe right now."
        ],
        "guidance": [
            "Let’s ground you — feel your feet on the floor.",
            "Try a deep inhale through your nose… and exhale.",
            "Name one thing you can see and one thing you can touch."
        ]
    },
    "joy": {
        "prefix": [
            "That’s so wonderful to hear!",
            "Joy like this is a gift.",
            "I love that you're feeling this."
        ],
        "guidance": [
            "Take a moment to really soak it in.",
            "Let’s breathe it in fully and smile.",
            "Celebrate it — you deserve that feeling."
        ]
    },
    "love": {
        "prefix": [
            "That connection sounds beautiful.",
            "Love is such a powerful feeling.",
            "That warmth you’re feeling is precious."
        ],
        "guidance": [
            "Hold onto it and let it fill your chest.",
            "Just pause and feel it — it matters.",
            "Let’s stay with that good feeling for a bit."
        ]
    },
    "surprise": {
        "prefix": [
            "That sounds unexpected.",
            "Wow — that probably caught you off guard.",
            "That’s a lot to take in at once."
        ],
        "guidance": [
            "Let’s take a breath and process slowly.",
            "You don’t have to react right away.",
            "Pause for a moment — your body might need that."
        ]
    },
    "neutral": {
        "prefix": [
            "Thanks for checking in.",
            "It’s okay to just be in the moment.",
            "I’m here with you, no matter what."
        ],
        "guidance": [
            "Let’s take a quiet breath anyway.",
            "Even stillness deserves attention.",
            "This pause can be a kind one."
        ]
    }
}

# Manual override for boredom detection
def detect_emotion_with_keywords(text):
    lowered = text.lower()

    # Ego triggers
    ego_keywords = [
        "ego", "pride", "arrogant", "disrespect", "self-respect",
        "how dare", "they should respect", "better than", "insulted",
        "humiliated", "undermined", "they think i'm stupid", "they don't value me"
    ]

    # Revenge triggers
    revenge_keywords = [
        "revenge", "get back", "retaliate", "hurt them", "make them pay",
        "teach them a lesson", "they’ll regret", "vengeful", "punish them",
        "karma will get", "payback", "settle the score"
    ]

    if any(kw in lowered for kw in revenge_keywords):
        return "revenge"
    if any(kw in lowered for kw in ego_keywords):
        return "ego"

    # Fallback to model
    try:
        emotion_result = emotion_model(text)[0]
        return emotion_result['label'].lower()
    except:
        return "neutral"



# Generate calm response
def generate_response(emotion):
    parts = dynamic_parts.get(emotion, dynamic_parts["neutral"])
    return f"{random.choice(parts['prefix'])} {random.choice(parts['guidance'])}"

# Web app layout
st.set_page_config(page_title="CalmBot+", page_icon="🌿")
st.title("🌿 CalmBot – Your Emotional Support Companion")

user_input = st.text_input("Tell me how you're feeling right now:")

if user_input:
    emotion = detect_emotion_with_override(user_input)

    calm_reply = generate_response(emotion)

    st.markdown(f"**Detected Emotion:** `{emotion.capitalize()}`")
    st.success(calm_reply)
