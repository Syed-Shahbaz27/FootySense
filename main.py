# This .py is the backend of our ML app it connects our database and model together.

from fastapi import FastAPI
from pydantic import BaseModel
import pickle 
import pandas as pd 
import sqlite3

app = FastAPI()

#1. HOME ENDPOINT 
@app.get("/")
def home():
    return {"message": "Our Footysense API is running!"} 

# 2. TEAMS ENDPOINT 
@app.get("/teams")
def get_teams():
    conn = sqlite3.connect("footysense.db")
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM teams")
    result = cursor.fetchall()
    conn.close()
    return {"teams": result}

#3. SCORERS ENDPOINT
@app.get("/scorers")
def get_scorers():
    # NOTE: Ensure this path is correct.
    conn = sqlite3.connect("footysense.db")
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM scorers")
    result_1 = cursor.fetchall()
    conn.close()
    return {"scorers": result_1}

#  4. PREDICTION SETUP
class MatchRequest(BaseModel):
    home_team: str
    away_team: str

# Load Model and CSV 
model = pickle.load(open("model.pkl", "rb"))
df = pd.read_csv("2. Machine Learning Model/epl_final.csv")

#  5. PREDICT ENDPOINT 
@app.post("/predict")
def predict(request: MatchRequest):
    # A. Home Team's Average Stats (When playing at Home)
    home_data = df[df['HomeTeam'] == request.home_team]
    
    avg_home_shots = home_data['HomeShots'].mean()
    avg_home_sot = home_data['HomeShotsOnTarget'].mean()
    avg_home_corners = home_data['HomeCorners'].mean()

    # B. Away Team's Average Stats (When playing Away)
    away_data = df[df['AwayTeam'] == request.away_team]
    
    avg_away_shots = away_data['AwayShots'].mean()
    avg_away_sot = away_data['AwayShotsOnTarget'].mean()
    avg_away_corners = away_data['AwayCorners'].mean()

    # C. Fill missing values with 0 (if team not found)
    # This prevents the code from crashing if a team has no history
    values = [avg_home_shots, avg_away_shots, avg_home_sot, avg_away_sot, avg_home_corners, avg_away_corners]
    values = [0 if v != v else v for v in values] # NaN check

    # D. Create Feature List (Must match my Week 2 order)
    # Order: HomeShots, AwayShots, HomeSOT, AwaySOT, HomeCorners, AwayCorners
    features = [[
        values[0], values[1], values[2], values[3], values[4], values[5]
    ]]

    # E. Predict
    prediction = model.predict(features)
    probabilities = model.predict_proba(features)[0]
    classes = model.classes_  # ['A', 'D', 'H']

    prob_dict = {}
    for i, cls in enumerate(classes):
        prob_dict[cls] = round(float(probabilities[i]) * 100, 1)

    return {
    "home_team": request.home_team,
    "away_team": request.away_team,
    "prediction": prediction[0],
    "probabilities": prob_dict
    }
    