import sqlite3
import polars as pl
import pandas as pd
import pyarrow




stats = pl.read_parquet("nfl_stats_clean.parquet")

db_path = r"C:\Users\yuvi_\Desktop\Fantasy_Boom\fantasy_data.db"


conn = sqlite3.connect(db_path)

stats.to_pandas().to_sql("player_stats", conn, if_exists="replace", index=False)

conn.close()

print(f"Database created at: {db_path}")
print(f"Table 'player_stats' created with {stats.shape[0]} rows and {stats.shape[1]} columns.")