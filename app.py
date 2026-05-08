import streamlit as st
from transformers import pipeline
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from googletrans import Translator
import requests
import pyttsx3

# Load Emotion Detection Model
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

# Translator for multilingual support
translator = Translator()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "emotion_log" not in st.session_state:
    st.session_state.emotion_log = []

# Streamlit App UI
st.title("🧑‍⚕️ Emotion-Aware Medical Chatbot (Text & Multilingual)")
st.markdown("""
<style>
    .stChatMessage { font-size: 16px; }
</style>
""", unsafe_allow_html=True)

# Text-to-speech (optional)
def speak(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except:
        pass

# Emotion handling
def detect_emotion(text):
    result = emotion_classifier(text)[0]
    st.session_state.emotion_log.append(result['label'])
    return result['label']

def add_empathy(response, emotion):
    empathy_phrases = {
        "sadness": "I'm really sorry you're feeling this way. ",
        "joy": "I'm glad you're feeling good. ",
        "love": "That's wonderful to hear. ",
        "anger": "I understand this can be frustrating. ",
        "fear": "That sounds concerning. Let's take a deep breath and go through this together. ",
        "surprise": "That's unexpected. Let's look into it. ",
        "neutral": ""
    }
    return empathy_phrases.get(emotion.lower(), "") + response

# Translate input to English and back
def translate_to_english(text):
    try:
        return translator.translate(text, dest='en').text
    except:
        return text

def translate_back(text, src_lang='auto'):
    try:
        return translator.translate(text, dest=translator.detect(text).lang).text
    except:
        return text

# Expanded symptom keyword mapping
symptom_keywords = {
    "headache": ["headache", "head hurts", "head pain", "migraine"],
    "fever": ["fever", "temperature", "high temp", "chills", "cold", "hot"],
    "fatigue": ["fatigue", "tired", "tiredness", "weak", "weakness", "lazy", "exhausted", "no energy"],
    "dizziness": ["dizziness", "dizzy", "lightheaded", "spinning"],
    "cough": ["cough", "coughing", "throat"],
    "nausea": ["nausea", "nauseous", "vomiting", "vomit", "sick"],
    "body ache": ["body ache", "body pain", "neck hurts", "neck pain", "muscle pain", "aching"],
}

def extract_symptoms(text):
    found = []
    text_lower = text.lower()
    for symptom, keywords in symptom_keywords.items():
        if any(kw in text_lower for kw in keywords):
            found.append(symptom)
    return found

# OpenFDA drug lookup
def get_fda_drugs(symptoms):
    drugs_found = []
    condition_map = {
        "fever": "fever",
        "headache": "headache",
        "fatigue": "fatigue",
        "cough": "cough",
        "dizziness": "dizziness",
        "nausea": "nausea",
        "body ache": "pain"
    }
    for symptom in symptoms:
        query = condition_map.get(symptom, symptom)
        try:
            url = f"https://api.fda.gov/drug/label.json?search=indications_and_usage:{query}&limit=3"
            response = requests.get(url, timeout=5)
            data = response.json()
            for result in data.get("results", []):
                brand = result.get("openfda", {}).get("brand_name", [])
                generic = result.get("openfda", {}).get("generic_name", [])
                if brand:
                    drugs_found.append(brand[0])
                elif generic:
                    drugs_found.append(generic[0])
        except:
            pass
    return list(dict.fromkeys(drugs_found)) if drugs_found else []

# Response logic (expanded)
def get_bot_response(user_input):
    symptoms = extract_symptoms(user_input)

    if not symptoms:
        return "Thank you for sharing. Please provide more symptoms so I can help better."

    if "fever" in symptoms and "headache" in symptoms:
        return "Fever with headache may indicate a viral infection like the flu. Rest, stay hydrated, and take paracetamol if needed. See a doctor if fever exceeds 39°C."
    if "fever" in symptoms and "fatigue" in symptoms:
        return "Fever with fatigue and weakness is commonly seen in viral infections or flu. Rest and fluids are key. Monitor your temperature closely."
    if "fever" in symptoms and "body ache" in symptoms:
        return "Fever with body aches and neck pain could indicate flu or in rare cases meningitis. If neck stiffness is severe, seek medical attention promptly."
    if "fatigue" in symptoms and "body ache" in symptoms:
        return "Fatigue with body weakness and pain is common with viral infections, anaemia, or overexertion. Rest and ensure you are eating and drinking enough."
    if "headache" in symptoms:
        return "Headaches can be caused by dehydration, stress, or migraines. Drink water, rest in a dark room, and take a mild painkiller if needed."
    if "fever" in symptoms:
        return "A high temperature usually indicates your body is fighting an infection. Rest, stay hydrated, and monitor your fever. See a doctor if it persists over 3 days."
    if "fatigue" in symptoms:
        return "Fatigue and weakness are common symptoms of anaemia, stress, or viral illness. Ensure you are sleeping well and eating a balanced diet."
    if "dizziness" in symptoms:
        return "Dizziness could be related to dehydration, low blood pressure, or inner ear issues. Sit down, drink water, and avoid sudden movements."
    if "nausea" in symptoms:
        return "Nausea can be caused by infections, food poisoning, or stress. Stay hydrated with small sips of water and avoid heavy meals."
    if "body ache" in symptoms:
        return "Body aches and neck pain can be due to muscle strain, poor posture, or a viral infection. Rest and gentle stretching may help."
    if "cough" in symptoms:
        return "A persistent cough may indicate a respiratory infection or bronchitis. Stay hydrated and consider steam inhalation. See a doctor if it lasts more than a week."

    return f"You mentioned: {', '.join(symptoms)}. These symptoms could have several causes. Please consult a doctor for a proper diagnosis."

# Knowledge Graph
symptom_graph = {
    "fever": ["flu", "infection", "covid"],
    "cough": ["flu", "bronchitis", "asthma"],
    "headache": ["migraine", "flu", "dehydration"],
    "fatigue": ["anemia", "flu", "depression"],
    "dizziness": ["low blood pressure", "anemia", "dehydration"],
    "nausea": ["gastroenteritis", "food poisoning"],
    "body ache": ["flu", "fibromyalgia", "viral infection"],
}

def draw_graph(text):
    symptoms = extract_symptoms(text)
    if not symptoms:
        st.info("No symptoms matched for the graph.")
        return
    G = nx.Graph()
    for s in symptoms:
        if s in symptom_graph:
            for d in symptom_graph[s]:
                G.add_edge(s, d)
    if G.number_of_edges() == 0:
        st.info("No symptoms matched for the graph.")
        return
    fig, ax = plt.subplots()
    nx.draw(G, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, ax=ax)
    st.pyplot(fig)

# Chat Display
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Text input
user_input = st.chat_input("Type your symptoms or concerns in any language...")
if user_input:
    translated_input = translate_to_english(user_input)
    emotion = detect_emotion(translated_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    bot_raw = get_bot_response(translated_input)
    bot_final = add_empathy(bot_raw, emotion)
    translated_output = translate_back(bot_final)
    st.session_state.messages.append({"role": "assistant", "content": translated_output})
    with st.chat_message("assistant"):
        st.write(translated_output)

    # OpenFDA drug lookup
    detected_symptoms = extract_symptoms(translated_input)
    if detected_symptoms:
        with st.spinner("Looking up medications from OpenFDA..."):
            fda_drugs = get_fda_drugs(detected_symptoms)
        if fda_drugs:
            st.markdown("💊 **Related medications from OpenFDA:**")
            for drug in fda_drugs[:5]:
                st.markdown(f"- {drug}")
        else:
            st.info("No matching drugs found in OpenFDA for these symptoms.")

    draw_graph(translated_input)
    speak(translated_output)

# Emotion chart
if st.session_state.emotion_log:
    st.markdown("### 📊 Emotion Trend")
    df = pd.DataFrame({"Emotion": st.session_state.emotion_log})
    st.bar_chart(df["Emotion"].value_counts())

# Watermark
st.markdown(
    """
    <style>
    .watermark {
        position: fixed;
        bottom: 10px;
        right: 10px;
        font-size: 18px;
        color: rgba(200, 200, 200, 0.3);
        z-index: 1000;
    }
    </style>
    <div class="watermark">©️ Noel Cleetus</div>
    """,
    unsafe_allow_html=True
)