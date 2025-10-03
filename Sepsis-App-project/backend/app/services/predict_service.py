import joblib
import os
from sklearn.preprocessing import StandardScaler

MODEL_PATH = "final_model.pkl"
SCALER_PATH = "scaler.pkl"

# Load model & scaler khi server start
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None

if os.path.exists(SCALER_PATH):
    scaler = joblib.load(SCALER_PATH)
else:
    scaler = None

def predict_sepsis(data):
    """Nhận list số, trả kết quả dự đoán"""
    if model is None or scaler is None:
        return {"error": "Model hoặc scaler chưa được load"}
    scaled_data = scaler.transform([data])
    pred = model.predict(scaled_data)[0]
    return {"prediction": int(pred)}
