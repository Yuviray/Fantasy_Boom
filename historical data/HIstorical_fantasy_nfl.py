import nflreadpy as nfl
from pathlib import Path

print("Loading NFL data...")


folder = Path(r"C:\Users\yuvi_\Desktop\Fantasy_Boom\historical data\2021-2025")
folder.mkdir(parents=True, exist_ok=True)
for season in [2021, 2022, 2023, 2024, 2025]:
    print(f"Loading {season}...")
    stats = nfl.load_player_stats(season)
    stats = stats.filter(
        stats["position"].is_in(["QB", "RB", "WR", "TE"])
    )
    stats.write_parquet(folder / f"nfl_stats_{season}.parquet")
    print(f"Saved nfl_stats_{season}.parquet")

