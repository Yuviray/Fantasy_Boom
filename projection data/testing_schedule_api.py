import nflreadpy as nfl
import pandas as pd

YEAR = 2026
CURRENT_WEEK = 9

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

print(team_opponents.head())

print(schedule.columns.tolist())
print(schedule.head())