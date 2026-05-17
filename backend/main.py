from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import os
import pandas as pd
import numpy as np

app = FastAPI(title="Sarlaft IA API", version="1.0.0")

# Mock classes for simulation if models are missing
class MockModel:
    def predict_proba(self, X):
        return np.array([[0.1, 0.9]]) # 90% risk

class MockScaler:
    def transform(self, X):
        return X

# Global variables for model and scaler
model = None
scaler = None

@app.on_event("startup")
async def load_model():
    global model, scaler
    try:
        # These will be populated by Claude Code's training
        with open('models/xgboost_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('models/scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        print("Real model loaded successfully")
    except Exception as e:
        print(f"Loading simulation mode. Error: {e}")
        model = MockModel()
        scaler = MockScaler()

class Transaction(BaseModel):
    features: list[float]

@app.get("/")
def read_root():
    return {"status": "Sarlaft IA Backend Running", "mode": "Real" if not isinstance(model, MockModel) else "Simulation"}

@app.post("/predict")
def predict(tx: Transaction):
    # Convert features to DataFrame
    df = pd.DataFrame([tx.features])
    
    # Scale and predict
    X_scaled = scaler.transform(df)
    prob = model.predict_proba(X_scaled)
    
    risk_score = float(prob[0][1]) * 100
    
    return {
        "risk_score": risk_score,
        "is_suspicious": risk_score > 50,
        "mode": "Simulation" if isinstance(model, MockModel) else "Real"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
