from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from predictor import predict_multiplier
import subprocess
import os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Environment variables
PORT = int(os.getenv("PORT", "8000"))
TIMEOUT = int(os.getenv("SCRAPPER_TIMEOUT", "10000"))
MODEL_PATH = os.getenv("MODEL_PATH", "models/latest.pkl")
API_KEY = os.getenv("API_KEY")

@app.post("/start-scraper")
async def start_scraper(request: Request):
    data = await request.json()
    url = data["url"]
    subprocess.Popen(["node", "backend/scraper.js", url])
    return {"status": "Scraper started"}

@app.get("/predict")
def get_prediction():
    result = predict_multiplier()
    return result

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/env")
def show_env():
    return {
        "PORT": PORT,
        "SCRAPPER_TIMEOUT": TIMEOUT,
        "MODEL_PATH": MODEL_PATH,
        "API_KEY": "****" if API_KEY else None
    }
