import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ML_PROJECT_DIR = BASE_DIR.parent / "ML-Project"

print("Base directory:", BASE_DIR)

# 1. Rename ML-Frontend to FRONTEND
frontend_old = BASE_DIR / "ML-Frontend"
frontend_new = BASE_DIR / "FRONTEND"
if frontend_old.exists() and not frontend_new.exists():
    print("Renaming ML-Frontend -> FRONTEND")
    frontend_old.rename(frontend_new)

# 2. Rename ML-Backend to BACKEND
backend_old = BASE_DIR / "ML-Backend"
backend_new = BASE_DIR / "BACKEND"
if backend_old.exists() and not backend_new.exists():
    print("Renaming ML-Backend -> BACKEND")
    backend_old.rename(backend_new)

# 3. Create ML structure
ml_dir = BASE_DIR / "ML"
dataset_dir = ml_dir / "DATASET"
eda_dir = ml_dir / "EDA"
models_dir = ml_dir / "MODELS"
python_dir = ml_dir / "PYTHON"
results_dir = ml_dir / "RESULTS"
charts_dir = results_dir / "charts"
extra_dir = BASE_DIR / "EXTRA"

for d in [dataset_dir, eda_dir, models_dir, python_dir, results_dir, charts_dir, extra_dir]:
    d.mkdir(parents=True, exist_ok=True)
    print("Directory ready:", d.relative_to(BASE_DIR))

# 4. Copy dataset file
src_dataset = ML_PROJECT_DIR / "parkinsons_disease_data.csv"
dst_dataset = dataset_dir / "parkinsons_dataset.csv"
if src_dataset.exists():
    print(f"Copying dataset from {src_dataset.relative_to(BASE_DIR.parent)} to {dst_dataset.relative_to(BASE_DIR)}")
    shutil.copy2(src_dataset, dst_dataset)
    shutil.copy2(src_dataset, dataset_dir / "parkinsons_disease_data.csv")

# 5. Move existing notebooks to ML/EDA
old_notebooks = BASE_DIR / "notebooks"
if old_notebooks.exists():
    for nb in old_notebooks.glob("*.ipynb"):
        dst = eda_dir / nb.name
        print(f"Copying {nb.name} -> ML/EDA/")
        shutil.copy2(nb, dst)

# Copy original notebooks from ML-Project to EXTRA/original_notebooks
orig_nb_dir = extra_dir / "original_notebooks"
orig_nb_dir.mkdir(parents=True, exist_ok=True)
if ML_PROJECT_DIR.exists():
    for f in ML_PROJECT_DIR.glob("*"):
        if f.is_file() and f.name != "parkinsons_disease_data.csv":
            print(f"Copying {f.name} to EXTRA/original_notebooks/")
            shutil.copy2(f, orig_nb_dir / f.name)

# 6. Ensure BACKEND model directory exists
backend_model_dir = BASE_DIR / "BACKEND" / "model"
backend_model_dir.mkdir(parents=True, exist_ok=True)

# Copy old model files if existing
old_model_dir = BASE_DIR / "model"
if old_model_dir.exists():
    for mf in old_model_dir.glob("*"):
        shutil.copy2(mf, backend_model_dir / mf.name)

print("Restructuring completed successfully.")
