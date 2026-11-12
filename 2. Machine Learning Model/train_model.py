# FootySense - train the match predictor on PRE-MATCH features only.
# Run from the project root:  python "2. Machine Learning Model/train_model.py"

import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

DATA_PATH = "2. Machine Learning Model/epl_final.csv"
MODEL_PATH = "model.pkl"   # main.py loads the model from the project root
WINDOW = 10                # same "last 10 matches" that main.py uses

# 1. Load the matches and sort them by date (oldest first).
df = pd.read_csv(DATA_PATH)
df["MatchDate"] = pd.to_datetime(df["MatchDate"])
df = df.sort_values("MatchDate").reset_index(drop=True)


# 2. Build pre-match features.
#    For every match, average each team's stats over its previous 10 matches.
#    shift(1) moves the numbers down one row, so a match never sees its own stats.
def rolling_before(team_col, stat_col):
    return (
        df.groupby(team_col)[stat_col]
          .transform(lambda s: s.shift(1).rolling(WINDOW, min_periods=5).mean())
    )

# Home team: its last 10 HOME games. Away team: its last 10 AWAY games.
# This matches exactly how main.py builds features at prediction time.
for stat in ["Shots", "ShotsOnTarget", "Corners"]:
    df[f"Home{stat}"] = rolling_before("HomeTeam", f"Home{stat}")
    df[f"Away{stat}"] = rolling_before("AwayTeam", f"Away{stat}")

FEATURES = ["HomeShots", "AwayShots",
            "HomeShotsOnTarget", "AwayShotsOnTarget",
            "HomeCorners", "AwayCorners"]
TARGET = "FullTimeResult"

# Drop early matches where a team has fewer than 5 previous games.
df = df.dropna(subset=FEATURES)


# 3. Split by time: train on older seasons, test on the newest 20%.
#    A random split would let the model learn from the future.
cutoff = df["MatchDate"].quantile(0.8)
train = df[df["MatchDate"] <= cutoff]
test = df[df["MatchDate"] > cutoff]


# 4. Train the Random Forest.
#    min_samples_leaf=20 stops trees memorising single matches (and keeps model.pkl small).
model = RandomForestClassifier(n_estimators=300, min_samples_leaf=20, random_state=42)
model.fit(train[FEATURES], train[TARGET])


# 5. Evaluate against a simple baseline: always predict a home win.
accuracy = accuracy_score(test[TARGET], model.predict(test[FEATURES]))
baseline = (test[TARGET] == "H").mean()
print(f"Test period: {test['MatchDate'].min().date()} to {test['MatchDate'].max().date()} ({len(test)} matches)")
print(f"Model accuracy:         {accuracy:.1%}")
print(f"Always-home baseline:   {baseline:.1%}")


# 6. Retrain on ALL matches so the live app uses the most data, then save.
model.fit(df[FEATURES], df[TARGET])
with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)
print(f"Saved model to {MODEL_PATH}")
