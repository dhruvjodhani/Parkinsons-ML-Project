"""
Train Logistic Regression Model for Parkinson's Disease Prediction.
Excludes PatientID from training features and saves model artifacts.
"""

from pathlib import Path
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

from preprocessing import get_train_test_data, calculate_metrics

BASE_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_MODEL_DIR = BASE_DIR / "BACKEND" / "model"
ML_MODELS_DIR = BASE_DIR / "ML" / "MODELS"

def train_logistic_regression():
    data = get_train_test_data(scale=True)
    X_train_scaled = data["X_train_scaled"]
    X_test_scaled = data["X_test_scaled"]
    y_train = data["y_train"]
    y_test = data["y_test"]
    scaler = data["scaler"]
    feature_names = data["feature_names"]

    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]

    metrics = calculate_metrics("Logistic Regression", y_test, y_pred, y_prob)

    print("=== LOGISTIC REGRESSION RESULTS ===")
    for k, v in metrics.items():
        print(f"{k}: {v}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Save trained artifacts
    for target_dir in [BACKEND_MODEL_DIR, ML_MODELS_DIR]:
        target_dir.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, target_dir / "parkinsons_model.pkl")
        joblib.dump(scaler, target_dir / "scaler.pkl")
        joblib.dump(feature_names, target_dir / "feature_columns.pkl")
    
    print(f"\nSaved Logistic Regression artifacts to {BACKEND_MODEL_DIR} and {ML_MODELS_DIR}")
    return model, metrics

if __name__ == "__main__":
    train_logistic_regression()
