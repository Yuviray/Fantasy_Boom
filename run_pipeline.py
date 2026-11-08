import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime


PROJECT_DIR = Path(__file__).resolve().parent


PYTHON = PROJECT_DIR / ".venv" / "Scripts" / "python.exe"


CURRENT_WEEK = 9

def run_script(script_path):
    print(f"\nRunning script: {script_path.name} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("__" * 50)
        
    if not script_path.exists():
        raise FileNotFoundError(f"Script not found: {script_path}")
        
    env = os.environ.copy()
    env["CURRENT_WEEK"] = str(CURRENT_WEEK)

    subprocess.run(
        [str(PYTHON), str(script_path)],
        cwd=PROJECT_DIR,
        env=env,
        check=True
    )
    
    print(f"Finished script: {script_path.name} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

DATA_PIPELINE = [
    PROJECT_DIR / "2026_season" / "2026_data.py",
    PROJECT_DIR / "2026_season" / "add_to_sql.py",
    PROJECT_DIR / "2026_season" / "build_new_features.py",
    PROJECT_DIR / "projection data" / "get_gridiron_data.py",
    PROJECT_DIR / "projection data" / "adding_gridiron projection_data.py"
    
]

MODEL_PIPELINE = [
    PROJECT_DIR / "models" /  "latest_week.py",
    PROJECT_DIR / "models" / "model_features" / "training_validation_data.py",
    PROJECT_DIR / "models" / "model_features" / "test_features.py",
    PROJECT_DIR / "models" /  "create_training_dfs.py",
    PROJECT_DIR / "models" /  "create test_dfs.py",
    PROJECT_DIR / "models" /  "train_XGBoost.py",
    PROJECT_DIR / "models" /  "test_xgboost.py",
]

    
    
def main():
    
    print(f"Starting Fantasy Boom Data Pipeline")
    for script in DATA_PIPELINE:
        run_script(script)
        
    print(f"\nStarting Fantasy Boom Model Pipeline")
    for script in MODEL_PIPELINE:
        run_script(script)
        
    print(f"\nAll scripts completed successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        
if __name__ == "__main__":
    main()
    
    