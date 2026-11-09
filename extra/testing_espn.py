import sqlite3
import pandas as pd

conn = sqlite3.connect("fantasy_data.db")

df = pd.read_sql_query("""
    SELECT *
    FROM Model_training_data_2026
""", conn)

conn.close()

print("Dataset shape:", df.shape)
print("\nWeeks available:")
print(df.groupby("week").size())

print("\nProjections by week:")
print(df.groupby("week")["projected_points"].count())

print("\nBoom labels by class:")
print(df["Boom"].value_counts(dropna=False).sort_index())

print("\nUsable labeled rows:", df["Boom"].notna().sum())

print("\nFeature columns:")
print(df.columns.tolist())

with sqlite3.connect("fantasy_data.db") as conn:

    print("GRIDIRON:")
    print(pd.read_sql_query(
        """
        SELECT player_name
        FROM gridiron_projections_2026
        WHERE season = ?
          AND player_name LIKE '%Kenneth Walker%'
        """,
        conn,
        params=(2026,)
    ))

    print("\nFEATURE SET:")
    print(pd.read_sql_query(
        """
        SELECT DISTINCT player_display_name
        FROM feature_set_2026
        WHERE season = ?
          AND player_display_name LIKE '%Kenneth Walker%'
        """,
        conn,
        params=(2026,)
    ))