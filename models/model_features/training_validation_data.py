import sqlite3
import pandas as pd

from pathlib import Path


folder = Path(__file__).parent.parent /"training_data"

DB_PATH = "fantasy_data.db"

current_week = 7


with sqlite3.connect(DB_PATH) as conn:
    
    historical_data = pd.read_sql_query("SELECT * FROM Historical_training_data", conn)
    current_data = pd.read_sql_query("SELECT * FROM Model_training_data_2026", conn)
    
    
    
historical_data = historical_data.dropna(subset = ["Boom"]).copy()
current_data = current_data.dropna(subset = ["Boom"]).copy()


train_data = pd.concat([
    historical_data[historical_data["week"] <= 14],
    current_data[current_data["week"] <= current_week-2],
], ignore_index=True)



validation_data = pd.concat([
    historical_data[historical_data["week"] > 14],
    current_data[(current_data["week"] ==  current_week-1)],
], ignore_index=True)   



train_data.to_csv(folder / "train_data.csv", index=False)
validation_data.to_csv(folder / "validation_data.csv", index=False)  
