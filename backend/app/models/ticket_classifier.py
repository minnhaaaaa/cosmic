from typing import List, Dict, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.exceptions import NotFittedError
import joblib


class TicketClassifier:
    def __init__(self, labels: Optional[List[str]] = None):
        self.labels = labels or [
            "Billing",
            "Technical",
            "Account",
            "Feature",
            "Refund Request",
            "Service Complaint",
        ]
        self.pipeline: Optional[Pipeline] = None

    def build_pipeline(self) -> Pipeline:
        return Pipeline(
            [
                ("tfidf", TfidfVectorizer(min_df=1, ngram_range=(1, 2))),
                ("clf", LogisticRegression(max_iter=200)),
            ]
        )

    def train(self, texts: List[str], labels: List[str]):
        if not texts:
            raise ValueError("No training texts provided")
        self.pipeline = self.build_pipeline()
        self.pipeline.fit(texts, labels)

    def predict(self, text: str) -> Dict[str, object]:
        if self.pipeline is None:
            raise NotFittedError("Model is not trained yet")
        pred = self.pipeline.predict([text])[0]
        probs = self.pipeline.predict_proba([text])[0]
        label_probs = {label: float(prob) for label, prob in zip(self.pipeline.classes_, probs)}
        # Ensure all known labels exist in the probs mapping (zero if absent)
        for lbl in self.labels:
            label_probs.setdefault(lbl, 0.0)
        return {"category": pred, "probabilities": label_probs}

    def save(self, path: str):
        if self.pipeline is None:
            raise NotFittedError("Model is not trained yet")
        joblib.dump({"pipeline": self.pipeline, "labels": self.labels}, path)

    def load(self, path: str):
        data = joblib.load(path)
        self.pipeline = data["pipeline"]
        self.labels = data.get("labels", self.labels)
