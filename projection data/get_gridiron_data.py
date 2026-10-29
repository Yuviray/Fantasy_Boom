import os
import sqlite3
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(str(env_path))

year = 2026

DB_PATH = Path(__file__).parent.parent / "fantasy_data.db"
CSV_PATH = Path(__file__).parent.parent / "historical data" / f"gridiron_projections_{year}.csv"

API = "https://api.gridirondata.com/api/v1"
HEADERS = {"x-api-key": os.getenv("GRIDIRON_API_KEY")}

if not HEADERS["x-api-key"]:
    raise ValueError("GRIDIRON_API_KEY was not found in .env")

all_projections = []

for week in range(1, 9):
    response = requests.get(
        f"{API}/projections/{week}",
        headers=HEADERS,
        params={
            "season": year,
            "scoring": "ppr",
            "source": "weekly",
        },
        timeout=30,
    )

    print(f"Week {week}: HTTP {response.status_code}")

    response.raise_for_status()
    data = response.json()
    projections = data.get("projections", [])

    for player in projections:
        if player.get("position") not in {"QB", "RB", "WR", "TE"}:
            continue

        all_projections.append({
            "season": year,
            "week": int(player.get("week", week)),
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

df.to_csv(CSV_PATH, index=False)

with sqlite3.connect(DB_PATH) as conn:
    df.to_sql(
        f"gridiron_projections_{year}",
        conn,
        if_exists="replace",
        index=False,
    )

print("\nTotal projection rows:", len(df))
print("\nRows by week:")
print(df.groupby("week").size().to_string())
print("\nRows by position:")
print(df.groupby("position").size().to_string())
print("\nSaved CSV:", CSV_PATH)
print(f"Saved SQLite table: gridiron_projections_{year}")