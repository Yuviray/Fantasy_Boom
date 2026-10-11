import sqlite3
import pandas as pd

projections = pd.read_csv("espn_projections_2026_week4.csv")

conn = sqlite3.connect("fantasy_data.db")

projections.to_sql(
    "espn_projections_2026",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Saved", len(projections), "projections")