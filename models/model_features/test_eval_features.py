import sqlite3
import pandas as pd
import os

from pathlib import Path


folder = Path(__file__).parent.parent /"training_data"

DB_PATH = "fantasy_data.db"

past_week = int(os.getenv("CURRENT_WEEK", 9)) -1


with sqlite3.connect(DB_PATH) as conn:
    
    current_data = pd.read_sql_query("SELECT * FROM Model_training_data_2026", conn)
    

test = current_data[current_data["week"] == past_week].copy()

test.to_csv(folder / "test_eval_data.csv", index=False)
