import os
from dotenv import load_dotenv
import pandas as pd
from pathlib import Path
import sqlite3


with sqlite3.connect("fantasy_data.db") as conn:
    
    for table in ["Model_training_data_2026", "Historical_training_data"]:
        query = f"""
        SELECT COUNT(*)  AS [Boom or Bust], Boom
        FROM "{table}"
        GROUP BY Boom
        """
    
        df = pd.read_sql_query(query, conn)
        
        print(f"{table} distribution:")
        
        print("\n Boom distribution:")
        print(df)
        query = f"""
            SELECT *
            FROM "{table}"
            """
        df2 = pd.read_sql_query(query, conn)
        
        print(f"\nTotal rows in {table}: {len(df2)}")
        print(f"Columns: {df2.columns.tolist()}")
        
        for col in df2.columns:
            if any(term in col.lower() for term in
                ["projected_points", "fantasy_points_ppr", "points_diff", "boom"]):
                print( f"{col}: missing={df2[col].isna().sum()}")