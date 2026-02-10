from fastapi import FastAPI, HTTPException
import logging
from fastapi.middleware.cors import CORSMiddleware
from .models.ticket_classifier import TicketClassifier
from .schemas import PredictRequest, PredictResponse, TrainRequest, TrainResponse
from .data.sample_data import SAMPLE_TRAINING
from typing import List
import os


MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "model.joblib")

app = FastAPI(title="Ticket Classifier API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

classifier = TicketClassifier()

# basic logging for debugging predict flows
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def initial_train():
    texts, labels = zip(*SAMPLE_TRAINING)
    classifier.train(list(texts), list(labels))
    try:
        classifier.save(MODEL_PATH)
    except Exception:
        # ignore save errors for environments without write permissions
        pass


@app.on_event("startup")
def startup_event():
    # try load saved model, otherwise train on sample data
    try:
        if os.path.exists(MODEL_PATH):
            classifier.load(MODEL_PATH)
        else:
            initial_train()
    except Exception:
        # fallback to training on sample data
        initial_train()


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Empty text")
    try:
        result = classifier.predict(text)
        logger.info("Predict request: %s -> %s", text, result)
        return PredictResponse(category=result["category"], probabilities=result["probabilities"], label=result["category"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/train", response_model=TrainResponse)
def train(request: TrainRequest):
    examples = request.examples
    if not examples:
        raise HTTPException(status_code=400, detail="No training examples provided")
    texts = [ex.text for ex in examples]
    labels = [ex.label for ex in examples]
    classifier.train(texts, labels)
    try:
        classifier.save(MODEL_PATH)
    except Exception:
        pass
    return TrainResponse(success=True, trained_on=len(texts))


@app.get("/labels")
def get_labels():
    return {"labels": classifier.labels}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
