import sqlite3
import polars as pl
import pandas as pd

from pathlib import Path

# Load cleaned 2026 data

folder = Path(r"C:\Users\yuvi_\Desktop\Fantasy_Boom\2026_season")
stats = pl.read_parquet(folder / "nfl_stats_2026_clean.parquet")

db_path = r"C:\Users\yuvi_\Desktop\Fantasy_Boom\fantasy_data.db"

conn = sqlite3.connect(db_path)

stats.to_pandas().to_sql(
    "player_stats_2026",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("2026 data added successfully!")
print(f"Rows: {stats.height}")
print(f"Columns: {stats.width}")