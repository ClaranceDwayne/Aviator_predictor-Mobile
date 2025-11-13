from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from predictor import predict_multiplier
import subprocess

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

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
