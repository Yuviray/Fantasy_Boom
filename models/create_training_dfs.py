import pandas as pd
import joblib
import xgboost as xgb
from pathlib import Path
import numpy as np

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report,average_precision_score, roc_auc_score, brier_score_loss

folder = Path(__file__).parent.parent /"models/training_data"

output_path =  Path(__file__).parent.parent /"models/parquet_files"

train_data = pd.read_csv(folder / "train_data.csv")
validation_data = pd.read_csv(folder / "validation_data.csv")





numerical_features = ['week', 'previous_ppr', 'prev_targets', 'prev_carries', 'prev_receptions', 'prev_receiving_yards', 'prev_rushing_yards',
                      'prev_rushing_tds', 'prev_receiving_tds', 'prev_3_avg', 'prev_5_avg', 'prev_3_targets_avg', 'prev_5_targets_avg', 'prev_3_carries', 'prev_5_carries',
                      'receptions_avg_3', 'receptions_avg_5', 'receiving_yards_avg_3', 'receiving_yards_avg_5', 'rushing_yards_avg_3', 'rushing_yards_avg_5', 'rushing_tds_avg_3', 
                      'rushing_tds_avg_5', 'receiving_tds_avg_3', 'receiving_tds_avg_5', 'projected_points']

categorical_features = ['position', 'team', 'opponent_team']


numerical_features = [
    f for f in numerical_features
    if all(f in df.columns for df in [train_data, validation_data])
    
]

categorical_features = [
    f for f in categorical_features
    if all(f in df.columns for df in [train_data, validation_data])
]


features = numerical_features + categorical_features

train = train_data.dropna(subset= ["Boom"]).copy()
validation = validation_data.dropna(subset= ["Boom"]).copy()


for name, df in [("train", train), ("validation", validation)]:
    df["Boom"] = df["Boom"].astype(int)
    
    if not set(df["Boom"].unique()).issubset({0, 1}):
        raise ValueError(f"{name} data contains invalid values in 'Boom' column: {df['Boom'].unique()}")
    
    if df["Boom"].isnull().any():
        raise ValueError(f"{name} data contains NaN values in 'Boom' column")
    

x_train = train[features].copy()
y_train = train["Boom"].copy()

x_validation = validation[features].copy()
y_validation = validation["Boom"].copy()




for df in [x_train, x_validation]:
    for col in numerical_features:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    for col in categorical_features:
        df[col] = df[col].fillna("missing").astype(str)
        
        
        
x_train = pd.get_dummies(x_train, columns=categorical_features, dtype=int)
x_validation = pd.get_dummies(x_validation, columns=categorical_features, dtype=int).reindex(columns=x_train.columns, fill_value=0)



x_train.to_parquet(output_path/"x_train.parquet", index=False)

y_train.to_frame().to_parquet(output_path/"y_train.parquet", index=False)

x_validation.to_parquet(output_path/"x_validation.parquet", index=False)


y_validation.to_frame().to_parquet(output_path/"y_validation.parquet", index=False)






