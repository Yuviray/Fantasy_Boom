import sqlite3
import polars as pl
import pandas as pd

from pathlib import Path

folder = Path(__file__).parent.parent /"2026_season"

stats = pl.read_parquet(folder / "nfl_stats_2026_clean.parquet")

conn = sqlite3.connect("fantasy_data.db")

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