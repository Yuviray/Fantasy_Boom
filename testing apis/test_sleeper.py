import requests

league_id = "1389736777807335424"

url = f"https://api.sleeper.app/v1/league/{league_id}/rosters"

response = requests.get(url)

print("Status:", response.status_code)

rosters = response.json()

print("Number of rosters:", len(rosters))

for roster in rosters:
    print("\nRoster ID:", roster["roster_id"])
    print("Players:", len(roster.get("players", [])))
    print("Player IDs:", roster.get("players", []))