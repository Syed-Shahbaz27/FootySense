# Library that will make API key talk to the internet.
from dotenv import load_dotenv
import os
load_dotenv()

import requests
API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE_URL ="https://api.football-data.org/v4/"
headers = {"X-Auth-Token": API_KEY}
#Api call 
response = requests.get(BASE_URL +"competitions/PL/scorers",headers = headers)

#JSON AND FOR LOOP
data = response.json()
print("These are the premier league top scorers ranked from top to bottom: \n")
for scorer in data ["scorers"]:
  print(scorer["player"]["name"],"-",scorer['goals'],"-",scorer["team"]["name"])
