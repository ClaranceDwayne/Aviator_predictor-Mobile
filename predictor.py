import pandas as pd
import xgboost as xgb
import numpy as np
import os

MODEL_PATH = "backend/model.json"
DATA_PATH = "backend/rounds.csv"

def train_model():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("No training data found at rounds.csv")

    df = pd.read_csv(DATA_PATH)
    for i in range(1, 6):
        df[f"lag_{i}"] = df["multiplier"].shift(i)
    df = df.dropna()

    X = df[[f"lag_{i}" for i in range(1, 6)]]
    y = df["multiplier"]

    model = xgb.XGBRegressor(n_estimators=200, max_depth=5, learning_rate=0.05)
    model.fit(X, y)
    model.save_model(MODEL_PATH)
    print("✅ Model retrained and saved.")

def predict_multiplier(latest_rounds=[1.25, 3.40, 2.10, 1.80, 4.00]):
    if not os.path.exists(MODEL_PATH):
        return {"error": "Model not trained yet"}

    model = xgb.XGBRegressor()
    model.load_model(MODEL_PATH)

    X_input = np.array(latest_rounds).reshape(1, -1)
    prediction = model.predict(X_input)[0]
    confidence = 0.85
    return {"multiplier": round(float(prediction), 2), "confidence": confidence}
