import re
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay

BASE = Path(__file__).parent
data = pd.read_csv(BASE / "data" / "emails.csv")

def clean(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\.\S+", " URL ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

data["text"] = (data["subject"] + " " + data["body"]).apply(clean)

X_train, X_test, y_train, y_test = train_test_split(
    data["text"], data["label"], test_size=0.2, random_state=42, stratify=data["label"]
)

vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

pred = model.predict(X_test)

metrics = {
    "accuracy": accuracy_score(y_test, pred),
    "precision": precision_score(y_test, pred),
    "recall": recall_score(y_test, pred),
    "f1_score": f1_score(y_test, pred)
}

np.save(BASE / "models" / "test_predictions.npy", pred)

joblib.dump((vectorizer, model), BASE / "models" / "phishing_model.joblib")
(BASE / "models" / "metrics.json").write_text(json.dumps(metrics, indent=2))

cm = confusion_matrix(y_test, pred)
ConfusionMatrixDisplay(cm, display_labels=["Legitimate", "Phishing"]).plot()
plt.title("Phishing Email Detector")
plt.tight_layout()
plt.savefig(BASE / "models" / "confusion_matrix.png")
plt.close()

print("Model trained successfully")
for name, value in metrics.items():
    print(name + ":", round(value * 100, 2), "%")
