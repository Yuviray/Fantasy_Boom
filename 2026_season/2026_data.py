import nflreadpy as nfl
import polars as pl

from pathlib import Path


folder = Path(__file__).parent.parent /"2026_season"

print("Loading 2026 player stats...")

stats = nfl.load_player_stats(
    seasons=2026,
    summary_level="week"
)

print("Original shape:", stats.shape)

stats = stats.filter(
    pl.col("position").is_in(["QB", "RB", "WR", "TE"])
)

print("Filtered shape:", stats.shape)

print("\nPositions:")
print(stats["position"].value_counts())

print("\nWeeks available:")
print(
    stats.group_by("week")
    .agg(pl.len().alias("player_rows"))
    .sort("week")
)


stats.write_parquet(folder / "nfl_stats_2026.parquet")

print("\nSaved: nfl_stats_2026.parquet")

columns_to_remove = [
    col for col in stats.columns
    if col.startswith("def_")
    or col.startswith("fg_")
    or col.startswith("pat_")
    or col.startswith("gwfg_")
    or col.startswith("pt_")
]

stats = stats.drop(columns_to_remove)


stats.write_parquet(folder / "nfl_stats_2026_clean.parquet")

print("Saved: nfl_stats_2026_clean.parquet")