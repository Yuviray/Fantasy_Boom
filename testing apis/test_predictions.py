import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
print("API key loaded:", API_KEY is not None)
print("API key length:", len(API_KEY) if API_KEY else 0)

url = "https://api.fantasypros.com/public/v2/json/nfl/2026/projections"

headers = {
    "x-api-key": API_KEY
}

params = {
    "week": 4,
    "scoring": "PPR",
    "position": "QB"
}

response = requests.get(
    url,
    params=params,
    headers=headers
)

print("Status:", response.status_code)

data = response.json()

print("\nResponse keys:")
print(data.keys())

print("\nCount:", data.get("count"))

print("\nReturned players:", len(data.get("players", [])))

print("\nFirst player:")
print(data.get("players", [])[0])