import pandas as pd
import joblib
import xgboost as xgb
from pathlib import Path
import numpy as np

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report,average_precision_score, roc_auc_score, brier_score_loss

folder = Path(__file__).parent.parent /"models/training_data"

train_data = pd.read_csv(folder / "train_data.csv")
validation_data = pd.read_csv(folder / "validation_data.csv")
test_data = pd.read_csv(folder / "test_data.csv")




numerical_features = ['week', 'previous_ppr', 'prev_targets', 'prev_carries', 'prev_receptions', 'prev_receiving_yards', 'prev_rushing_yards',
                      'prev_rushing_tds', 'prev_receiving_tds', 'prev_3_avg', 'prev_5_avg', 'prev_3_targets_avg', 'prev_5_targets_avg', 'prev_3_carries', 'prev_5_carries',
                      'receptions_avg_3', 'receptions_avg_5', 'receiving_yards_avg_3', 'receiving_yards_avg_5', 'rushing_yards_avg_3', 'rushing_yards_avg_5', 'rushing_tds_avg_3', 
                      'rushing_tds_avg_5', 'receiving_tds_avg_3', 'receiving_tds_avg_5', 'projected_points']

categorical_features = ['position', 'team', 'opponent_team']


numerical_features = [
    f for f in numerical_features
    if all(f in df.columns for df in [train_data, validation_data, test_data])
    
]

categorical_features = [
    f for f in categorical_features
    if all(f in df.columns for df in [train_data, validation_data, test_data])
]


features = numerical_features + categorical_features

train = train_data.dropna(subset= ["Boom"]).copy()
validation = validation_data.dropna(subset= ["Boom"]).copy()
test = test_data.dropna(subset= ["Boom"]).copy() #test = test_data.copy()


for name, df in [("train", train), ("validation", validation), ("test", test)]:
    df["Boom"] = df["Boom"].astype(int)
    
    if not set(df["Boom"].unique()).issubset({0, 1}):
        raise ValueError(f"{name} data contains invalid values in 'Boom' column: {df['Boom'].unique()}")
    
    if df["Boom"].isnull().any():
        raise ValueError(f"{name} data contains NaN values in 'Boom' column")
    

x_train = train[features].copy()
y_train = train["Boom"].copy()

x_validation = validation[features].copy()
y_validation = validation["Boom"].copy()

x_test = test[features].copy()
y_test = test["Boom"].copy()


for df in [x_train, x_validation, x_test]:
    for col in numerical_features:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    for col in categorical_features:
        df[col] = df[col].fillna("missing").astype(str)
        
        
        
x_train = pd.get_dummies(x_train, columns=categorical_features, dtype=int)
x_validation = pd.get_dummies(x_validation, columns=categorical_features, dtype=int).reindex(columns=x_train.columns, fill_value=0)
x_test = pd.get_dummies(x_test, columns=categorical_features, dtype=int).reindex(columns=x_train.columns, fill_value=0)


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



pre_threshold = model.predict_proba(x_test)[:,1]

test_pred = (pre_threshold > threshold).astype(int)
assert len(test_data) == len(test_pred)

print("test_metrics:")
print("Accuracy:", accuracy_score(y_test, test_pred))
print("Precision:", precision_score(y_test, test_pred))
print("Recall:", recall_score(y_test, test_pred))
print("F1 Score:", f1_score(y_test, test_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, test_pred))
print("Classification Report:\n", classification_report(y_test, test_pred))


results_df = test_data[[
    'player_display_name',
    'position',
    'week',
    'opponent_team',
    'team',
    'projected_points',
    'headshot_url'
]].copy()

results_df["boom_prediction"] = test_pred

results_df.to_csv(folder / "model_results.csv")


    
    
