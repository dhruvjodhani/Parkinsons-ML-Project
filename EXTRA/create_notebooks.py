"""Create the three course notebooks from existing student work, then train the model."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC_CSV = Path(r"C:\Users\dhruv\OneDrive\Desktop\ML\ML-Project\parkinsons_disease_data.csv")
DST_CSV = ROOT / "Dataset" / "parkinsons_disease_data.csv"
NB_DIR = ROOT / "notebooks"


def cell(cell_type, source, **kwargs):
    if isinstance(source, str):
        # Jupyter stores sources as line lists ending with \n except last
        lines = source.splitlines(keepends=True)
        if lines and not source.endswith("\n"):
            pass
        else:
            pass
        src = source.split("\n")
        formatted = []
        for i, line in enumerate(src):
            if i < len(src) - 1:
                formatted.append(line + "\n")
            elif line != "" or source.endswith("\n"):
                formatted.append(line if source.endswith("\n") and i == len(src) - 1 and line == "" else (line if i == len(src) - 1 else line + "\n"))
        # simpler:
        formatted = [line + "\n" for line in source.split("\n")]
        if formatted and formatted[-1] == "\n" and not source.endswith("\n"):
            formatted[-1] = ""
        if formatted and not source.endswith("\n") and formatted[-1].endswith("\n"):
            formatted[-1] = formatted[-1][:-1]
    else:
        formatted = source

    item = {
        "cell_type": cell_type,
        "metadata": {},
        "source": formatted,
    }
    if cell_type == "code":
        item["execution_count"] = None
        item["outputs"] = []
        item["id"] = kwargs.get("id", "")
    return item


def md(text):
    return cell("markdown", text)


def code(text):
    return cell("code", text)


def notebook(cells):
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


def write_nb(path, cells):
    path.write_text(json.dumps(notebook(cells), indent=1), encoding="utf-8")
    print("Wrote", path)


def build_eda():
    return [
        md("# 01 — Exploratory Data Analysis\n\nParkinson's disease dataset EDA. This notebook expands the original `Parkisons.ipynb` work (load, overview, quality checks, target plot)."),
        md("## 1. Import Libraries"),
        code("import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\nsns.set(style=\"whitegrid\")\nplt.rcParams[\"figure.figsize\"] = (8, 5)\n%matplotlib inline"),
        md("## 2. Load Dataset\n\nPath is relative to this notebook in `notebooks/`."),
        code('df = pd.read_csv("../Dataset/parkinsons_disease_data.csv")\nprint("Dataset loaded successfully")\nprint("Shape:", df.shape)'),
        md("## 3. Dataset Overview"),
        code("df.head()"),
        code("df.tail()"),
        code("print(\"Shape:\", df.shape)\nprint(\"\\nColumns:\")\nprint(df.columns.tolist())"),
        code("print(df.dtypes)"),
        code("df.info()"),
        code("df.describe().T"),
        md("## 4. Data Quality\n\nMissing values, duplicate rows, unique values, and empty extra columns."),
        code("print(\"Missing values per column:\")\nprint(df.isnull().sum())\nprint(\"\\nTotal missing values:\", df.isnull().sum().sum())"),
        code("print(\"Duplicate rows:\", df.duplicated().sum())"),
        code("for col in df.columns:\n    print(col)\n    print(df[col].unique()[:20], \"...\" if df[col].nunique() > 20 else \"\")\n    print(\"-\" * 40)"),
        code("print(\"Unnamed: 34 non-null:\", df[\"Unnamed: 34\"].notna().sum() if \"Unnamed: 34\" in df.columns else \"column missing\")\nprint(\"Unnamed: 35 non-null:\", df[\"Unnamed: 35\"].notna().sum() if \"Unnamed: 35\" in df.columns else \"column missing\")"),
        md("## 5. Data Cleaning\n\n`Unnamed: 34` and `Unnamed: 35` are completely empty (CSV trailing commas). They are not features.\n\n`PatientID` is an identifier, not a clinical feature. It is kept here for EDA identity checks and dropped later in preprocessing.\n\n`pd.get_dummies` is **not** needed: every column is already numeric or binary."),
        code("unnamed_columns = [c for c in df.columns if str(c).startswith(\"Unnamed\")]\nprint(\"Unnecessary empty columns:\", unnamed_columns)\n\ndf = df.drop(columns=unnamed_columns)\ndf = df.drop_duplicates()\n\nprint(\"Shape after cleaning:\", df.shape)\nprint(\"Missing values after cleaning:\", df.isnull().sum().sum())\nprint(\"Duplicate rows after cleaning:\", df.duplicated().sum())"),
        md("## 6. Target Analysis\n\nTarget column: `Diagnosis` (0 = negative class, 1 = positive class)."),
        code("print(df[\"Diagnosis\"].value_counts())\nprint(\"\\nPercentage:\")\nprint((df[\"Diagnosis\"].value_counts(normalize=True) * 100).round(2))"),
        code("ax = sns.countplot(x=\"Diagnosis\", data=df, palette=\"Set2\")\nplt.title(\"Diagnosis counts\")\nplt.xlabel(\"Diagnosis (0 = Negative, 1 = Positive)\")\nplt.ylabel(\"Number of records\")\nfor c in ax.containers:\n    ax.bar_label(c)\nplt.show()"),
        md("## 7. Univariate Analysis"),
        code("num_cols = [\n    \"Age\", \"BMI\", \"UPDRS\", \"MoCA\", \"FunctionalAssessment\",\n    \"PhysicalActivity\", \"SleepQuality\", \"CholesterolTotal\",\n    \"CholesterolLDL\", \"CholesterolHDL\", \"CholesterolTriglycerides\",\n]\n\nfig, axes = plt.subplots(4, 3, figsize=(16, 14))\naxes = axes.flatten()\nfor i, col in enumerate(num_cols):\n    sns.histplot(df[col], kde=True, ax=axes[i], color=\"steelblue\")\n    axes[i].set_title(col)\naxes[-1].axis(\"off\")\nplt.tight_layout()\nplt.show()"),
        code("fig, axes = plt.subplots(4, 3, figsize=(16, 14))\naxes = axes.flatten()\nfor i, col in enumerate(num_cols):\n    sns.boxplot(y=df[col], ax=axes[i], color=\"lightblue\")\n    axes[i].set_title(col)\naxes[-1].axis(\"off\")\nplt.tight_layout()\nplt.show()"),
        md("## 8. Categorical / Binary Analysis"),
        code("cat_cols = [\n    \"Gender\", \"Smoking\", \"Hypertension\", \"Diabetes\", \"Depression\",\n    \"Stroke\", \"Tremor\", \"Rigidity\", \"Bradykinesia\", \"Posture\",\n    \"SpeechProblems\", \"SleepDisorders\", \"Constipation\",\n]\n\nfig, axes = plt.subplots(5, 3, figsize=(16, 18))\naxes = axes.flatten()\nfor i, col in enumerate(cat_cols):\n    sns.countplot(x=col, hue=\"Diagnosis\", data=df, ax=axes[i], palette=\"Set2\")\n    axes[i].set_title(f\"{col} vs Diagnosis\")\nfor j in range(len(cat_cols), len(axes)):\n    axes[j].axis(\"off\")\nplt.tight_layout()\nplt.show()"),
        code("# AlcoholConsumption is continuous in this dataset (units/week), not a 0/1 flag.\nplt.figure(figsize=(8, 5))\nsns.kdeplot(data=df, x=\"AlcoholConsumption\", hue=\"Diagnosis\", common_norm=False)\nplt.title(\"AlcoholConsumption by Diagnosis\")\nplt.show()"),
        md("## 9. Bivariate Analysis"),
        code("bivariate_num = [\"Age\", \"BMI\", \"UPDRS\", \"MoCA\"]\nfig, axes = plt.subplots(2, 2, figsize=(12, 10))\naxes = axes.flatten()\nfor i, col in enumerate(bivariate_num):\n    sns.boxplot(x=\"Diagnosis\", y=col, data=df, ax=axes[i], palette=\"Set2\")\n    axes[i].set_title(f\"{col} vs Diagnosis\")\nplt.tight_layout()\nplt.show()"),
        code("bivariate_bin = [\"Tremor\", \"Rigidity\", \"Bradykinesia\", \"SleepDisorders\"]\nfig, axes = plt.subplots(2, 2, figsize=(12, 10))\naxes = axes.flatten()\nfor i, col in enumerate(bivariate_bin):\n    sns.countplot(x=col, hue=\"Diagnosis\", data=df, ax=axes[i], palette=\"Set2\")\n    axes[i].set_title(f\"{col} vs Diagnosis\")\nplt.tight_layout()\nplt.show()"),
        md("## 10. Correlation Analysis"),
        code("corr = df.drop(columns=[\"PatientID\"]).corr()\nplt.figure(figsize=(18, 14))\nsns.heatmap(corr, cmap=\"coolwarm\", center=0, annot=False, linewidths=0.3)\nplt.title(\"Correlation heatmap (numerical features, PatientID excluded)\")\nplt.tight_layout()\nplt.show()"),
        code("target_corr = corr[\"Diagnosis\"].drop(\"Diagnosis\").sort_values(key=abs, ascending=False)\nprint(\"Correlation with Diagnosis (absolute value, strongest first):\")\nprint(target_corr.head(15))"),
        md("""## 11. EDA Conclusions

