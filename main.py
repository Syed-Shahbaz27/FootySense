# FootySense Backend: Database + ML Predictions
from fastapi import FastAPI
from pydantic import BaseModel
import pickle 
import pandas as pd 
import sqlite3

app = FastAPI()

# --- 1. CONFIGURATION & LOADING ---
# Ensure your file paths are correct for Render!
try:
    model = pickle.load(open("model.pkl", "rb"))
    # Note: Using your original path. Change to "epl_final.csv" if you moved the file to the root.
    df = pd.read_csv("2. Machine Learning Model/epl_final.csv")
except Exception as e:
    print(f"CRITICAL ERROR LOADING ASSETS: {e}")

# The Bridge: Maps API names to epl_final.csv names
TEAM_NAME_MAP = {
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
    "Sheffield United FC": "Sheffield United",
    "Leeds United FC": "Leeds",
    "Sunderland AFC": "Sunderland"
}

class MatchRequest(BaseModel):
    home_team: str
    away_team: str

# --- 2. EXISTING DATABASE ENDPOINTS ---

@app.get("/")
def home():
    return {"message": "Our Footysense API is running!"} 

@app.get("/teams")
def get_teams():
    conn = sqlite3.connect("footysense.db")
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM teams")
    result = cursor.fetchall()
    conn.close()
    return {"teams": result}

@app.get("/scorers")
def get_scorers():
    conn = sqlite3.connect("footysense.db")
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM scorers")
    result_1 = cursor.fetchall()
    conn.close()
    return {"scorers": result_1}

# --- 3. UPGRADED PREDICT ENDPOINT ---
@app.post("/predict")
def predict(request: MatchRequest):
    # A. Normalize names using the Map
     h_name = TEAM_NAME_MAP.get(request.home_team, request.home_team)
     a_name = TEAM_NAME_MAP.get(request.away_team, request.away_team)

    # B. Get recent form (Last 10 games)
     home_recent = df[df['HomeTeam'] == h_name].tail(10)
     away_recent = df[df['AwayTeam'] == a_name].tail(10)

    # C. Debug Logging (Visible in Render Logs)
     print(f"DEBUG: Processing {h_name} vs {a_name}")

    # D. Fallback Hierarchy
     league = df 

     avg_h_shots = home_recent['HomeShots'].mean() if not home_recent.empty else league['HomeShots'].mean()
     avg_a_shots = away_recent['AwayShots'].mean() if not away_recent.empty else league['AwayShots'].mean()
     avg_h_sot = home_recent['HomeShotsOnTarget'].mean() if not home_recent.empty else league['HomeShotsOnTarget'].mean()
     avg_a_sot = away_recent['AwayShotsOnTarget'].mean() if not away_recent.empty else league['AwayShotsOnTarget'].mean()
     avg_h_corners = home_recent['HomeCorners'].mean() if not home_recent.empty else league['HomeCorners'].mean()
     avg_a_corners = away_recent['AwayCorners'].mean() if not away_recent.empty else league['AwayCorners'].mean()

    # E. Feature DataFrame (Matches your trained feature order)
     feature_cols = [
        "HomeShots", "AwayShots", 
        "HomeShotsOnTarget", "AwayShotsOnTarget", 
        "HomeCorners", "AwayCorners"
     ]
    
     X_input = pd.DataFrame([[
        avg_h_shots, avg_a_shots, 
        avg_h_sot, avg_a_sot, 
        avg_h_corners, avg_a_corners
    ]], columns=feature_cols)

    # F. Predict
     prediction = model.predict(X_input)[0]
     probs = model.predict_proba(X_input)[0]
     classes = model.classes_.tolist() # Likely ['A', 'D', 'H']
    
     return {
         "home_team": request.home_team,
         "away_team": request.away_team,
         "prediction": prediction,
         "probabilities": {
             "Home Win": round(probs[classes.index("H")] * 100, 1),
             "Draw": round(probs[classes.index("D")] * 100, 1),
             "Away Win": round(probs[classes.index("A")] * 100, 1)
         }
     }