import sqlite3
import pandas as pd

db_path = r"C:\Users\yuvi_\Desktop\Fantasy_Boom\fantasy_data.db"

conn = sqlite3.connect(db_path)

df = pd.read_sql_query("""
    SELECT
        fantasy_points_ppr,
        previous_ppr,
        prev_3_avg,
        prev_5_avg,
        prev_targets,
        prev_3_targets_avg,
        prev_5_targets_avg,
        prev_carries,
        prev_3_carries,
        prev_5_carries,
        prev_receptions,
        receptions_avg_3,
        receptions_avg_5,
        prev_receiving_yards,
        receiving_yards_avg_3,
        receiving_yards_avg_5,
        prev_rushing_yards,
        rushing_yards_avg_3,
        rushing_yards_avg_5,
        prev_rushing_tds,
        rushing_tds_avg_3,
        rushing_tds_avg_5,
        prev_receiving_tds,
        receiving_tds_avg_3,
        receiving_tds_avg_5
    FROM feature_set
""", conn)

conn.close()

correlations = (
    df.corr(numeric_only=True)["fantasy_points_ppr"]
    .drop("fantasy_points_ppr")
    .sort_values(ascending=False)
)

correlation_data = correlations.reset_index()
correlation_data.columns = ["feature", "correlation"]
correlation_data.to_csv("correlation_data.csv", index=False)

print("\nCorrelation with PPR:\n")
print(correlation_data.to_string(index=False))