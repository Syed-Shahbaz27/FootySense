📊⚽ FootySense: Premier League Match Predictor
A full-stack Machine Learning application that predicts the outcome of Premier League football matches.

🌟 Highlights
End-to-End ML: From raw API data to a deployed web application.
Real Data: Trained on 9,380 historical Premier League matches.
Live API: FastAPI backend serving predictions to a Streamlit frontend.
Problem Solving: Solved "Data Leakage" issues to ensure model validity.

🚀 Live Demo
Click here to view the live app (Link will be added after deployment)

🧠 The Problem vs. The Solution
The Problem:Football match prediction is notoriously difficult due to the unpredictable nature of the sport. Many models suffer from "Data Leakage" (using future data to predict the past), leading to fake high accuracy.

The Solution:FootySense uses a Random Forest model trained only on data available before a match starts. By calculating rolling averages of team stats (Shots, Corners), it provides a realistic prediction probability (Win/Draw/Loss) rather than a guaranteed outcome.

🛠️ Tech Stack
Language: Python
Backend: FastAPI, Uvicorn
Database: SQLite
ML Model: Scikit-Learn (Random Forest)
Frontend: Streamlit
Deployment: Render
📊 Model Performance
Accuracy: ~52% (Realistic for football prediction. Industry standard is 50-60%).
Data Source: Football-Data.org API.
⚙️ Installation & Running Locally
Clone the repo
git clone https://github.com/Syed-Shahbaz27/FootySense.gitcd FootySense
Install dependencies
pip install -r requirements.txt
Set up Environment VariablesCreate a .env file and add your API key:FOOTBALL_API_KEY=your_key_here
Run the Backend
uvicorn main:app --reload
Run the Frontend (in a new terminal)
streamlit run app.py
📬 Author
Syed Shahbaz Jilani

University: Majan University College, Oman
LinkedIn: linkedin.com/in/syed-shahbaz-jilani
GitHub: github.com/Syed-Shahbaz27
