import nflreadpy as nfl
import polars as pl

print("Loading 2026 player stats...")

stats = nfl.load_player_stats(
    seasons=2026,
    summary_level="week"
)

print("Original shape:", stats.shape)

# Keep fantasy-relevant positions
stats = stats.filter(
    pl.col("position").is_in(["QB", "RB", "WR", "TE"])
)

print("Filtered shape:", stats.shape)

print("\nPositions:")
print(stats["position"].value_counts())

# Save
stats.write_parquet("nfl_stats_2026.parquet")

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

print("Cleaned shape:", stats.shape)

stats.write_parquet("nfl_stats_2026_clean.parquet")

print("Saved: nfl_stats_2026_clean.parquet")