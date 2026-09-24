"""
Train K-Nearest Neighbors Classifier for Parkinson's Disease Prediction.
Applies StandardScaler, tests k=3, 5, 7, 9, selects optimal k, and prints full evaluation.
"""

from pathlib import Path
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix

from preprocessing import get_train_test_data, calculate_metrics

def train_knn():
    data = get_train_test_data(scale=True)
    X_train_scaled = data["X_train_scaled"]
    X_test_scaled = data["X_test_scaled"]
    y_train = data["y_train"]
    y_test = data["y_test"]

    print("=== TESTING KNN WITH VARIOUS K VALUES ===")
    k_values = [3, 5, 7, 9]
    k_results = {}
    best_k = 5
    best_f1 = -1.0
    best_model = None

    for k in k_values:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train_scaled, y_train)
        pred = knn.predict(X_test_scaled)
        prob = knn.predict_proba(X_test_scaled)[:, 1]
        metrics_k = calculate_metrics(f"KNN (k={k})", y_test, pred, prob)
        k_results[k] = metrics_k
        print(f"k={k}: Accuracy={metrics_k['Accuracy']}, Precision={metrics_k['Precision']}, Recall={metrics_k['Recall']}, F1={metrics_k['F1 Score']}")
        
        if metrics_k['F1 Score'] > best_f1:
            best_f1 = metrics_k['F1 Score']
            best_k = k
            best_model = knn

    print(f"\nSelected Optimal K: {best_k}")
    best_pred = best_model.predict(X_test_scaled)
    best_prob = best_model.predict_proba(X_test_scaled)[:, 1]
    final_metrics = calculate_metrics("K-Nearest Neighbors", y_test, best_pred, best_prob)

    print("\n=== K-NEAREST NEIGHBORS (FINAL MODEL) RESULTS ===")
    for k, v in final_metrics.items():
        print(f"{k}: {v}")

    print("\nClassification Report:")
    print(classification_report(y_test, best_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, best_pred))

    return best_model, final_metrics, k_results

if __name__ == "__main__":
    train_knn()
