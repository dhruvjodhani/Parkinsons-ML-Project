"""
Train Logistic Regression, save model/scaler/feature order, and print
comparison metrics for the other classifiers.

This script is the source of the deployed .pkl files used by the Flask API.
"""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

ROOT = Path(__file__).resolve().parent
MODEL_DIR = ROOT / "model"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

DATA_CANDIDATES = [
    ROOT / "Dataset" / "parkinsons_disease_data.csv",
    ROOT.parent / "ML-Project" / "parkinsons_disease_data.csv",
]


def resolve_data_path():
    for path in DATA_CANDIDATES:
        if path.exists():
            return path
    raise FileNotFoundError(
        "Could not find parkinsons_disease_data.csv. "
        "Place it in Dataset/ or keep it in ML-Project/."
    )


DATA_PATH = None


def load_clean_data():
    data_path = DATA_PATH or resolve_data_path()
    print("Loading:", data_path)
    df = pd.read_csv(data_path)
    unnamed = [c for c in df.columns if str(c).startswith("Unnamed")]
    if unnamed:
        df = df.drop(columns=unnamed)
    df = df.drop_duplicates()
    y = df["Diagnosis"]
    X = df.drop(columns=["Diagnosis", "PatientID"], errors="ignore")
    return X, y


def metrics_dict(name, y_true, y_pred, y_score):
    return {
        "Model": name,
        "Accuracy": round(accuracy_score(y_true, y_pred), 4),
        "Precision": round(precision_score(y_true, y_pred), 4),
        "Recall": round(recall_score(y_true, y_pred), 4),
        "F1": round(f1_score(y_true, y_pred), 4),
        "ROC-AUC": round(roc_auc_score(y_true, y_score), 4),
    }


def main():
    X, y = load_clean_data()
    feature_columns = X.columns.tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_train_scaled, y_train)

    joblib.dump(lr, MODEL_DIR / "parkinsons_model.pkl")
    joblib.dump(scaler, MODEL_DIR / "scaler.pkl")
    joblib.dump(feature_columns, MODEL_DIR / "feature_columns.pkl")

    print("Saved Logistic Regression model, scaler, and feature order.")
    print("Features:", feature_columns)

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
        "K-Nearest Neighbors": KNeighborsClassifier(),
        "Support Vector Machine": SVC(probability=True, random_state=42),
        "Naive Bayes": GaussianNB(),
    }

    rows = []
    for name, clf in models.items():
        clf.fit(X_train_scaled, y_train)
        pred = clf.predict(X_test_scaled)
        if hasattr(clf, "predict_proba"):
            score = clf.predict_proba(X_test_scaled)[:, 1]
        else:
            score = clf.decision_function(X_test_scaled)
        rows.append(metrics_dict(name, y_test, pred, score))

    results = pd.DataFrame(rows)
    print("\nModel comparison on the same 20% test set:")
    print(results.to_string(index=False))

    y_pred = lr.predict(X_test_scaled)
    y_score = lr.predict_proba(X_test_scaled)[:, 1]
    print("\nDeployed Logistic Regression test metrics:")
    print(metrics_dict("Logistic Regression", y_test, y_pred, y_score))


if __name__ == "__main__":
    main()
