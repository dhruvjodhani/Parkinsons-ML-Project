"""Load saved artifacts and test a real model prediction (no dummy output)."""

from pathlib import Path
import json
import sys

import joblib
import numpy as np

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

SAMPLE = {
    "Age": 65,
    "Gender": 1,
    "Ethnicity": 0,
    "EducationLevel": 2,
    "BMI": 24.5,
    "Smoking": 0,
    "AlcoholConsumption": 2.5,
    "PhysicalActivity": 3.0,
    "Diet": 7.0,
    "SleepQuality": 6.5,
    "FamilyHistoryParkinsons": 0,
    "BrainInjury": 0,
    "Hypertension": 0,
    "Diabetes": 0,
    "Depression": 0,
    "Stroke": 0,
    "SystolicBP": 125,
    "DiastolicBP": 80,
    "CholesterolTotal": 195.0,
    "CholesterolLDL": 115.0,
    "CholesterolHDL": 52.0,
    "CholesterolTriglycerides": 140.0,
    "UPDRS": 12.0,
    "MoCA": 26.5,
    "FunctionalAssessment": 7.5,
    "Tremor": 0,
    "Rigidity": 0,
    "Bradykinesia": 0,
    "Posture": 0,
    "SpeechProblems": 0,
    "SleepDisorders": 0,
    "Constipation": 0,
}


def main():
    for path in (MODEL_PATH, SCALER_PATH, FEATURE_PATH):
        if not path.exists():
            print(f"FAIL: missing file {path}")
            sys.exit(1)

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    feature_columns = list(joblib.load(FEATURE_PATH))

    print("Model loaded:", type(model).__name__)
    print("Scaler loaded:", type(scaler).__name__)
    print("Feature count:", len(feature_columns))
    print("Feature order:")
    print(feature_columns)

    row = np.array([[SAMPLE[name] for name in feature_columns]], dtype=float)
    scaled = scaler.transform(row)
    pred = int(model.predict(scaled)[0])
    proba = float(model.predict_proba(scaled)[0][1])

    result = {
        "prediction": pred,
        "predictionLabel": "Positive" if pred == 1 else "Negative",
        "probability": round(proba, 4),
    }
    print("Sample prediction (from saved model, not hardcoded):")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