```text
EDA CONCLUSION

- Dataset contains 2105 records and 36 raw columns (34 after dropping two empty Unnamed columns).
- Target variable is Diagnosis (1 = positive class, 0 = negative class).
- Class counts in this file: 1304 positive (about 62%) and 801 negative (about 38%).
- Missing values: none in real feature columns. Unnamed: 34 and Unnamed: 35 were 100% empty.
- Duplicate rows: 0.
- PatientID is a record identifier and should not be used as an ML feature.
- Important observations (relationships in THIS dataset, not medical causes):
  - Motor-related flags (Tremor, Rigidity, Bradykinesia, Posture) and clinical scores
    (UPDRS, MoCA, FunctionalAssessment) show visible differences across Diagnosis groups
    in the plots above.
  - Lifestyle and lab variables are mixed; some may be weakly associated.
- Features that appear useful for prediction in this dataset:
  UPDRS, MoCA, FunctionalAssessment, Tremor, Rigidity, Bradykinesia, Posture,
  and other symptom flags. Confirm with model coefficients and comparison metrics.
```

Do not treat any association in this notebook as proof that a feature causes Parkinson's disease.
"""),
    ]


def build_preprocess():
    return [
        md("# 02 — Preprocessing and Logistic Regression\n\nThis notebook continues the original `Untitled.ipynb` pipeline: clean data, drop `PatientID`, stratified split, scale **only on training data**, train Logistic Regression, evaluate, and save artifacts for the Flask API."),
        md("## 1. Load cleaned dataset"),
        code("import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport joblib\nfrom pathlib import Path\n\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.metrics import (\n    accuracy_score,\n    precision_score,\n    recall_score,\n    f1_score,\n    confusion_matrix,\n    classification_report,\n    roc_auc_score,\n    roc_curve,\n    ConfusionMatrixDisplay,\n)\n\nsns.set(style=\"whitegrid\")\n%matplotlib inline\n\nDATA_PATH = Path(\"../Dataset/parkinsons_disease_data.csv\")\nMODEL_DIR = Path(\"../model\")\nMODEL_DIR.mkdir(parents=True, exist_ok=True)\n\ndf = pd.read_csv(DATA_PATH)\nprint(\"Dataset loaded successfully!\")\nprint(\"Shape:\", df.shape)\ndf.head()"),
        md("## 2. Remove unnecessary columns\n\nDrop empty `Unnamed` columns and `PatientID` (identifier, not a predictor)."),
        code("unnamed_columns = [c for c in df.columns if str(c).startswith(\"Unnamed\")]\ndf = df.drop(columns=unnamed_columns)\nprint(\"Removed columns:\", unnamed_columns)\nprint(\"Missing values:\", df.isnull().sum().sum())\nprint(\"Duplicate rows:\", df.duplicated().sum())\ndf = df.drop_duplicates()\nprint(\"Shape:\", df.shape)"),
        md("## 3. Separate features and target"),
        code("y = df[\"Diagnosis\"]\nX = df.drop(columns=[\"Diagnosis\", \"PatientID\"], errors=\"ignore\")\n\nprint(\"X shape:\", X.shape)\nprint(\"y shape:\", y.shape)\nprint(\"\\nFeature columns (this order is saved for the API):\")\nprint(X.columns.tolist())\nprint(\"\\nTarget distribution:\")\nprint(y.value_counts())"),
        code("plt.figure(figsize=(7, 5))\nax = sns.countplot(x=y)\nplt.title(\"Diagnosis Distribution\")\nplt.xlabel(\"Diagnosis\")\nplt.ylabel(\"Number of Patients\")\nfor container in ax.containers:\n    ax.bar_label(container)\nplt.show()"),
        md("## 4. Train/Test Split\n\nStratify on `Diagnosis` so both classes stay in similar proportions.\n\nScaler is fitted **after** this split, on training data only (no leakage)."),
        code("X_train, X_test, y_train, y_test = train_test_split(\n    X,\n    y,\n    test_size=0.2,\n    random_state=42,\n    stratify=y,\n)\n\nprint(\"Training features:\", X_train.shape)\nprint(\"Testing features :\", X_test.shape)\nprint(\"Training target  :\", y_train.shape)\nprint(\"Testing target   :\", y_test.shape)"),
        md("## 5. Preprocessing\n\nFeatures are already numeric/binary, so `StandardScaler` is enough.\n\nFit only on `X_train`, then transform train and test."),
        code("scaler = StandardScaler()\nX_train_scaled = scaler.fit_transform(X_train)\nX_test_scaled = scaler.transform(X_test)\nprint(\"Feature scaling completed!\")\nprint(\"Scaler was fitted on training data only.\")"),
        md("## 6. Logistic Regression"),
        code("model = LogisticRegression(\n    max_iter=1000,\n    random_state=42,\n)\nmodel.fit(X_train_scaled, y_train)\nmodel"),
        md("## 7. Evaluation"),
        code("y_pred = model.predict(X_test_scaled)\ny_proba = model.predict_proba(X_test_scaled)[:, 1]\n\nprint(\"First 20 predictions:\")\nprint(y_pred[:20])\nprint()\nprint(\"Accuracy :\", round(accuracy_score(y_test, y_pred), 4))\nprint(\"Precision:\", round(precision_score(y_test, y_pred), 4))\nprint(\"Recall   :\", round(recall_score(y_test, y_pred), 4))\nprint(\"F1-score :\", round(f1_score(y_test, y_pred), 4))\nprint(\"ROC-AUC  :\", round(roc_auc_score(y_test, y_proba), 4))\nprint()\nprint(\"Classification report:\")\nprint(classification_report(y_test, y_pred, target_names=[\"Negative (0)\", \"Positive (1)\"]))"),
        code("cm = confusion_matrix(y_test, y_pred)\nprint(\"Confusion matrix:\\n\", cm)\nConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[\"Negative\", \"Positive\"]).plot(cmap=\"Blues\")\nplt.title(\"Logistic Regression — Confusion Matrix\")\nplt.show()"),
        code("fpr, tpr, _ = roc_curve(y_test, y_proba)\nplt.figure(figsize=(7, 5))\nplt.plot(fpr, tpr, label=f\"ROC-AUC = {roc_auc_score(y_test, y_proba):.3f}\")\nplt.plot([0, 1], [0, 1], \"k--\", label=\"Random chance\")\nplt.xlabel(\"False Positive Rate\")\nplt.ylabel(\"True Positive Rate\")\nplt.title(\"Logistic Regression — ROC Curve\")\nplt.legend()\nplt.show()"),
        md("**How to read the metrics (viva):**\n\n- **Accuracy** — overall share of correct predictions. Can look high if one class dominates.\n- **Precision** — of predicted positives, how many were actually positive.\n- **Recall** — of actual positives, how many the model found.\n- **F1-score** — balance of precision and recall.\n- **ROC-AUC** — ranking quality across thresholds; 0.5 is chance, 1.0 is perfect separation.\n- **Confusion matrix** — true negatives, false positives, false negatives, true positives."),
        md("## 8. Save Model and Scaler"),
        code("joblib.dump(model, MODEL_DIR / \"parkinsons_model.pkl\")\njoblib.dump(scaler, MODEL_DIR / \"scaler.pkl\")\nprint(\"Saved:\", (MODEL_DIR / \"parkinsons_model.pkl\").resolve())\nprint(\"Saved:\", (MODEL_DIR / \"scaler.pkl\").resolve())"),
        md("## 9. Save Feature Order\n\nThe API must send values in this exact column order. `feature_columns.pkl` stores that list so Flask does not guess the order of JSON keys."),
        code("feature_columns = X.columns.tolist()\njoblib.dump(feature_columns, MODEL_DIR / \"feature_columns.pkl\")\nprint(\"Saved feature order:\")\nprint(feature_columns)"),
        md("Logistic Regression is the **deployed** model because it is easy to explain in a viva, trains quickly, and produces calibrated class probabilities for the UI. Notebook `03_Model_Comparison.ipynb` compares it with other algorithms on the **same** split."),
    ]


def build_compare():
    return [
        md("# 03 — Model Comparison\n\nCompare six classifiers on the **same** stratified train/test split and the **same** StandardScaler (fit on train only).\n\nDeployment still uses Logistic Regression unless this notebook shows a clearly better, equally practical choice."),
        code("import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport joblib\nfrom pathlib import Path\n\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.neighbors import KNeighborsClassifier\nfrom sklearn.svm import SVC\nfrom sklearn.naive_bayes import GaussianNB\nfrom sklearn.metrics import (\n    accuracy_score,\n    precision_score,\n    recall_score,\n    f1_score,\n    roc_auc_score,\n    roc_curve,\n)\n\nsns.set(style=\"whitegrid\")\n%matplotlib inline"),
        md("## Load data and reuse the same split settings"),
        code("df = pd.read_csv(\"../Dataset/parkinsons_disease_data.csv\")\nunnamed = [c for c in df.columns if str(c).startswith(\"Unnamed\")]\ndf = df.drop(columns=unnamed).drop_duplicates()\n\ny = df[\"Diagnosis\"]\nX = df.drop(columns=[\"Diagnosis\", \"PatientID\"], errors=\"ignore\")\n\nX_train, X_test, y_train, y_test = train_test_split(\n    X, y, test_size=0.2, random_state=42, stratify=y\n)\n\nscaler = StandardScaler()\nX_train_scaled = scaler.fit_transform(X_train)\nX_test_scaled = scaler.transform(X_test)\nprint(X_train_scaled.shape, X_test_scaled.shape)"),
        md("## Metrics explained\n\n- Accuracy can hide poor performance on the smaller class.\n- Precision vs recall: in a screening-style task, missing positives (low recall) and false alarms (low precision) both matter.\n- F1 balances those two.\n- ROC-AUC summarizes ranking quality and is less tied to a single 0.5 threshold.\n\nWe do **not** pick a model using accuracy alone."),
        code("models = {\n    \"Logistic Regression\": LogisticRegression(max_iter=1000, random_state=42),\n    \"Decision Tree\": DecisionTreeClassifier(random_state=42),\n    \"Random Forest\": RandomForestClassifier(n_estimators=200, random_state=42),\n    \"K-Nearest Neighbors\": KNeighborsClassifier(),\n    \"Support Vector Machine\": SVC(probability=True, random_state=42),\n    \"Naive Bayes\": GaussianNB(),\n}\n\nrows = []\nroc_data = {}\n\nfor name, clf in models.items():\n    clf.fit(X_train_scaled, y_train)\n    y_pred = clf.predict(X_test_scaled)\n    y_score = clf.predict_proba(X_test_scaled)[:, 1]\n    rows.append({\n        \"Model\": name,\n        \"Accuracy\": accuracy_score(y_test, y_pred),\n        \"Precision\": precision_score(y_test, y_pred),\n        \"Recall\": recall_score(y_test, y_pred),\n        \"F1\": f1_score(y_test, y_pred),\n        \"ROC-AUC\": roc_auc_score(y_test, y_score),\n    })\n    fpr, tpr, _ = roc_curve(y_test, y_score)\n    roc_data[name] = (fpr, tpr, roc_auc_score(y_test, y_score))\n\nresults = pd.DataFrame(rows)\nresults_rounded = results.copy()\nfor col in [\"Accuracy\", \"Precision\", \"Recall\", \"F1\", \"ROC-AUC\"]:\n    results_rounded[col] = results_rounded[col].round(4)\n\nresults_rounded"),
        md("## Comparison visualizations"),
        code("plot_df = results.melt(id_vars=\"Model\", var_name=\"Metric\", value_name=\"Score\")\nplt.figure(figsize=(12, 6))\nsns.barplot(data=plot_df, x=\"Metric\", y=\"Score\", hue=\"Model\")\nplt.ylim(0, 1.05)\nplt.title(\"Test-set metrics by model (same split)\")\nplt.legend(bbox_to_anchor=(1.02, 1), loc=\"upper left\")\nplt.tight_layout()\nplt.show()"),
        code("plt.figure(figsize=(8, 6))\nfor name, (fpr, tpr, auc) in roc_data.items():\n    plt.plot(fpr, tpr, label=f\"{name} (AUC={auc:.3f})\")\nplt.plot([0, 1], [0, 1], \"k--\")\nplt.xlabel(\"False Positive Rate\")\nplt.ylabel(\"True Positive Rate\")\nplt.title(\"ROC curves on the same test set\")\nplt.legend(fontsize=8)\nplt.show()"),
        code("print(\"Best Accuracy:\", results.loc[results[\"Accuracy\"].idxmax(), \"Model\"])\nprint(\"Best F1       :\", results.loc[results[\"F1\"].idxmax(), \"Model\"])\nprint(\"Best ROC-AUC  :\", results.loc[results[\"ROC-AUC\"].idxmax(), \"Model\"])\nprint()\nprint(results_rounded.to_string(index=False))"),
        md("""## MODEL COMPARISON CONCLUSION

