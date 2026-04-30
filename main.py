import pandas as pd
import pickle
from fastapi import FastAPI
from pydantic import BaseModel

# 1. Load the model and data 
# Error handling for startup safety
try:
    model = pickle.load(open("model.pkl", "rb"))
    df = pd.read_csv("epl_final.csv")
    print("Model and dataset loaded successfully")
except Exception as e:
    print("Startup failure:", e)


#2. The Bridge: MAPS API names to epl_final.csv names
TEAM_NAMES_MAP ={
    "Arsenal FC": "Arsenal",
    "Aston Villa FC": "Aston Villa", 
    "Chelsea FC": "Chelsea", 
    "Everton FC": "Everton", 
    "Fulham FC": "Fulham", 
    "Liverpool FC": "Liverpool", 
    "Manchester City FC": "Man City", 
    "Manchester United FC": "Man United", 
    "Newcastle United FC": "Newcastle", 
    "Tottenham Hotspur FC": "Tottenham", 
    "Wolverhampton Wanderers FC": "Wolves", 
    "Burnley FC": "Burnley", 
    "Nottingham Forest FC": "Nott'm Forest", 
    "Crystal Palace FC": "Crystal Palace", 
    "Brighton & Hove Albion FC": "Brighton", 
    "Brentford FC": "Brentford", 
    "West Ham United FC": "West Ham", 
    "AFC Bournemouth": "Bournemouth", 
    "Luton Town FC": "Luton", 
    "Sheffield United FC": "Sheffield United"
}
@app.post("/predict") 
def predict(request: MatchRequest):
    # 1. Normalize names 
        h_name = TEAM_NAME_MAP.get(request.home_team, request.home_team) a_name = TEAM_NAME_MAP.get(request.away_team, request.away_team)

# Get recent form (Last 10 games)
home_recent = df[df['HomeTeam'] == h_name]


if h_name not in df["HomeTeam"].values and h_name not in df["AwayTeam"].values:
    return {"error": f"Team '{request.home_team}' not found in dataset"}

if a_name not in df["HomeTeam"].values and a_name not in df["AwayTeam"].values:
    return {"error": f"Team '{request.away_team}' not found in dataset"}