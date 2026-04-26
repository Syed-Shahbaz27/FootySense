from dotenv import load_dotenv
import os
load_dotenv()
import requests
API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE_URL = "https://api.football-data.org/v4/"
headers = {"X-Auth-Token": API_KEY}
response = requests.get (
  BASE_URL + "competitions/PL/teams",
  headers=headers
  )

data = response.json()
for team in data ["teams"]:
  print(team["name"], "-", team["venue"])