Run the cells above and read the printed table. Then interpret with these rules:

```text
MODEL COMPARISON CONCLUSION

Logistic Regression was used as the deployed model because:
- It is a linear, well-known classifier that is easy to explain in a college viva
  (coefficients, probability via sigmoid, StandardScaler).
- It outputs class probabilities that the React UI can show as a percentage.
- It is compared fairly with tree, KNN, SVM, and Naive Bayes models on the
  same stratified 80/20 split.

If another model has clearly higher F1 and ROC-AUC, mention that fact in the viva,
but keep Logistic Regression deployed unless you also re-save that model as
model/parkinsons_model.pkl so the backend stays in sync.
```

Do not copy invented numbers into this markdown. Use the DataFrame printed by this notebook.
"""),
        md("Optional: the backend currently loads Logistic Regression from `../model/parkinsons_model.pkl` produced by `02_Preprocessing.ipynb` / `train_and_save_model.py`."),
    ]


def main():
    (ROOT / "Dataset").mkdir(parents=True, exist_ok=True)
    (ROOT / "model").mkdir(parents=True, exist_ok=True)
    NB_DIR.mkdir(parents=True, exist_ok=True)

    if SRC_CSV.exists():
        shutil.copy2(SRC_CSV, DST_CSV)
        print("Copied dataset to", DST_CSV)
    else:
        print("WARNING: source CSV not found at", SRC_CSV)

    write_nb(NB_DIR / "01_EDA.ipynb", build_eda())
    write_nb(NB_DIR / "02_Preprocessing.ipynb", build_preprocess())
    write_nb(NB_DIR / "03_Model_Comparison.ipynb", build_compare())


if __name__ == "__main__":
    main()
