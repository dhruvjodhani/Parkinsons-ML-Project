"""
Train and Compare all ML Models (Logistic Regression, Decision Tree, KNN) for Parkinson's Disease Prediction.
Generates model_comparison.csv, model_accuracy.csv, and model_accuracy.png in ML/RESULTS/.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from preprocessing import get_train_test_data, calculate_metrics
from train_logistic_regression import train_logistic_regression
from train_decision_tree import train_decision_tree
from train_knn import train_knn

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RESULTS_DIR = BASE_DIR / "ML" / "RESULTS"
CHARTS_DIR = RESULTS_DIR / "charts"

def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)

    print("==================================================")
    print("      TRAINING & EVALUATING ALL ML MODELS         ")
    print("==================================================\n")

    # 1. Logistic Regression
    lr_model, lr_metrics = train_logistic_regression()

    print("\n--------------------------------------------------\n")

    # 2. Decision Tree
    dt_model, dt_metrics = train_decision_tree()

    print("\n--------------------------------------------------\n")

    # 3. K-Nearest Neighbors
    knn_model, knn_metrics, knn_all_k = train_knn()

    print("\n==================================================")
    print("              MODEL COMPARISON SUMMARY            ")
    print("==================================================\n")

    # Build comparison DataFrame
    all_metrics = [lr_metrics, dt_metrics, knn_metrics]
    df_comparison = pd.DataFrame(all_metrics)

    # Format accuracy, precision, recall, f1
    print(df_comparison.to_string(index=False))

    # Save model_comparison.csv
    comp_csv_path = RESULTS_DIR / "model_comparison.csv"
    df_comparison.to_csv(comp_csv_path, index=False)
    print(f"\nSaved comparison table to: {comp_csv_path}")

    # Save model_accuracy.csv
    df_accuracy = df_comparison[["Model", "Accuracy"]].copy()
    acc_csv_path = RESULTS_DIR / "model_accuracy.csv"
    df_accuracy.to_csv(acc_csv_path, index=False)
    print(f"Saved accuracy table to: {acc_csv_path}")

    # Generate Chart
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")
    
    # Plot accuracy comparison
    ax = sns.barplot(
        data=df_comparison,
        x="Model",
        y="Accuracy",
        palette="viridis",
        hue="Model",
        legend=False
    )
    plt.title("Parkinson's Disease Prediction - Model Accuracy Comparison", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Machine Learning Algorithm", fontsize=12, labelpad=10)
    plt.ylabel("Accuracy Score", fontsize=12, labelpad=10)
    plt.ylim(0, 1.05)

    # Add data labels above bars
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(
            f"{height * 100:.2f}%",
            (p.get_x() + p.get_width() / 2.0, height),
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            xytext=(0, 5),
            textcoords="offset points"
        )

    plt.tight_layout()
    chart_path = CHARTS_DIR / "model_accuracy.png"
    plt.savefig(chart_path, dpi=300)
    plt.close()
    print(f"Saved accuracy comparison chart to: {chart_path}")

if __name__ == "__main__":
    main()
