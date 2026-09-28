import polars as pl

from pathlib import Path 

folder = Path(r"C:\Users\yuvi_\Desktop\Fantasy_Boom\historical data\2021-2025")

files = [
    folder / f"nfl_stats_2021.parquet",
    folder / f"nfl_stats_2022.parquet",
    folder / f"nfl_stats_2023.parquet",
    folder / f"nfl_stats_2024.parquet",
    folder / f"nfl_stats_2025.parquet"
]

stats = pl.concat([
    pl.read_parquet(file)
    for file in files
])

print("BEFORE CLEANING")
print(
    stats
    .group_by("position")
    .len()
    .sort("position")
)
# Columns that are clearly defensive
defensive_cols = [
    col for col in stats.columns
    if col.startswith("def_")
]

# Kicking columns
kicking_cols = [
    col for col in stats.columns
    if (
        col.startswith("fg_")
        or col.startswith("pat_")
        or col.startswith("gwfg_")
    )
]

# Punting columns
punting_cols = [
    col for col in stats.columns
    if col.startswith("pt_")
]

# Remove those categories
columns_to_remove = defensive_cols + kicking_cols + punting_cols

clean_stats = stats.drop(columns_to_remove)

print("Original columns:", len(stats.columns))
print("Clean columns:", len(clean_stats.columns))
print("\nRemoved:", len(columns_to_remove))
print("\nRemaining columns:")
print(clean_stats.columns)

clean_stats.write_parquet(folder / "nfl_stats_clean.parquet")

print("\nAFTER CLEANING")
print(
    clean_stats
    .group_by("position")
    .len()
    .sort("position")
)
print(clean_stats.shape)
print(len(clean_stats.columns))