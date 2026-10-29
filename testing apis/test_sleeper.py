import sqlite3
import pandas as pd

with sqlite3.connect("fantasy_data.db") as conn:
    for table in ["player_stats_2026", "gridiron_projections_2026"]:
        print(f"\n{table}")
        print(pd.read_sql_query(
            f"PRAGMA table_info({table})", conn
        )[["name", "type"]].to_string(index=False))

        print(pd.read_sql_query(
            f"SELECT * FROM {table} ORDER BY week DESC LIMIT 3", conn
        ).to_string(index=False))