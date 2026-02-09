from pydantic import BaseModel
from typing import List, Dict


class PredictRequest(BaseModel):
    text: str


class PredictResponse(BaseModel):
    category: str
    probabilities: Dict[str, float]


class TrainExample(BaseModel):
    text: str
    label: str


class TrainRequest(BaseModel):
    examples: List[TrainExample]


class TrainResponse(BaseModel):
    success: bool
    trained_on: int
