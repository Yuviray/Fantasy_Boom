import sqlite3
import pandas as pd
import os

DB_PATH = "fantasy_data.db"
TARGET_SEASON = 2026
TARGET_WEEK = int(os.getenv("CURRENT_WEEK", 9))

with sqlite3.connect(DB_PATH) as conn:
    df = pd.read_sql_query(
        """
        SELECT *
        FROM feature_set_2026
        WHERE season = ?
          AND week < ?
        """,
        conn,
        params=(TARGET_SEASON, TARGET_WEEK)
    )


df = df.sort_values(["player_id", "week"]).copy()


previous_columns = {
    "previous_ppr": "fantasy_points_ppr",
    "prev_targets": "targets",
    "prev_carries": "carries",
    "prev_receptions": "receptions",
    "prev_receiving_yards": "receiving_yards",
    "prev_rushing_yards": "rushing_yards",
    "prev_rushing_tds": "rushing_tds",
    "prev_receiving_tds": "receiving_tds"
}

for new_col, source_col in previous_columns.items():
    df[new_col] = df.groupby("player_id")[source_col].transform(
        lambda s: s.shift(0)
    )


rolling_columns = {
    "prev_3_avg": ("fantasy_points_ppr", 3),
    "prev_5_avg": ("fantasy_points_ppr", 5),
    "prev_3_targets_avg": ("targets", 3),
    "prev_5_targets_avg": ("targets", 5),
    "prev_3_carries": ("carries", 3),
    "prev_5_carries": ("carries", 5),
    "receptions_avg_3": ("receptions", 3),
    "receptions_avg_5": ("receptions", 5),
    "receiving_yards_avg_3": ("receiving_yards", 3),
    "receiving_yards_avg_5": ("receiving_yards", 5),
    "rushing_yards_avg_3": ("rushing_yards", 3),
    "rushing_yards_avg_5": ("rushing_yards", 5),
    "rushing_tds_avg_3": ("rushing_tds", 3),
    "rushing_tds_avg_5": ("rushing_tds", 5),
    "receiving_tds_avg_3": ("receiving_tds", 3),
    "receiving_tds_avg_5": ("receiving_tds", 5)
}

for new_col, (source_col, window) in rolling_columns.items():
    df[new_col] = (
        df.groupby("player_id")[source_col]
          .transform(lambda s: s.rolling(window).mean())
    )

latest_features = (
    df.sort_values("week")
      .drop_duplicates("player_id", keep="last")
)

with sqlite3.connect(DB_PATH) as conn:
    projections = pd.read_sql_query(
        """
        SELECT *
        FROM gridiron_projections_2026
        WHERE season = ?
          AND week = ?
          AND position IN ('QB', 'RB', 'WR', 'TE')
        """,
        conn,
        params=(TARGET_SEASON, TARGET_WEEK)
    )


prediction_df = projections.merge(
    latest_features,
    left_on="player_name",
    right_on="player_display_name",
    how="left",
    suffixes=("_projection", "_stats")
)


with sqlite3.connect(DB_PATH) as conn:
    prediction_df.to_sql(
        "current_week",
        conn,
        if_exists="replace",
        index=False
    )

print(f"Week {TARGET_WEEK} projected players: {len(prediction_df)}")
print(prediction_df.head())
    