
import sqlite3
import pandas as pd

conn = sqlite3.connect("fantasy_data.db")

print("=== 2026 ACTUAL STATS BY WEEK ===")
print(pd.read_sql_query("""
    SELECT
        week,
        COUNT(*) AS player_rows,
        COUNT(fantasy_points_ppr) AS rows_with_actual_ppr
    FROM player_stats_2026
    GROUP BY week
    ORDER BY week
""", conn))

print("\n=== WEEK 4 PROJECTIONS ===")
print(pd.read_sql_query("""
    SELECT
        COUNT(*) AS projected_players,
        COUNT(projected_points) AS rows_with_projection
    FROM espn_projections_2026
    WHERE week = 4
""", conn))

print("\n=== WEEK 4 PROJECTION SAMPLE ===")
print(pd.read_sql_query("""
    SELECT *
    FROM espn_projections_2026
    WHERE week = 4
    LIMIT 10
""", conn))

conn.close()