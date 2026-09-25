# 📊⚽ FootySense: Premier League Match Predictor

Football has been one of my primary interests growing up. I've loved watching live Premier League matches, and I've also played in Oman at an academy level. With this in mind, I built FootySense.

A full-stack Machine Learning application that leverages historical data to predict the outcomes of English Premier League matches.

## 🌟 Highlights

* **End-to-End ML Pipeline:** Built a complete system from historical/API data processing to a functional web interface.

* **Real-World Data:** Trained on a dataset of over 9,000 historical Premier League matches.

* **FastAPI Backend:** Developed a FastAPI backend to serve team data, top scorers, and match predictions.

* **Logic-Driven:** Addressed data leakage by ensuring the model only uses information available before kickoff.

## 🚀 Live Demo

[Click here to view the live app](https://footysense-app.onrender.com/)

## 📸 Preview

<img width="1901" height="839" alt="FootySense Screenshot" src="https://github.com/user-attachments/assets/1bd99889-3e58-4d5e-b53b-e3236a53fd78" />

## 🧠 The Problem vs. The Solution

### The Problem

Football prediction is difficult due to the high variance of the sport. Sports-based ML models can also suffer from **data leakage**, such as using post-match statistics like "Goals Scored at Full Time Home / Away" to predict the final "Result". This can produce artificially high accuracy that does not reflect real-world prediction performance.

### The Solution

FootySense uses a **Random Forest Classifier** trained on pre-match features.

The system calculates historical averages of shots, shots on target, and corners. The API dynamically calculates each team's recent form using their last 10 matches, allowing predictions to reflect more recent performance rather than relying only on long-term historical averages.

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

The initial model produced approximately 99% accuracy due to data leakage from post-match statistics. After removing target-correlated features and using pre-match information, accuracy was approximately 52%.

## ⚙️ Engineering Decisions / Fixes

**Data Leakage Fix:** Initial model showed approximately 99% accuracy using post-match statistics. Identified and removed target-correlated features, reducing the result to approximately 52% after using pre-match features.

**Inference-Time Feature Calculation:** Users select team names only. The API calculates historical averages at request time, so no in-game statistics are required from the user.

**Team Name Normalization:** Built a `TEAM_NAME_MAP` dictionary to handle naming mismatches between live API responses and the historical dataset, preventing prediction failures caused by inconsistent team names.

**Backend Keep-Alive Architecture:** Migrated from cron-job.org to UptimeRobot, monitoring only the backend `/health` endpoint every 5 minutes using lightweight GET/HEAD requests. The frontend is allowed to sleep naturally, reducing unnecessary compute usage.

**Lazy Loading Pipeline:** The ML model and dataset are loaded only when a prediction request is made, rather than during health checks, keeping infrastructure monitoring lightweight.

**Cold Start UX:** The frontend retries the backend up to 25 times with 2-second request timeouts and retry delays, displaying a loading spinner while the free Render backend wakes up instead of failing immediately.

## 🔧 Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/Syed-Shahbaz27/FootySense.git
cd FootySense
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up environment variables**

Create `.env` file in root:
FOOTBALL_API_KEY=your_api_key_here

**4. Run FastAPI backend**
```bash
uvicorn main:app --reload
```

**5. Run Streamlit frontend (new terminal)**
```bash
streamlit run app.py
```

**6. Open browser at** `http://localhost:8501`

## 📁 Project Structure

# Project Structure

```text
FootySense/
├── 1. Data Collection and SQL/   
│   ├── fetch_teams.py           
│   ├── fetch_scorers.py         
│   ├── database.py             
│   └── analyze_data.py          
├── 2. Machine Learning Model/    
│   ├── epl_final.csv            
│   ├── prepare_ml_data.py      
│   └── train_model.py          
├── main.py                      
├── app.py                       
├── footysense.db                
├── model.pkl                    
└── requirements.txt             
```


## 📬 About the Developer
* **Syed Shahbaz JiLani**
  
*  **Majan University College (Oman)**

* **Degree: BSc (Hons) Software Engineering**

* **LinkedIn: https://linkedin.com/in/syed-shahbaz-jilani**

* **GitHub: https://github.com/Syed-Shahbaz27**


