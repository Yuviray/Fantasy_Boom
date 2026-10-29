import pandas as pd
from pathlib import Path


folder = Path(__file__).parent.parent /"models/training_data"


traing_data = pd.read_csv(folder / "train_data.csv")
validation_data = pd.read_csv(folder / "validation_data.csv")
test_data = pd.read_csv(folder / "test_data.csv")


for name,data in [("train_data", traing_data), ("validation_data", validation_data), ("test_data", test_data)]:
    print(f"{name}: {len(data)} rows, columns: {data.columns.tolist()}")
    print(f"Boom rate:\n{data['Boom'].mean()}")
    print(data["Boom"].value_counts())
    
    print(data["week"].value_counts())