import sqlite3
import polars as pl
import pandas as pd

from pathlib import Path

folder = Path(__file__).parent.parent /"2026_season"

stats = pl.read_parquet(folder / "nfl_stats_2026_clean.parquet").to_pandas()

db ="fantasy_data.db"

table_name = "player_stats_2026"



with sqlite3.connect(db) as conn:
    stats.head(0).to_sql(
        table_name,
        conn,
        if_exists="append",
        index=False
    )
    conn.execute("DROP INDEX IF EXISTS IDX_PLAYER_WEEK")
    conn.execute(f"""
        CREATE UNIQUE INDEX IF NOT EXISTS IDX_PLAYER_WEEK ON {table_name}(player_id, season, week)
    """)
    
    columns = stats.columns.tolist()
    
    quoted_columns = ", ".join(f'"{c}"' for c in columns)
    placeholders = ", ".join("?" for _ in columns)
    
    
    update_columns = [
        c for c in columns
        if c not in ["player_id", "season", "week"]
    ]
    
    update_clause = ", ".join(f'"{c}" = excluded."{c}"'
                              for c in update_columns)
    
    sql = f"""
        INSERT INTO {table_name} ({quoted_columns})
        VALUES ({placeholders})
        ON CONFLICT (player_id, season, week)
        DO UPDATE SET {update_clause}
    """
    
    conn.executemany(
        sql,
        stats.itertuples(index=False, name=None)
    )

print("2026 data added successfully!")
