import sqlite3

db_path = r"C:\Users\yuvi_\Desktop\Fantasy_Boom\fantasy_data.db"

conn = sqlite3.connect(db_path)

cursor = conn.cursor()

# Number of rows
cursor.execute("SELECT COUNT(*) FROM player_stats")
print("Rows:", cursor.fetchone()[0])

# Number of columns
cursor.execute("PRAGMA table_info(player_stats)")
columns = cursor.fetchall()
print("Columns:", len(columns))

# Seasons
cursor.execute("""
    SELECT season, COUNT(*)
    FROM player_stats
    GROUP BY season
    ORDER BY season
""")

print("\nRows by season:")
for row in cursor.fetchall():
    print(row)

conn.close()