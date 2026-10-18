import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle
import re
import os

# ── Load your real dataset ─────────────────────────────────
df = pd.read_csv("ai/training_data.csv")

# Fix the typo in category column
df["category"] = df["category"].str.strip()
df["category"] = df["category"].replace("finanzial_fraud", "financial_fraud")

# Only keep complaint_text and category
df = df[["complaint_text", "category"]].dropna()
print(f"Total samples: {len(df)}")
print(df["category"].value_counts())

# ── Preprocessing ──────────────────────────────────────────
def preprocess(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df["clean_text"] = df["complaint_text"].apply(preprocess)

# ── Train / test split ─────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    df["clean_text"], df["category"],
    test_size=0.2, random_state=42, stratify=df["category"]
)

# ── TF-IDF Vectorizer ──────────────────────────────────────
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    min_df=2,
    sublinear_tf=True
)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec  = vectorizer.transform(X_test)

# ── Logistic Regression ────────────────────────────────────
model = LogisticRegression(max_iter=1000, C=1.0, class_weight="balanced")
model.fit(X_train_vec, y_train)

# ── Evaluation ─────────────────────────────────────────────
y_pred = model.predict(X_test_vec)
print("\n=== Model Evaluation ===")
print(classification_report(y_test, y_pred))

# ── Save model ─────────────────────────────────────────────
os.makedirs("ai/model", exist_ok=True)
with open("ai/model/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)
with open("ai/model/classifier.pkl", "wb") as f:
    pickle.dump(model, f)

print("\nModel saved to ai/model/")
print("Vectorizer saved to ai/model/")