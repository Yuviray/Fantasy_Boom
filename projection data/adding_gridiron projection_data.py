import os
from dotenv import load_dotenv
from espn_api.football import League
import pandas as pd
from pathlib import Path
import sqlite3


env_path = Path(__file__).parent.parent / ".env"
load_dotenv(str(env_path))

folder_path = Path(__file__).parent.parent / "projection data" / "weekly projections"



TABLE_NAME = "gridiron_projections_2026"

with sqlite3.connect("fantasy_data.db") as conn:
    query = """
    SELECT
        f.*,
        p.projected_points
    FROM feature_set_2026 AS f
    LEFT JOIN gridiron_projections_2026 AS p
    
        ON f.player_display_name = p.player_name AND f.week = p.week
    WHERE f.season = 2026
    """
    
    df = pd.read_sql_query(query, conn)
    
    df["points_diff"] = (df["fantasy_points_ppr"] - df["projected_points"])
    
    df["Boom"] = pd.NA
    valid = df["fantasy_points_ppr"].notna() & df["projected_points"].notna()
    
    df.loc[valid, "Boom"] = (df.loc[valid, "points_diff"] >= 5).astype(int)
    
    
    df.to_sql(
        "Model_training_data_2026",
        conn,
        if_exists="replace",
        index=False 
        
    )
    
    print("Saved", len(df), "rows to Model_training_data_2026")
    
    print("\n Boom distribution:")
    print(df["Boom"].value_counts())    
    print("\n example rows:")
    print(df[["player_display_name", "week", "fantasy_points_ppr", "projected_points", "points_diff", "Boom"]].head(10))