import sqlite3
import pandas as pd

DB_PATH = "fantasy_data.db"
TARGET_SEASON = 2026
TARGET_WEEK = 8

with sqlite3.connect(DB_PATH) as conn:

    query = """
    WITH latest_features AS (
        SELECT
            f.*,
            ROW_NUMBER() OVER (
                PARTITION BY f.player_display_name
                ORDER BY f.week DESC
            ) AS rn
        FROM feature_set_2026 AS f
        WHERE f.season = ?
          AND f.week < ?
    )

    SELECT
        p.season,
        p.week,
        p.player_id AS projection_player_id,
        p.player_name,
        p.position,
        p.team,
        p.projected_points,
        p.injury_status,

        f.player_id AS nflverse_player_id,
        f.player_display_name,
        f.opponent_team,

        f.previous_ppr,
        f.prev_targets,
        f.prev_carries,
        f.prev_receptions,
        f.prev_receiving_yards,
        f.prev_rushing_yards,
        f.prev_rushing_tds,
        f.prev_receiving_tds,
        f.prev_3_avg,
        f.prev_5_avg,
        f.prev_3_targets_avg,
        f.prev_5_targets_avg,
        f.prev_3_carries,
        f.prev_5_carries,
        f.receptions_avg_3,
        f.receptions_avg_5,
        f.receiving_yards_avg_3,
        f.receiving_yards_avg_5,
        f.rushing_yards_avg_3,
        f.rushing_yards_avg_5,
        f.rushing_tds_avg_3,
        f.rushing_tds_avg_5,
        f.receiving_tds_avg_3,
        f.receiving_tds_avg_5

    FROM gridiron_projections_2026 AS p

    LEFT JOIN latest_features AS f
        ON p.player_name = f.player_display_name
       AND f.rn = 1

    WHERE p.season = ?
      AND p.week = ?
      AND p.position IN ('QB', 'RB', 'WR', 'TE')
    """

    prediction_df = pd.read_sql_query(
        query,
        conn,
        params=(TARGET_SEASON, TARGET_WEEK, TARGET_SEASON, TARGET_WEEK)
    )
    
    prediction_df.to_sql(
            "current_week",
            conn,
            if_exists="replace",
            index=False 
            
        )

print(f"Week {TARGET_WEEK} projected players: {len(prediction_df)}")
print(prediction_df.head())
    