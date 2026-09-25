# 📊⚽ FootySense: Premier League Match Predictor

Football has been one of my primary interests growing up, I've loved watching live Premier League matches, I've also played in Oman at an academy level. With this in mind, I built FootySense.

A full-stack Machine Learning application that leverages historical data to predict the outcomes of English Premier League matches.

## 🌟 Highlights
* **End-to-End ML Pipeline:** Built a complete system from raw API data ingestion to a functional web interface.
* **Real-World Data:** Trained on a dataset of over 9,000 historical Premier League matches.
* **FastAPI Backend:** Developed a FastAPI backend to serve predictions and connect the web interface with the ML model and database.
* **Logic-Driven:** Addressed "Data Leakage" by ensuring the model only uses information available *before* kickoff.

## 🚀 Live Demo
[Click here to view the live app](https://footysense-app.onrender.com/)

## 📸 Preview 

**<img width="1901" height="839" alt="Screenshot 2026-05-02 025812" src="https://github.com/user-attachments/assets/1bd99889-3e58-4d5e-b53b-e3236a53fd78" />**


## 🧠 The Problem vs. The Solution
### The Problem
Football prediction is notably difficult due to the high variance of the sport. Many sports-based ML models suffer from **Data Leakage** (using end-of-game stats like "Goals Scored at Full Time Home / Away" to predict the "Result"), which leads to artificially high accuracy (99%) that fails in real-world use cases.

### The Solution
FootySense uses a **Random Forest Classifier** trained on pre-match features. It calculates historical averages of shots, shots on target, and corners. The API dynamically calculates each team's recent form using their last 10 matches, ensuring predictions reflect current performance rather than 24-year historical averages.

## 🛠️ Tech Stack
| Category | Technology |
| :--- | :--- |
| **Language** | Python |
| **Backend** | FastAPI, Uvicorn |
| **Database** | SQLite |
| **ML Model** | Scikit-Learn (Random Forest) |
| **Frontend** | Streamlit |
| **Data Handling** | Pandas, Requests |
| **Deployment** | Render |

## 📊 Model Performance
* **Accuracy:** ~52%
* **Features:** HomeShots, AwayShots, HomeShotsOnTarget, AwayShotsOnTarget, HomeCorners, AwayCorners
* **Data Source:** Live data via the [Football-Data.org](https://www.football-data.org/) API and historical Kaggle datasets.

## ⚙️ Engineering Decisions / Fixes I Did

**Data Leakage Fix:** Initial model showed 99% accuracy using 
post-match statistics. Identified and removed target-correlated 
features, correcting accuracy to a realistic 52%.

**Inference-Time Feature Calculation:** Users select team names 
only. API calculates historical averages at request time; no 
in-game stats are required from the user.

**Team Name Normalization:** Built TEAM_NAME_MAP dictionary to 
bridge naming mismatches between live API responses and the Kaggle 
historical dataset, resolving silent prediction failures.

**Asymmetric Keep-Alive Architecture:** Migrated from 
cron-job.org to UptimeRobot, monitoring only the backend 
`/health` endpoint every 5 minutes using lightweight GET/HEAD 
requests. The frontend is allowed to sleep naturally, reducing 
unnecessary backend/frontend compute usage.

**Lazy Loading Pipeline:** ML model and dataset load only on 
genuine prediction requests, not on health pings, keeping 
infrastructure monitoring lightweight.

**Cold Start UX:** Frontend implements a 25-attempt polling loop 
with 2-second timeouts, showing a loading spinner during backend 
warm-up instead of crashing with a 503 error.

## 🔧 Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/Syed-Shahbaz27/FootySense.git
cd FootySense
