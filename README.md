# 🧑‍⚕️ Emotion-Aware Medical Chatbot

> A multilingual, AI-powered medical chatbot that detects user emotions and responds with empathy — built with DistilRoBERTa, Streamlit, OpenFDA, and NetworkX.

---

## 📌 Overview

The **Emotion-Aware Medical Chatbot** sits at the intersection of emotional health and medical diagnosis. As telemedicine and digital health assistants grow in adoption, the need for emotionally intelligent tools has never been greater. This chatbot addresses that gap by:

- Detecting the **emotional state** of the user in real time
- Providing **empathetic, context-aware** medical responses
- Supporting interaction in **any language**
- Visualising symptom–condition–drug relationships as a **knowledge graph**

> ⚠️ **Disclaimer:** This chatbot is intended for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment.

---

## 🚀 Features

### 💬 Conversational Interface
- Interactive chat UI built with **Streamlit**
- Users describe symptoms in natural language
- Responses are contextual and empathy-driven

### 😊 Emotion Detection
Powered by [`j-hartmann/emotion-english-distilroberta-base`](https://huggingface.co/j-hartmann/emotion-english-distilroberta-base) — a fine-tuned DistilRoBERTa model.

| Emotion   | Empathetic Prefix |
|-----------|-------------------|
| Sadness   | "I'm really sorry you're feeling this way." |
| Joy       | "I'm glad you're feeling good." |
| Fear      | "That sounds concerning. Let's go through this together." |
| Anger     | "I understand this can be frustrating." |
| Surprise  | "That's unexpected. Let's look into it." |
| Love      | "That's wonderful to hear." |
| Neutral   | *(no prefix)* |

### 🌍 Multilingual Support
Full translation pipeline using the **Google Translate API**:

```
User input (any language)
       ↓
Translate → English
       ↓
Emotion detection + Response generation
       ↓
Translate back → User's language
       ↓
Final response
```

### 🧠 Symptom Analysis & Medical Advice
Keyword-based NLP extracts symptoms and correlates them with user profile data (age, medical history) to generate personalised advice.

| Symptom Combination     | Suggested Condition           |
|-------------------------|-------------------------------|
| Headache + Fever        | Viral infection / Flu         |
| Dizziness               | Dehydration / Low blood pressure |
| Fatigue                 | Anaemia / Stress              |

### 💊 OpenFDA Drug Lookup
- Queries the **[OpenFDA API](https://open.fda.gov)** in real time
- Returns relevant drug associations for identified conditions
- Results are integrated into the knowledge graph

### 🕸️ Knowledge Graph Visualisation
- Built with **NetworkX** and rendered via **Matplotlib**
- Dynamically generated per conversation turn
- Visualises **Symptom → Condition → Drug** relationships

### 📊 Emotion Analytics
- Tracks detected emotions across the full conversation session
- Rendered as an interactive **bar chart** inside the Streamlit UI

### 🔊 Text-to-Speech (Optional)
- Responses can be spoken aloud using **pyttsx3**
- Runs locally with no external API calls

---

## 🏗️ Architecture

```
User Input
    │
    ├──► Google Translate API   →  English Text
    │
    ├──► DistilRoBERTa          →  Detected Emotion
    │
    ├──► Symptom Extractor      →  Symptoms List
    │         │
    │         ├──► User Profile →  Personalised Advice
    │         │
    │         └──► OpenFDA API  →  Drug Information
    │
    ├──► Response Generator     →  Empathy-Aware Response
    │         │
    │         └──► Google Translate → Response in User's Language
    │
    └──► NetworkX               →  Knowledge Graph (Streamlit)
```

---

## 🛠️ Tech Stack

| Component              | Technology |
|------------------------|------------|
| Frontend               | Streamlit |
| Emotion Detection      | HuggingFace Transformers (DistilRoBERTa) |
| Translation            | Google Translate API (`googletrans`) |
| Drug Information       | OpenFDA REST API |
| Knowledge Graph        | NetworkX + Matplotlib |
| Text-to-Speech         | pyttsx3 |
| Language               | Python 3.9+ |

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/emotion-aware-medical-chatbot.git
cd emotion-aware-medical-chatbot
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

---

## 📦 Requirements

```txt
streamlit
transformers
torch
googletrans==4.0.0-rc1
networkx
matplotlib
pandas
requests
pyttsx3
```

---

## 📁 Project Structure

```
emotion-aware-medical-chatbot/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md
│
├── modules/
│   ├── emotion.py          # Emotion detection pipeline
│   ├── translator.py       # Translation utilities
│   ├── symptom_extractor.py# Keyword-based symptom NLP
│   ├── drug_lookup.py      # OpenFDA API integration
│   └── knowledge_graph.py  # NetworkX graph generation
│
└── assets/
    └── screenshots/        # UI screenshots for documentation
```

---

## 🔭 Future Scope

- [ ] Replace heuristic rules with a full **LLM backend** (e.g. BioMedLM, MedPaLM)
- [ ] Named Entity Recognition (**NER**) for more robust symptom extraction
- [ ] **Offline mode** with on-device models
- [ ] Mobile app or **AR-based** interface
- [ ] Integration with **electronic health records (EHR)** systems
- [ ] Clinician review workflow and audit logging

---

## 👤 Author

| Name | ID |
|------|----|
| Noel Cleetus | 2022A7PS0906U |


---

## 📚 References

- [HuggingFace — emotion-english-distilroberta-base](https://huggingface.co/j-hartmann/emotion-english-distilroberta-base)
- [OpenFDA API](https://open.fda.gov)
- [Streamlit Documentation](https://streamlit.io)
- [NetworkX](https://networkx.org)
- [Google Translate API (googletrans)](https://pypi.org/project/googletrans/)
- [pyttsx3](https://pypi.org/project/pyttsx3/)

---

## 📄 License

This project was developed as an academic submission. Please contact the authors before reusing or redistributing any part of this work.
