import requests
import sqlite3
from dotenv import load_dotenv
import os
load_dotenv()
#API related coding
API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE_URL = "https://api.football-data.org/v4/"
headers = {"X-Auth-Token": API_KEY}
#Fetch teams
teams_response = requests.get (
  BASE_URL + "competitions/PL/teams",
  headers=headers
  )

# fetching top scorers
scorers_response = requests.get(
  BASE_URL +"competitions/PL/scorers",headers = headers
  )
teams_data = teams_response.json()
scorers_data = scorers_response.json()


# Connect to database (creates footysense.db file) 
con = sqlite3.connect('footysense.db')
#Create cursor (This executes SQL commands)
cursor = con.cursor()

#Create teams table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS teams(
               name TEXT, venue TEXT
               )
               ''')

# Create scores table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS scorers(
               player_name TEXT, goals INTEGER, team_name TEXT
               )
               ''')

#Insert each team
for team in teams_data ["teams"]:
  cursor.execute('''
  INSERT INTO TEAMS (name,venue)
   VALUES(?, ?)
               ''', (team["name"],team["venue"]))
  
# Insert goal scorer
for scorer in scorers_data ["scorers"]:
  cursor.execute('''
      INSERT INTO SCORERS (player_name,goals,team_name )
      VALUES (?,?,?)
        ''', (scorer["player"]["name"], scorer["goals"], scorer["team"]["name"]))

# Save changes
con.commit()
print(f"I have Inserted {len(teams_data['teams'])} teams into database!")
print(f"Also, successfully Inserted {len(scorers_data['scorers'])} goal scorers into database!")


# Additional code to show our database 
cursor.execute ("SELECT * FROM teams LIMIT 5")
print("\n First 5 teams:")
for row in cursor.fetchall():
  print(row)
cursor.execute ("SELECT * FROM teams LIMIT 3")
print("\n First 3 teams:")
for row in cursor.fetchall():
  print(row)


