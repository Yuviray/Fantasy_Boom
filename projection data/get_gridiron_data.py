import os
import sqlite3
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import nflreadpy as nfl
import pandas as pd

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(str(env_path))

YEAR = 2026
CURRENT_WEEK = int(os.getenv("CURRENT_WEEK", 9))

DB_PATH = Path(__file__).parent.parent / "fantasy_data.db"
CSV_PATH = Path(__file__).parent.parent / "historical data" / f"gridiron_projections_{YEAR}.csv"

API = "https://api.gridirondata.com/api/v1"
HEADERS = {"x-api-key": os.getenv("GRIDIRON_API_KEY")}

if not HEADERS["x-api-key"]:
    raise ValueError("GRIDIRON_API_KEY was not found in .env")



TABLE_NAME = f"gridiron_projections_{YEAR}" 


schedule = nfl.load_schedules(seasons=YEAR).to_pandas()

schedule = schedule[schedule["week"] == CURRENT_WEEK]

home_teams = schedule[["week", "home_team", "away_team"]].copy()

home_teams = home_teams.rename(columns={
    "home_team": "team",
    "away_team": "opponent_team"
})

away_teams = schedule[["week", "away_team", "home_team"]].copy()

away_teams = away_teams.rename(columns={
    "away_team": "team",
    "home_team": "opponent_team"
})

team_opponents = pd.concat(
    [home_teams, away_teams],
    ignore_index=True
)


response = requests.get(
    f"{API}/projections/{CURRENT_WEEK}",
    headers=HEADERS,
    params={
        "season": YEAR,
        "scoring": "ppr",
        "source": "weekly",
    },
    timeout=30,
)

print(f"Week {CURRENT_WEEK}: HTTP {response.status_code}")

response.raise_for_status()
data = response.json()
projections = data.get("projections", [])

all_projections = []



for player in projections:
        if player.get("position") not in {"QB", "RB", "WR", "TE"}:
            continue

        all_projections.append({
            "season": YEAR,
            "week": int(player.get("week", CURRENT_WEEK)),
            "player_id": player.get("player_id"),
            "player_name": player.get("player_name"),
            "position": player.get("position"),
            "team": player.get("team"),
            "projected_points": player.get("projected_points"),
            "projection_source": player.get("projection_source"),
            "injury_status": player.get("injury_status"),
        })

df = pd.DataFrame(all_projections)

if df.empty:
    raise ValueError("No weekly projections were returned.")

df = df.drop_duplicates(
    subset=["season", "week", "player_id"],
    keep="last",
)

team_opponents["team"] = team_opponents["team"].replace({
    "LA": "LAR"
})

df = df.merge(
    team_opponents,
    on=["week", "team"],
    how="left"
)

with sqlite3.connect(DB_PATH) as conn:
    columns = pd.read_sql_query(
        "PRAGMA table_info(gridiron_projections_2026)",
        conn
    )["name"].tolist()

    if "opponent_team" not in columns:
        conn.execute("""
            ALTER TABLE gridiron_projections_2026
            ADD COLUMN opponent_team TEXT
        """)
    
    df.head(0).to_sql(
        TABLE_NAME,
        conn,
        if_exists="append",
        index=False
    )
    #conn.execute("DROP INDEX IF EXISTS IDX_GRIDIRON_PLAYER_WEEK")
    conn.execute(f"""
        CREATE UNIQUE INDEX IF NOT EXISTS IDX_GRIDIRON_PLAYER_WEEK ON {TABLE_NAME}(player_id, season, week)
    """)
    
    columns = df.columns.tolist()
    
    quoted_columns = ", ".join(f'"{c}"' for c in columns)
    placeholders = ", ".join("?" for _ in columns)
    
    
    update_columns = [
        c for c in columns
        if c not in ["player_id", "season", "week"]
    ]
    
    update_clause = ", ".join(f'"{c}" = excluded."{c}"'
                              for c in update_columns)
    
    sql = f"""
        INSERT INTO {TABLE_NAME} ({quoted_columns})
        VALUES ({placeholders})
        ON CONFLICT (player_id, season, week)
        DO UPDATE SET {update_clause}
    """
    
    conn.executemany(
        sql,
        df.itertuples(index=False, name=None)
    )
    
if CSV_PATH.exists():

    old_df = pd.read_csv(CSV_PATH)

    combined_df = pd.concat(
        [old_df, df],
        ignore_index=True
    )

    combined_df = combined_df.drop_duplicates(
        subset=["season", "week", "player_id"],
        keep="last"
    )

else:
    combined_df = df.copy()

combined_df.to_csv(CSV_PATH, index=False)

print("\nTotal projection rows:", len(df))
print("\nRows by week:")
print(df.groupby("week").size().to_string())
print("\nRows by position:")
print(df.groupby("position").size().to_string())
print("\nSaved CSV:", CSV_PATH)
print(f"Saved SQLite table: gridiron_projections_{YEAR}")