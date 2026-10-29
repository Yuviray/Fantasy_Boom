import pandas as pd
import joblib
import xgboost as xgb
from pathlib import Path
import numpy as np

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report,average_precision_score, roc_auc_score, brier_score_loss

folder = Path(__file__).parent.parent /"models/training_data"

output_path =  Path(__file__).parent.parent /"models/parquet_files"



test_data = pd.read_csv(folder / "test_data.csv")





numerical_features = ['week', 'previous_ppr', 'prev_targets', 'prev_carries', 'prev_receptions', 'prev_receiving_yards', 'prev_rushing_yards',
                      'prev_rushing_tds', 'prev_receiving_tds', 'prev_3_avg', 'prev_5_avg', 'prev_3_targets_avg', 'prev_5_targets_avg', 'prev_3_carries', 'prev_5_carries',
                      'receptions_avg_3', 'receptions_avg_5', 'receiving_yards_avg_3', 'receiving_yards_avg_5', 'rushing_yards_avg_3', 'rushing_yards_avg_5', 'rushing_tds_avg_3', 
                      'rushing_tds_avg_5', 'receiving_tds_avg_3', 'receiving_tds_avg_5', 'projected_points']

categorical_features = ['position', 'team', 'opponent_team']


numerical_features = [
    f for f in numerical_features
    if f in test_data.columns
    
]

categorical_features = [
    f for f in categorical_features
     if f in test_data.columns
]


features = numerical_features + categorical_features

#test = test_data.dropna(subset= ["Boom"]).copy() 
test = test_data.copy()


player_info = test[[
    'player_display_name',
    'position',
    'week',
    'opponent_team',
    'team',
    'projected_points',
    'headshot_url'
]].copy()

player_info.to_parquet(
    output_path / "test_player_info.parquet",
    index=False
)



x_test = test[features].copy()

for col in numerical_features:
    x_test[col] = pd.to_numeric(x_test[col], errors='coerce')
        
for col in categorical_features:
    x_test[col] = x_test[col].fillna("missing").astype(str)
        
        
x_train = pd.read_parquet(
    output_path / "x_train.parquet"
)

        
        
x_test = pd.get_dummies(x_test, columns=categorical_features, dtype=int).reindex(columns=x_train.columns, fill_value=0)    



x_test.to_parquet(output_path/"x_test.parquet", index=False)
