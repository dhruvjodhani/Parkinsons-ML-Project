"""
Common preprocessing module for Parkinson's Disease Prediction ML project.
Provides reusable functions for data loading, cleaning, feature-target separation,
train-test splitting, scaling, and evaluation metric calculations.
"""

from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def resolve_dataset_path(data_path=None):
    if data_path is not None and Path(data_path).exists():
        return Path(data_path)
    
    candidates = [
        BASE_DIR / "ML" / "DATASET" / "parkinsons_dataset.csv",
        BASE_DIR / "ML" / "DATASET" / "parkinsons_disease_data.csv",
        BASE_DIR / "Dataset" / "parkinsons_disease_data.csv",
        BASE_DIR.parent / "ML-Project" / "parkinsons_disease_data.csv"
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError("Could not locate parkinsons_dataset.csv in ML/DATASET/.")

def load_clean_data(data_path=None):
    """
    Loads raw dataset, cleans empty/unnamed columns, removes duplicates,
    excludes PatientID identifier column, and separates features X and target y.
    
    Returns:
        X (pd.DataFrame): 32 clinical feature columns (PatientID excluded)
        y (pd.Series): Target Diagnosis column (0 or 1)
    """
    path = resolve_dataset_path(data_path)
    df = pd.read_csv(path)
    
    # Drop trailing empty/unnamed columns
    unnamed_cols = [c for c in df.columns if str(c).startswith("Unnamed")]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)
        
    # Drop duplicate rows
    df = df.drop_duplicates()
    
    if "Diagnosis" not in df.columns:
        raise KeyError("Target column 'Diagnosis' not found in dataset.")
        
    y = df["Diagnosis"]
    
    # Exclude PatientID and Diagnosis from features
    X = df.drop(columns=["Diagnosis", "PatientID"], errors="ignore")
    
    return X, y

def get_train_test_data(data_path=None, test_size=0.2, random_state=42, scale=True):
    """
    Performs train-test split (stratified by target) and optionally fits StandardScaler.
    
    Returns:
        dict containing:
            X_train, X_test, y_train, y_test,
            X_train_scaled, X_test_scaled, scaler, feature_names
    """
    X, y = load_clean_data(data_path)
    feature_names = list(X.columns)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    scaler = None
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    
    if scale:
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "X_train_scaled": X_train_scaled,
        "X_test_scaled": X_test_scaled,
        "scaler": scaler,
        "feature_names": feature_names
    }

def calculate_metrics(model_name, y_true, y_pred, y_prob=None):
    """
    Calculates standard binary classification performance metrics.
    """
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    
    roc_auc = None
    if y_prob is not None:
        try:
            roc_auc = roc_auc_score(y_true, y_prob)
        except Exception:
            roc_auc = None
            
    res = {
        "Model": model_name,
        "Accuracy": round(float(acc), 4),
        "Precision": round(float(prec), 4),
        "Recall": round(float(rec), 4),
        "F1 Score": round(float(f1), 4),
    }
    if roc_auc is not None:
        res["ROC-AUC"] = round(float(roc_auc), 4)
    return res
