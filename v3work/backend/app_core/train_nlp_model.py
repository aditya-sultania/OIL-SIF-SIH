import pandas as pd
import numpy as np
import spacy
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    """Clean and lemmatize raw text using spaCy."""
    doc = nlp(str(text).lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and token.is_alpha]
    return " ".join(tokens)

# 1. Synthetic Training Data (Realistic Safety Incident Descriptions)
training_data = [
    # Low / Medium Risk Examples
    ("Worker dropped pencil in office area", "Low/Medium Risk"),
    ("Trash bin overflowing near hallway entrance", "Low/Medium Risk"),
    ("Minor water spill on cafeteria floor", "Low/Medium Risk"),
    ("Operator forgot to wear safety glasses during inspection", "Low/Medium Risk"),
    ("Worker slipped on wet tile but did not fall", "Low/Medium Risk"),
    ("Storage box left blocking secondary walkway", "Low/Medium Risk"),
    
    # High Risk / SIF Precursor Examples
    ("Worker entered confined vessel without permit or air monitoring", "High Risk (SIF Precursor)"),
    ("Heavy pipe swung near workers during crane lift due to snap link failure", "High Risk (SIF Precursor)"),
    ("Technician bypassed pressure safety valve while pipeline was pressurized", "High Risk (SIF Precursor)"),
    ("Contractor worked at 20ft height without wearing fall protection harness", "High Risk (SIF Precursor)"),
    ("Gas leak alarm triggered near main refinery furnace", "High Risk (SIF Precursor)"),
    ("High pressure line ruptured during hydrotest causing violent recoil", "High Risk (SIF Precursor)")
]

df = pd.DataFrame(training_data, columns=["description", "risk_level"])

print("🧹 Preprocessing text with spaCy...")
df['clean_description'] = df['description'].apply(clean_text)

# 2. Extract Features using TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['clean_description'])
y = df['risk_level']

# 3. Train Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

print("⚡ Model trained successfully!")

# 4. Save trained Model and Vectorizer to disk
joblib.dump(model, 'sif_classifier_model.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')
print("💾 Model artifacts saved to 'sif_classifier_model.pkl' and 'tfidf_vectorizer.pkl'!")

# 5. Quick Test on Unseen Text
test_incident = "Worker was seen standing under suspended load without wearing hard hat"
clean_test = clean_text(test_incident)
test_vector = vectorizer.transform([clean_test])
prediction = model.predict(test_vector)[0]
confidence = np.max(model.predict_proba(test_vector)) * 100

print("--------------------------------------------------")
print(f"🧪 Test Incident: '{test_incident}'")
print(f"🤖 AI Prediction: {prediction} ({confidence:.1f}% confidence)")
print("--------------------------------------------------")