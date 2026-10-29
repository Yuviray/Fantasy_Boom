import pandas as pd
import joblib
import xgboost as xgb
from pathlib import Path
import numpy as np

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report,average_precision_score, roc_auc_score, brier_score_loss

folder = Path(__file__).parent.parent /"models/training_data"


model_dir =  Path(__file__).parent.parent /"models/saved_models"
model_path = model_dir/ "xgboost_v1_model.json"


output_path =  Path(__file__).parent.parent /"models/parquet_files"


x_test = pd.read_parquet(
    output_path / "x_test.parquet"
)

player_info = pd.read_parquet(
    output_path / "test_player_info.parquet"
)



model = xgb.XGBClassifier()
model.load_model(model_path)


threshold = 0.33


pre_threshold = model.predict_proba(x_test)[:,1]

test_pred = (pre_threshold > threshold).astype(int)
assert len(player_info) == len(test_pred)

results_df = player_info.copy()


results_df["boom_probability"] = pre_threshold
results_df["boom_prediction"] = test_pred

results_df.to_csv(folder / "model_results.csv")