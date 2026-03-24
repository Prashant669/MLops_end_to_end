# main.py
import pandas as pd
from pathlib import Path
from fastapi import FastAPI
from joblib import load
from pydantic import BaseModel
from src.models.helper import clean_text

app = FastAPI()

class modelinput(BaseModel):
    text: str 

model_path = Path.cwd().as_posix() + '/models/sentiment_analysis.joblib'
tfidf_path = Path.cwd().as_posix() + '/models/tfidf.joblib'
model = load(model_path)
tfidf = load(tfidf_path)

@app.get("/")
def home():
    return "Welcome to Sentiment Analysis model!!! Hurray byou completed the first step"

@app.post("/sentiment_prediction")

def predict_sentiment(input_data:modelinput):

    text = input_data.text

    clean_data = clean_text(text)

    tfidf_transform = tfidf.transform([clean_data])

    prediction = model.predict(tfidf_transform)[0].item()

    if prediction == 0:
        return f"Sentiment for this movie is Negative😞😞😞"
    elif prediction == 1:
        return f"Sentiment for this movie is Positive😁😁😁"

  

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)







