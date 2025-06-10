
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictions_store = []

class Prediction(BaseModel):
    time: str
    price: float
    prediction: float
    confidence: float

@app.post("/prediction")
def add_prediction(pred: Prediction):
    predictions_store.append(pred)
    if len(predictions_store) > 100:
        predictions_store.pop(0)
    return {"status": "ok"}

@app.get("/predictions", response_model=List[Prediction])
def get_predictions():
    return predictions_store

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
