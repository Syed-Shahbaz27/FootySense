# 📊⚽ FootySense: Premier League Match Predictor

Football has been one of my primary interests growing up, I've loved watching live premier league matches, I've also played in Oman at an academy level. With this in mind, I built FootySense.

A full-stack Machine Learning application that leverages historical data to predict the outcomes of English Premier League matches.

## 🌟 Highlights
* **End-to-End ML Pipeline:** Built a complete system from raw API data ingestion to a functional web interface.
* **Real-World Data:** Trained on a dataset of over 9,000 historical Premier League matches.
* **Production-Ready Backend:** Developed a FastAPI backend to serve predictions with high performance.
* **Logic-Driven:** Addressed "Data Leakage" by ensuring the model only uses information available *before* kickoff.

## 🚀 Live Demo
[Click here to view the live app](https://footysense-app.onrender.com/)

## 📸 Preview 

**<img width="1901" height="839" alt="Screenshot 2026-05-02 025812" src="https://github.com/user-attachments/assets/1bd99889-3e58-4d5e-b53b-e3236a53fd78" />**


## 🧠 The Problem vs. The Solution
### The Problem
Football prediction is notably difficult due to the high variance of the sport. Many sports-based ML models suffer from **Data Leakage** (using end-of-game stats like "Goals Scored at Full Time Home / Away" to predict the "Result"), which leads to artificially high accuracy (99%) that fails in real-world use cases.

### The Solution
FootySense uses a **Random Forest Classifier** trained on pre-match features. It calculates historical averages of shots, shots on target, and corners. The API calculates team averages at inference time so users simply select two teams and receive a realistic prediction for 3 outcomes as stated: a Home Win, Away Win, or Draw.

## 🛠️ Tech Stack
| Category | Technology |
| :--- | :--- |
| **Language** | Python |
| **Backend** | FastAPI, Uvicorn |
| **Database** | SQLite |
| **ML Model** | Scikit-Learn (Random Forest) |
| **Frontend** | Streamlit |
| **Data Handling** | Pandas, Requests |
| **Deployment** | Render, Github |

## 📊 Model Performance
* **Accuracy:** ~52%  
* **Context:** While it might seem low, industry standards for sports betting and prediction models typically range between 50-60%.
* **Features**: HomeShots, AwayShots, ShotsOnTarget, Corners
* **Data Source:** Live data via the [Football-Data.org](https://www.football-data.org/) API and historical Kaggle datasets.

## ⚙️ Engineering Decisions/ Fixes I did

**Data Leakage Fix:** Initial model showed 99% accuracy using 
post-match statistics. Identified and removed target-correlated 
features, correcting accuracy to a realistic 52%.

**Inference-Time Feature Calculation:** Users select team names 
only. API calculates historical averages at request time  no 
in-game stats required from the user.

**Team Name Normalization:** Built TEAM_NAME_MAP dictionary to 
bridge naming mismatch between live API responses and Kaggle 
historical dataset, resolving silent prediction failures.

**Keep-Alive Architecture:** Implemented cron-job.org pings 
every 10 minutes to bypass Render free tier inactivity limits.


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

* **LinkedIn: https://www.linkedin.com/in/syed-shahbaz-jilani-816052253/**

* **GitHub: https://github.com/Syed-Shahbaz27**

Contact me on LinkedIn, to let me know what more you want to see in Footysense, Gradually more updates will be added later. 

