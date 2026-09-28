import sqlite3
import pandas as pd
import polars as pl

db_path = r"C:\Users\yuvi_\Desktop\Fantasy_Boom\fantasy_data.db"

conn = sqlite3.connect(db_path)

df = pd.read_sql("SELECT * FROM player_stats_2026", conn)

df = df.sort_values(["player_id", "week"])

df["previous_ppr"] = df.groupby("player_id")["fantasy_points_ppr"].shift(1)
df["prev_targets"] = df.groupby("player_id")["targets"].shift(1)
df["prev_carries"] = df.groupby("player_id")["carries"].shift(1)
df["prev_receptions"] = df.groupby("player_id")["receptions"].shift(1)
df["prev_receiving_yards"] = df.groupby("player_id")["receiving_yards"].shift(1)
df["prev_rushing_yards"] = df.groupby("player_id")["rushing_yards"].shift(1)
df["prev_rushing_tds"] = df.groupby("player_id")["rushing_tds"].shift(1)
df["prev_receiving_tds"] = df.groupby("player_id")["receiving_tds"].shift(1)

df["prev_3_avg"] = df.groupby("player_id")["fantasy_points_ppr"].rolling(3).mean().shift(1).reset_index(level=0, drop=True)
df["prev_5_avg"] = df.groupby("player_id")["fantasy_points_ppr"].rolling(5).mean().shift(1).reset_index(level=0, drop=True)
df["prev_3_targets_avg"] = df.groupby("player_id")["targets"].rolling(3).mean().shift(1).reset_index(level=0, drop=True)
df["prev_5_targets_avg"] = df.groupby("player_id")["targets"].rolling(5).mean().shift(1).reset_index(level=0, drop=True)
df["prev_3_carries"] = df.groupby("player_id")["carries"].rolling(3).mean().shift(1).reset_index(level=0, drop=True)
df["prev_5_carries"] = df.groupby("player_id")["carries"].rolling(5).mean().shift(1).reset_index(level=0, drop=True)
df["receptions_avg_3"] = df.groupby("player_id")["receptions"].rolling(3).mean().shift(1).reset_index(level=0, drop=True)
df["receptions_avg_5"] = df.groupby("player_id")["receptions"].rolling(5).mean().shift(1).reset_index(level=0, drop=True)
df["receiving_yards_avg_3"] = df.groupby("player_id")["receiving_yards"].rolling(3).mean().shift(1).reset_index(level=0, drop=True)
df["receiving_yards_avg_5"] = df.groupby("player_id")["receiving_yards"].rolling(5).mean().shift(1).reset_index(level=0, drop=True)
df["rushing_yards_avg_3"] = df.groupby("player_id")["rushing_yards"].rolling(3).mean().shift(1).reset_index(level=0, drop=True)
df["rushing_yards_avg_5"] = df.groupby("player_id")["rushing_yards"].rolling(5).mean().shift(1).reset_index(level=0, drop=True)
df["rushing_tds_avg_3"] = df.groupby("player_id")["rushing_tds"].rolling(3).mean().shift(1).reset_index(level=0, drop=True)
df["rushing_tds_avg_5"] = df.groupby("player_id")["rushing_tds"].rolling(5).mean().shift(1).reset_index(level=0, drop=True)
df["receiving_tds_avg_3"] = df.groupby("player_id")["receiving_tds"].rolling(3).mean().shift(1).reset_index(level=0, drop=True)
df["receiving_tds_avg_5"] = df.groupby("player_id")["receiving_tds"].rolling(5).mean().shift(1).reset_index(level=0, drop=True)

df.to_sql("feature_set_2026", conn, if_exists="replace", index=False)

conn.close()

print("Feature set for 2026 created successfully!")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")