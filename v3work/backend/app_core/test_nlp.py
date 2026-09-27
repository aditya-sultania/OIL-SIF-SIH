import spacy
import sklearn
import xgboost

# Load the English NLP model you just installed
nlp = spacy.load("en_core_web_sm")

sample_text = "Technician operated heavy machinery near water pump without wearing a safety harness."
doc = nlp(sample_text)

print("--------------------------------------------------")
print("🎉 NLP Setup Successful!")
print(f"Sample Incident Text: '{sample_text}'")
print("\nExtracted Keywords & Lemma Tokens:")
print([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])
print("--------------------------------------------------")