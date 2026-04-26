# 📊⚽ FootySense: Premier League Match Predictor

A full-stack Machine Learning application that leverages historical data to predict the outcomes of English Premier League matches.

## 🌟 Highlights
* **End-to-End ML Pipeline:** Built a complete system from raw API data ingestion to a functional web interface.
* **Real-World Data:** Trained on a dataset of over 9,000 historical Premier League matches.
* **Production-Ready Backend:** Developed a FastAPI backend to serve predictions with high performance.
* **Logic-Driven:** Addressed "Data Leakage" by ensuring the model only uses information available *before* kickoff.

## 🚀 Live Demo
[Click here to view the live app](LINK_WILL_BE_ADDED_AFTER_DEPLOYMENT)

## 🧠 The Problem vs. The Solution
### The Problem
Football prediction is notoriously difficult due to the high variance of the sport. Many entry-level models suffer from **Data Leakage** (using end-of-game stats like "Total Yellow Cards" to predict the "Result"), which leads to artificially high accuracy that fails in real-world scenarios.

### The Solution
FootySense uses a **Random Forest Classifier** trained on pre-match features. The system calculates rolling averages for key metrics—such as **Shots on Target** and **Corners**—to provide realistic probability distributions for a Home Win, Away Win, or Draw.

## 🛠️ Tech Stack
| Category | Technology |
| :--- | :--- |
| **Language** | Python |
| **Backend** | FastAPI, Uvicorn |
| **Database** | SQLite3 |
| **ML Model** | Scikit-Learn (Random Forest) |
| **Frontend** | Streamlit |
| **Data Handling** | Pandas, Requests |
| **Deployment** | Render / GitHub |

## 📊 Model Performance
* **Accuracy:** ~52% - 56% 
* **Context:** While it might seem low, industry standards for sports betting and prediction models typically hover between 50-60%.
* **Data Source:** Live data via the [Football-Data.org](https://www.football-data.org/) API and historical Kaggle datasets.

## ⚙️ Installation & Running Locally

### 1. Clone the repo
```bash
git clone [https://github.com/Syed-Shahbaz27/FootySense.git](https://github.com/Syed-Shahbaz27/FootySense.git)
cd FootySense
