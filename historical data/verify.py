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

print("Shape:", stats.shape)
print("Seasons:", stats["season"].unique().sort())

duplicates = (
    stats
    .group_by(["player_id", "season", "week", "season_type"])
    .len()
    .filter(pl.col("len") > 1)
)

print("Duplicate groups:", duplicates.height)
print(duplicates.head(20))

null_counts = (
    stats
    .null_count()
    .transpose(
        include_header=True,
        header_name="column"
    )
    .rename({"column_0": "null_count"})
    .filter(pl.col("null_count") > 0)
    .sort("null_count", descending=True)
)

print(null_counts)


for column in stats.columns:
    print(column)