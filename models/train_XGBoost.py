import pandas as pd
import joblib
import xgboost as xgb
from pathlib import Path
import numpy as np

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report,average_precision_score, roc_auc_score, brier_score_loss

folder = Path(__file__).parent.parent /"models/training_data"

output_path =  Path(__file__).parent.parent /"models/parquet_files"


x_train = pd.read_parquet(
    output_path / "x_train.parquet"
)

y_train = pd.read_parquet(
    output_path / "y_train.parquet"
).squeeze("columns")


x_validation = pd.read_parquet(
    output_path / "x_validation.parquet"
)

y_validation = pd.read_parquet(
    output_path / "y_validation.parquet"
).squeeze("columns")




negative_count = (y_train == 0).sum()
positive_count = (y_train == 1).sum()
positive_class_weight = negative_count / positive_count



model = xgb.XGBClassifier(
    objective='binary:logistic',
    scale_pos_weight=positive_class_weight *.5,
    eval_metric='aucpr',
    n_estimators=1000,
    learning_rate=0.03,
    max_depth=3,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    reg_lambda=2.0,
    early_stopping_rounds=50,
    tree_method='hist',
    min_child_weight=5,
    n_jobs=-1
)


model.fit(
    x_train, y_train,
    eval_set=[(x_validation, y_validation)],
    verbose=50
)

probs = model.predict_proba(x_validation)[:, 1]

print("Minimum:", probs.min())
print("Maximum:", probs.max())
print("Mean:", probs.mean())
print("Percentiles:", np.percentile(probs, [50, 75, 90, 95, 99]))

for threshold in [0.1, 0.2, 0.3, 0.4, 0.5]:
    preds = (probs >= threshold).astype(int)
    print(f"Threshold {threshold}: predicted Boom = {preds.sum()}")
    print("PR-AUC:", average_precision_score(y_validation, probs))

threshold = 0.33


pre_threshold = model.predict_proba(x_validation)[:,1]

validation_preds = (pre_threshold > threshold).astype(int)


print("Validation Metrics:")
print("Accuracy:", accuracy_score(y_validation, validation_preds))
print("Precision:", precision_score(y_validation, validation_preds))
print("Recall:", recall_score(y_validation, validation_preds))
print("F1 Score:", f1_score(y_validation, validation_preds))
print("Confusion Matrix:\n", confusion_matrix(y_validation, validation_preds))
print("Classification Report:\n", classification_report(y_validation, validation_preds))


model_dir =  Path(__file__).parent.parent /"models/saved_models"
model_path = model_dir/ "xgboost_v1_model.json"



model.save_model(model_path)





