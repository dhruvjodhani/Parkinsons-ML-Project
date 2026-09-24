"""
Train Decision Tree Classifier for Parkinson's Disease Prediction.
Excludes PatientID from features and computes metrics.
"""

from pathlib import Path
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix

from preprocessing import get_train_test_data, calculate_metrics

def train_decision_tree():
    # Decision Trees are invariant to monotonic feature scaling, but we use scaled or unscaled features
    data = get_train_test_data(scale=False)
    X_train = data["X_train"]
    X_test = data["X_test"]
    y_train = data["y_train"]
    y_test = data["y_test"]

    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = calculate_metrics("Decision Tree", y_test, y_pred, y_prob)

    print("=== DECISION TREE RESULTS ===")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    return model, metrics

if __name__ == "__main__":
    train_decision_tree()
