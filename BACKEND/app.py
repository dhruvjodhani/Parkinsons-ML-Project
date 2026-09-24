"""
Flask prediction API for the Parkinson's educational ML project.

Loads the trained model, scaler, and feature order, then returns a
model prediction and probability. This is not a medical diagnosis.
"""

from pathlib import Path

import joblib
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS

BASE_DIR = Path(__file__).resolve().parent

def resolve_model_dir():
    candidates = [
        BASE_DIR / "model",
        BASE_DIR.parent / "ML" / "MODELS",
        BASE_DIR.parent / "model",
    ]
    for p in candidates:
        if (p / "parkinsons_model.pkl").exists():
            return p
    return BASE_DIR / "model"

MODEL_DIR = resolve_model_dir()
MODEL_PATH = MODEL_DIR / "parkinsons_model.pkl"
SCALER_PATH = MODEL_DIR / "scaler.pkl"
FEATURE_PATH = MODEL_DIR / "feature_columns.pkl"

# Ranges used by the React form. Backend validation should match.
FEATURE_RANGES = {
    "Age": (18, 100),
    "Gender": (0, 1),
    "Ethnicity": (0, 3),
    "EducationLevel": (0, 3),
    "BMI": (10, 60),
    "Smoking": (0, 1),
    "AlcoholConsumption": (0, 30),
    "PhysicalActivity": (0, 20),
    "Diet": (0, 10),
    "SleepQuality": (0, 10),
    "FamilyHistoryParkinsons": (0, 1),
    "BrainInjury": (0, 1),
    "Hypertension": (0, 1),
    "Diabetes": (0, 1),
    "Depression": (0, 1),
    "Stroke": (0, 1),
    "SystolicBP": (70, 230),
    "DiastolicBP": (40, 140),
    "CholesterolTotal": (80, 500),
    "CholesterolLDL": (30, 350),
    "CholesterolHDL": (15, 120),
    "CholesterolTriglycerides": (30, 600),
    "UPDRS": (0, 260),
    "MoCA": (0, 30),
    "FunctionalAssessment": (0, 10),
    "Tremor": (0, 1),
    "Rigidity": (0, 1),
    "Bradykinesia": (0, 1),
    "Posture": (0, 1),
    "SpeechProblems": (0, 1),
    "SleepDisorders": (0, 1),
    "Constipation": (0, 1),
}

# React (localhost:3000 from vite.config.js) talking to Flask on port 5000.
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": CORS_ORIGINS}})

model = None
scaler = None
feature_columns = None
load_error = None


def load_artifacts():
    """Load model, scaler, and feature order once at startup."""
    global model, scaler, feature_columns, load_error
    try:
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        feature_columns = list(joblib.load(FEATURE_PATH))
        load_error = None
    except Exception:
        model = None
        scaler = None
        feature_columns = None
        load_error = "Model files could not be loaded. Train the model and restart the backend."


load_artifacts()


def parse_numeric(name, value):
    if value is None or value == "":
        raise ValueError(f"Missing value for '{name}'.")
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"'{name}' must be a number.")
    if not np.isfinite(number):
        raise ValueError(f"'{name}' is not a valid number.")
    return number


def validate_and_order_features(payload):
    """Build a 1-row feature vector in the exact training column order."""
    if not isinstance(payload, dict):
        raise ValueError("Request body must be a JSON object.")

    values = []
    for name in feature_columns:
        if name not in payload:
            raise ValueError(f"Missing required field '{name}'.")

        number = parse_numeric(name, payload[name])
        low, high = FEATURE_RANGES.get(name, (None, None))
        if low is not None and number < low:
            raise ValueError(f"'{name}' must be at least {low}.")
        if high is not None and number > high:
            raise ValueError(f"'{name}' must be at most {high}.")
        values.append(number)

    return np.array(values, dtype=float).reshape(1, -1)


@app.get("/health")
def health():
    ready = model is not None and scaler is not None and feature_columns is not None
    return jsonify(
        {
            "status": "ok" if ready else "error",
            "modelLoaded": ready,
            "featureCount": len(feature_columns) if feature_columns else 0,
            "message": None if ready else load_error,
        }
    ), 200 if ready else 500


@app.post("/predict")
def predict():
    if model is None or scaler is None or feature_columns is None:
        return jsonify(
            {
                "error": load_error or "The prediction model is not available.",
            }
        ), 500

    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Send a JSON body with patient feature values."}), 400

    try:
        feature_row = validate_and_order_features(payload)
        scaled = scaler.transform(feature_row)
        prediction = int(model.predict(scaled)[0])
        # Probability of the positive class (Diagnosis = 1)
        probability = float(model.predict_proba(scaled)[0][1])
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "The server could not complete this prediction."}), 500

    label = "Positive" if prediction == 1 else "Negative"
    return jsonify(
        {
            "prediction": prediction,
            "predictionLabel": label,
            "probability": round(probability, 4),
            "message": "Model prediction for educational use only. This is not a medical diagnosis.",
        }
    ), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
