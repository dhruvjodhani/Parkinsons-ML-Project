# Parkinson's Prediction Backend

Lightweight Flask API that loads the trained scikit-learn model and returns a **model prediction** and **prediction probability**.

This is an educational project. It is **not** a medical diagnosis system.

## Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The API starts at `http://127.0.0.1:5000`.

The React frontend in this project uses Vite on **port 3000**. CORS is enabled for that origin.

## Endpoints

- `GET /health` — checks that the model, scaler, and feature list loaded
- `POST /predict` — runs a real model prediction

## Example request

```bash
python test_prediction.py
```

Or with curl:

```bash
curl -X POST http://127.0.0.1:5000/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"Age\":65,\"Gender\":1,\"Ethnicity\":0,\"EducationLevel\":2,\"BMI\":24.5,\"Smoking\":0,\"AlcoholConsumption\":2.5,\"PhysicalActivity\":3.0,\"Diet\":7.0,\"SleepQuality\":6.5,\"FamilyHistoryParkinsons\":0,\"BrainInjury\":0,\"Hypertension\":0,\"Diabetes\":0,\"Depression\":0,\"Stroke\":0,\"SystolicBP\":125,\"DiastolicBP\":80,\"CholesterolTotal\":195,\"CholesterolLDL\":115,\"CholesterolHDL\":52,\"CholesterolTriglycerides\":140,\"UPDRS\":12,\"MoCA\":26.5,\"FunctionalAssessment\":7.5,\"Tremor\":0,\"Rigidity\":0,\"Bradykinesia\":0,\"Posture\":0,\"SpeechProblems\":0,\"SleepDisorders\":0,\"Constipation\":0}"
```

## Status codes

- `200` successful prediction
- `400` invalid or missing input
- `500` model/server error

`PatientID` may be sent by the frontend, but it is **not** used as a model feature.
