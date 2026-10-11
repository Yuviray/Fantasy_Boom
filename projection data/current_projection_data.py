import os
from dotenv import load_dotenv
from espn_api.football import League
import pandas as pd
from pathlib import Path
import sqlite3


env_path = Path(__file__).parent.parent / ".env"
load_dotenv(str(env_path))

folder_path = Path(__file__).parent.parent / "projection data" / "weekly projections"



TABLE_NAME = "espn_projections_2026"

proj_week = 5

league = League(
    league_id=os.getenv("LEAGUE_ID"),
    year=2026,
    espn_s2=os.getenv("ESPN_S2"),
    swid=os.getenv("ESPN_SWID")
    
)

with sqlite3.connect("fantasy_data.db") as conn:
    conn.execute("""CREATE TABLE IF NOT EXISTS espn_projections_2026 (
        player_name TEXT,
        player_id INTEGER,
        position TEXT,
        week INTEGER,
        projected_points REAL
        )
    """)
    conn.execute("""
                 CREATE UNIQUE INDEX IF NOT EXISTS idx_player_week
                 ON espn_projections_2026 (player_id, week)
                 """)       


for i in range(1, proj_week + 1):
    print(f"Week {i} projections:")

    players = league.free_agents(
        week=i,
        size=1000
    )



    rows = []

    for player in players:
        if player.position not in ["QB", "RB", "WR", "TE"]:
            continue

        week_stats = player.stats.get(i, {})

        if "projected_points" not in week_stats:
            continue

        rows.append({
            "player_name": player.name,
            "player_id": player.playerId,
            "position": player.position,
            "week": i,
            "projected_points": week_stats["projected_points"]
        })

    projections = pd.DataFrame(rows)

    #print("Shape:", projections.shape)
    #print(projections.head(20))

    projections.to_csv(
        folder_path / f"espn_projections_2026_week{i}.csv",
        index=False
    )
    
    with sqlite3.connect("fantasy_data.db") as conn:
        conn.executemany(f"""
            INSERT OR REPLACE INTO {TABLE_NAME} (player_name, player_id, position, week, projected_points)
            VALUES (:player_name, :player_id, :position, :week, :projected_points)
        """, projections.to_dict(orient="records"))

    #print(f"Saved {len(projections)} projections for week {i} to database.")
print(f"Database '{TABLE_NAME}' updated with projections for weeks 1 to {proj_week}.")