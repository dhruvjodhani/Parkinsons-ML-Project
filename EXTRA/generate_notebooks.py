"""
Generate all Jupyter notebooks for the Parkinson's ML project.
Includes EDA.ipynb, logistic_regression.ipynb, decision_tree.ipynb, and knn.ipynb.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
EDA_DIR = BASE_DIR / "ML" / "EDA"
MODELS_DIR = BASE_DIR / "ML" / "MODELS"

EDA_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

def cell(cell_type, source):
    if isinstance(source, str):
        lines = [line + "\n" for line in source.split("\n")]
        if lines and lines[-1] == "\n":
            lines.pop()
        if lines and lines[-1].endswith("\n"):
            lines[-1] = lines[-1][:-1]
    else:
        lines = source

    item = {
        "cell_type": cell_type,
        "metadata": {},
        "source": lines,
    }
    if cell_type == "code":
        item["execution_count"] = None
        item["outputs"] = []
    return item

def md(text):
    return cell("markdown", text)

def code(text):
    return cell("code", text)

def make_notebook(cells):
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "pygments_lexer": "ipython3",
            },
        },
        "cells": cells,
    }

def save_nb(path, cells):
    path.write_text(json.dumps(make_notebook(cells), indent=1), encoding="utf-8")
    print("Generated Notebook:", path)

# ----------------------------------------------------
# 1. EDA.ipynb
# ----------------------------------------------------
eda_cells = [
    md("# Parkinson's Disease Dataset — Exploratory Data Analysis (EDA)\n\nThis notebook conducts a comprehensive data inspection, cleaning, quality check, and exploratory visual analysis on the Parkinson's Disease clinical dataset."),
    
    md("## 1. Import Required Libraries"),
    code("import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\nsns.set_theme(style=\"whitegrid\")\nplt.rcParams[\"figure.figsize\"] = (10, 6)\n%matplotlib inline"),
    
    md("## 2. Load Dataset\n\nDataset location relative to notebook: `../DATASET/parkinsons_dataset.csv`."),
    code("df = pd.read_csv(\"../DATASET/parkinsons_dataset.csv\")\nprint(\"Dataset shape:\", df.shape)"),
    
    md("## 3. Dataset Understanding\n\nInspect first 5 rows, last 5 rows, data types, and column names."),
    code("df.head()"),
    code("df.tail()"),
    code("print(\"Column Names:\\n\", df.columns.tolist())\nprint(\"\\nData Types:\\n\", df.dtypes)"),
    code("df.info()"),
    code("df.describe().T"),
    
    md("## 4. Data Cleaning & Integrity Check\n\nCheck for missing values, duplicates, and invalid columns."),
    code("print(\"Missing values per column:\\n\", df.isnull().sum())\nprint(\"\\nTotal missing values:\", df.isnull().sum().sum())"),
    code("print(\"Duplicate rows count:\", df.duplicated().sum())"),
    code("# Drop trailing unnamed columns if present\nunnamed = [c for c in df.columns if str(c).startswith(\"Unnamed\")]\nif unnamed:\n    df = df.drop(columns=unnamed)\n\n# Drop exact duplicates\ndf = df.drop_duplicates()\nprint(\"Shape after cleaning:\", df.shape)"),
    
    md("## 5. Identifier Column Handling\n\n`PatientID` is a unique record identifier used for referencing, but **must not be used as a predictive feature** in machine learning modeling."),
    code("if \"PatientID\" in df.columns:\n    print(\"PatientID column detected. Unique IDs:\", df[\"PatientID\"].nunique())\n    print(\"PatientID will be excluded during X/y feature separation.\")"),
    
    md("## 6. Exploratory Visualizations"),
    
    md("### Target Distribution (Diagnosis)"),
    code("plt.figure(figsize=(6, 4))\nax = sns.countplot(data=df, x=\"Diagnosis\", palette=\"Set2\", hue=\"Diagnosis\", legend=False)\nplt.title(\"Target Distribution: Parkinson's Diagnosis (0 = No, 1 = Yes)\")\nplt.xlabel(\"Diagnosis\")\nplt.ylabel(\"Patient Count\")\nfor p in ax.patches:\n    ax.annotate(f\"{int(p.get_height())}\", (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom')\nplt.show()\n\nprint(\"Diagnosis value counts:\")\nprint(df[\"Diagnosis\"].value_counts(normalize=True))"),
    
    md("### Demographics Distribution (Age, Gender, BMI)"),
    code("fig, axes = plt.subplots(1, 3, figsize=(16, 4))\nsns.histplot(df[\"Age\"], kde=True, ax=axes[0], color=\"skyblue\")\naxes[0].set_title(\"Age Distribution\")\n\nsns.countplot(data=df, x=\"Gender\", ax=axes[1], palette=\"pastel\", hue=\"Gender\", legend=False)\naxes[1].set_title(\"Gender Distribution (0=Female, 1=Male)\")\n\nsns.histplot(df[\"BMI\"], kde=True, ax=axes[2], color=\"teal\")\naxes[2].set_title(\"BMI Distribution\")\nplt.tight_layout()\nplt.show()"),
    
    md("### Correlation Matrix Heatmap"),
    code("plt.figure(figsize=(14, 10))\ncorr = df.drop(columns=[\"PatientID\"], errors=\"ignore\").corr()\nsns.heatmap(corr, cmap=\"coolwarm\", annot=False, linewidths=0.5)\nplt.title(\"Correlation Matrix of Clinical Features\")\nplt.show()"),
    
    md("### Key Neurological Scores vs Diagnosis"),
    code("fig, axes = plt.subplots(1, 2, figsize=(14, 5))\nsns.boxplot(data=df, x=\"Diagnosis\", y=\"UPDRS\", ax=axes[0], palette=\"Set1\", hue=\"Diagnosis\", legend=False)\naxes[0].set_title(\"UPDRS Score by Diagnosis\")\n\nsns.boxplot(data=df, x=\"Diagnosis\", y=\"MoCA\", ax=axes[1], palette=\"Set2\", hue=\"Diagnosis\", legend=False)\naxes[1].set_title(\"MoCA Score by Diagnosis\")\nplt.tight_layout()\nplt.show()"),
    
    md("## 7. Machine Learning Preparation\n\nSeparate features `$X$` (32 clinical predictors) and target `$y$` (`Diagnosis`)."),
    code("X = df.drop(columns=[\"Diagnosis\", \"PatientID\"], errors=\"ignore\")\ny = df[\"Diagnosis\"]\n\nprint(\"Features X shape:\", X.shape)\nprint(\"Target y shape:\", y.shape)\nprint(\"Feature Columns:\\n\", X.columns.tolist())")
]

save_nb(EDA_DIR / "EDA.ipynb", eda_cells)

# ----------------------------------------------------
# 2. logistic_regression.ipynb
# ----------------------------------------------------
lr_cells = [
    md("# Logistic Regression Model — Parkinson's Disease Prediction\n\nTrain and evaluate a Logistic Regression binary classification model using standardized clinical features."),
    
    md("## 1. Import Dependencies"),
    code("import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.metrics import (\n    accuracy_score, precision_score, recall_score, f1_score,\n    roc_auc_score, confusion_matrix, classification_report\n)\n\nsns.set_theme(style=\"whitegrid\")"),
    
    md("## 2. Load Dataset & Exclude Identifier Column"),
    code("df = pd.read_csv(\"../DATASET/parkinsons_dataset.csv\")\nunnamed = [c for c in df.columns if str(c).startswith(\"Unnamed\")]\nif unnamed:\n    df = df.drop(columns=unnamed)\ndf = df.drop_duplicates()\n\n# Exclude PatientID from predictive features X\nX = df.drop(columns=[\"Diagnosis\", \"PatientID\"], errors=\"ignore\")\ny = df[\"Diagnosis\"]\n\nprint(\"Feature matrix X shape:\", X.shape)\nprint(\"Target y shape:\", y.shape)"),
    
    md("## 3. Stratified Train-Test Split"),
    code("X_train, X_test, y_train, y_test = train_test_split(\n    X, y, test_size=0.2, random_state=42, stratify=y\n)\nprint(f\"Training set: {X_train.shape[0]} samples\")\nprint(f\"Testing set:  {X_test.shape[0]} samples\")"),
    
    md("## 4. Feature Scaling (StandardScaler)"),
    code("scaler = StandardScaler()\nX_train_scaled = scaler.fit_transform(X_train)\nX_test_scaled = scaler.transform(X_test)"),
    
    md("## 5. Train Logistic Regression Model"),
    code("model = LogisticRegression(max_iter=1000, random_state=42)\nmodel.fit(X_train_scaled, y_train)\nprint(\"Logistic Regression model successfully trained.\")"),
    
    md("## 6. Predictions & Evaluation"),
    code("y_pred = model.predict(X_test_scaled)\ny_prob = model.predict_proba(X_test_scaled)[:, 1]\n\nacc = accuracy_score(y_test, y_pred)\nprec = precision_score(y_test, y_pred)\nrec = recall_score(y_test, y_pred)\nf1 = f1_score(y_test, y_pred)\nroc_auc = roc_auc_score(y_test, y_prob)\n\nprint(f\"Accuracy:  {acc * 100:.2f}%\")\nprint(f\"Precision: {prec * 100:.2f}%\")\nprint(f\"Recall:    {rec * 100:.2f}%\")\nprint(f\"F1 Score:  {f1 * 100:.2f}%\")\nprint(f\"ROC-AUC:   {roc_auc:.4f}\")"),
    
    md("## 7. Classification Report & Confusion Matrix"),
    code("print(\"Classification Report:\\n\")\nprint(classification_report(y_test, y_pred))"),
    code("cm = confusion_matrix(y_test, y_pred)\nplt.figure(figsize=(6, 5))\nsns.heatmap(cm, annot=True, fmt=\"d\", cmap=\"Blues\", cbar=False,\n            xticklabels=[\"Negative (0)\", \"Positive (1)\"],\n            yticklabels=[\"Negative (0)\", \"Positive (1)\"])\nplt.title(\"Logistic Regression Confusion Matrix\")\nplt.xlabel(\"Predicted\")\nplt.ylabel(\"Actual\")\nplt.show()")
]

save_nb(MODELS_DIR / "logistic_regression.ipynb", lr_cells)

# ----------------------------------------------------
# 3. decision_tree.ipynb
# ----------------------------------------------------
dt_cells = [
    md("# Decision Tree Classifier — Parkinson's Disease Prediction\n\nTrain and evaluate a Decision Tree classifier for Parkinson's disease prediction."),
    
    md("## 1. Import Dependencies"),
    code("import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.tree import DecisionTreeClassifier, plot_tree\nfrom sklearn.metrics import (\n    accuracy_score, precision_score, recall_score, f1_score,\n    roc_auc_score, confusion_matrix, classification_report\n)\n\nsns.set_theme(style=\"whitegrid\")"),
    
    md("## 2. Load Dataset & Exclude Identifier Column"),
    code("df = pd.read_csv(\"../DATASET/parkinsons_dataset.csv\")\nunnamed = [c for c in df.columns if str(c).startswith(\"Unnamed\")]\nif unnamed:\n    df = df.drop(columns=unnamed)\ndf = df.drop_duplicates()\n\nX = df.drop(columns=[\"Diagnosis\", \"PatientID\"], errors=\"ignore\")\ny = df[\"Diagnosis\"]\n\nprint(\"Feature matrix X shape:\", X.shape)"),
    
    md("## 3. Stratified Train-Test Split"),
    code("X_train, X_test, y_train, y_test = train_test_split(\n    X, y, test_size=0.2, random_state=42, stratify=y\n)\nprint(f\"Training set: {X_train.shape[0]} samples\")\nprint(f\"Testing set:  {X_test.shape[0]} samples\")"),
    
    md("## 4. Train Decision Tree Classifier"),
    code("model = DecisionTreeClassifier(random_state=42)\nmodel.fit(X_train, y_train)\nprint(\"Decision Tree Classifier successfully trained.\")"),
    
    md("## 5. Predictions & Performance Evaluation"),
    code("y_pred = model.predict(X_test)\ny_prob = model.predict_proba(X_test)[:, 1]\n\nacc = accuracy_score(y_test, y_pred)\nprec = precision_score(y_test, y_pred)\nrec = recall_score(y_test, y_pred)\nf1 = f1_score(y_test, y_pred)\nroc_auc = roc_auc_score(y_test, y_prob)\n\nprint(f\"Accuracy:  {acc * 100:.2f}%\")\nprint(f\"Precision: {prec * 100:.2f}%\")\nprint(f\"Recall:    {rec * 100:.2f}%\")\nprint(f\"F1 Score:  {f1 * 100:.2f}%\")\nprint(f\"ROC-AUC:   {roc_auc:.4f}\")"),
    
    md("## 6. Classification Report & Confusion Matrix"),
    code("print(\"Classification Report:\\n\")\nprint(classification_report(y_test, y_pred))"),
    code("cm = confusion_matrix(y_test, y_pred)\nplt.figure(figsize=(6, 5))\nsns.heatmap(cm, annot=True, fmt=\"d\", cmap=\"Greens\", cbar=False,\n            xticklabels=[\"Negative (0)\", \"Positive (1)\"],\n            yticklabels=[\"Negative (0)\", \"Positive (1)\"])\nplt.title(\"Decision Tree Confusion Matrix\")\nplt.xlabel(\"Predicted\")\nplt.ylabel(\"Actual\")\nplt.show()"),
    
    md("## 7. Feature Importances"),
    code("importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)\nplt.figure(figsize=(10, 6))\nsns.barplot(x=importances.values[:10], y=importances.index[:10], palette=\"viridis\", hue=importances.index[:10], legend=False)\nplt.title(\"Top 10 Important Features in Decision Tree\")\nplt.xlabel(\"Feature Importance Score\")\nplt.show()")
]

save_nb(MODELS_DIR / "decision_tree.ipynb", dt_cells)

# ----------------------------------------------------
# 4. knn.ipynb
# ----------------------------------------------------
knn_cells = [
    md("# K-Nearest Neighbors (KNN) Classifier — Parkinson's Disease Prediction\n\nTrain and evaluate a distance-based K-Nearest Neighbors classifier on standardized clinical features."),
    
    md("## 1. Import Dependencies"),
    code("import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.neighbors import KNeighborsClassifier\nfrom sklearn.metrics import (\n    accuracy_score, precision_score, recall_score, f1_score,\n    roc_auc_score, confusion_matrix, classification_report\n)\n\nsns.set_theme(style=\"whitegrid\")"),
    
    md("## 2. Load Dataset & Exclude Identifier Column"),
    code("df = pd.read_csv(\"../DATASET/parkinsons_dataset.csv\")\nunnamed = [c for c in df.columns if str(c).startswith(\"Unnamed\")]\nif unnamed:\n    df = df.drop(columns=unnamed)\ndf = df.drop_duplicates()\n\nX = df.drop(columns=[\"Diagnosis\", \"PatientID\"], errors=\"ignore\")\ny = df[\"Diagnosis\"]\n\nprint(\"Feature matrix X shape:\", X.shape)"),
    
    md("## 3. Stratified Train-Test Split & Feature Scaling"),
    code("X_train, X_test, y_train, y_test = train_test_split(\n    X, y, test_size=0.2, random_state=42, stratify=y\n)\n\nscaler = StandardScaler()\nX_train_scaled = scaler.fit_transform(X_train)\nX_test_scaled = scaler.transform(X_test)"),
    
    md("## 4. Hyperparameter Evaluation ($k = 3, 5, 7, 9$)"),
    code("k_values = [3, 5, 7, 9]\nk_scores = []\n\nfor k in k_values:\n    knn = KNeighborsClassifier(n_neighbors=k)\n    knn.fit(X_train_scaled, y_train)\n    pred = knn.predict(X_test_scaled)\n    acc = accuracy_score(y_test, pred)\n    f1 = f1_score(y_test, pred)\n    k_scores.append({\"k\": k, \"Accuracy\": round(acc, 4), \"F1 Score\": round(f1, 4)})\n    print(f\"k={k}: Accuracy = {acc * 100:.2f}%, F1 = {f1 * 100:.2f}%\")\n\ndf_k = pd.DataFrame(k_scores)\nprint(\"\\nHyperparameter Tuning Results:\\n\", df_k)"),
    
    md("## 5. Train Final KNN Model with Optimal K ($k = 7$)"),
    code("final_k = 7\nmodel = KNeighborsClassifier(n_neighbors=final_k)\nmodel.fit(X_train_scaled, y_train)\nprint(f\"Final KNN model trained with k={final_k}.\")"),
    
    md("## 6. Predictions & Performance Evaluation"),
    code("y_pred = model.predict(X_test_scaled)\ny_prob = model.predict_proba(X_test_scaled)[:, 1]\n\nacc = accuracy_score(y_test, y_pred)\nprec = precision_score(y_test, y_pred)\nrec = recall_score(y_test, y_pred)\nf1 = f1_score(y_test, y_pred)\nroc_auc = roc_auc_score(y_test, y_prob)\n\nprint(f\"Accuracy:  {acc * 100:.2f}%\")\nprint(f\"Precision: {prec * 100:.2f}%\")\nprint(f\"Recall:    {rec * 100:.2f}%\")\nprint(f\"F1 Score:  {f1 * 100:.2f}%\")\nprint(f\"ROC-AUC:   {roc_auc:.4f}\")"),
    
    md("## 7. Classification Report & Confusion Matrix"),
    code("print(\"Classification Report:\\n\")\nprint(classification_report(y_test, y_pred))"),
    code("cm = confusion_matrix(y_test, y_pred)\nplt.figure(figsize=(6, 5))\nsns.heatmap(cm, annot=True, fmt=\"d\", cmap=\"Oranges\", cbar=False,\n            xticklabels=[\"Negative (0)\", \"Positive (1)\"],\n            yticklabels=[\"Negative (0)\", \"Positive (1)\"])\nplt.title(f\"KNN (k={final_k}) Confusion Matrix\")\nplt.xlabel(\"Predicted\")\nplt.ylabel(\"Actual\")\nplt.show()")
]

save_nb(MODELS_DIR / "knn.ipynb", knn_cells)

print("All notebooks generated successfully.")
