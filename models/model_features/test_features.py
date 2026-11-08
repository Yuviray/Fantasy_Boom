import sqlite3
import pandas as pd
import os

from pathlib import Path


folder = Path(__file__).parent.parent /"training_data"

DB_PATH = "fantasy_data.db"

current_week = int(os.getenv("CURRENT_WEEK", 9))


with sqlite3.connect(DB_PATH) as conn:
    
    current_data = pd.read_sql_query("SELECT * FROM current_week", conn)
    

test = current_data[current_data["week"] == current_week].copy()

test.to_csv(folder / "test_data.csv", index=False)
        