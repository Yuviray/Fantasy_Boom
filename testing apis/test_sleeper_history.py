import requests

player_id = "10229"  # Rashee Rice

url = f"https://api.sleeper.app/v1/stats/nfl/player/{player_id}"

response = requests.get(url)

print("Status:", response.status_code)
print(response.text[:5000])