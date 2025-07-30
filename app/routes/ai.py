from fastapi import APIRouter, Request
from pydantic import BaseModel
import random

router = APIRouter()

# In-memory history log
prediction_history = []

class PredictionInput(BaseModel):
    text: str

@router.post("/predict")
async def predict(input_data: PredictionInput):
    input_text = input_data.text
    sentiment = random.choice(["positive", "neutral", "negative"])
    confidence = round(random.uniform(0.85, 0.99), 2)
    message = f"The sentiment of your input is {sentiment} (confidence: {confidence})"

    result = {
        "input": input_text,
        "sentiment": sentiment,
        "confidence": confidence,
        "message": message
    }

    prediction_history.append(result)
    return result

@router.get("/history")
def get_history():
    return prediction_history
