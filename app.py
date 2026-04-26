# This file is basically the frontend of our end-to-end ML system
# The Backend from main.py is connected to app.py

# First import the  streamlit library
import streamlit as st
import requests
st.set_page_config(page_title="FootySense", page_icon="⚽📊")
API_URL = "http://127.0.0.1:8000"
# Title
st.title(":green[📊⚽ FootySense: Match Predictor]")
st.write("Predict outcomes of premier league matches using  Machine Learning")

# Sidebar Info
with st.sidebar:
  st.header("Project Info")
  st.markdown("Tech Stack")
  st.code("FastAPI + SQLite + Scikit-Learn", language="python")
  st.markdown("---")
  st.subheader("Built by Syed Shahbaz Jilani")
  st.subheader("Majan University College, Oman")
  st.markdown("---")
  st.header("How does this work?")
  st.subheader("Select two teams to face off. The model analyzes their historical performance (shots, corners, form) to predict the match outcome probabilities.")


#1. Now we will fetch teams from backend
try:
  response = requests.get(f"{API_URL}/teams")
  teams_data = response.json()['teams']
  # Extract names (assuming format [('Arsenal,'), ('Chelsea',)])
  team_list = sorted([team[0] for team in teams_data])
except Exception as e:
  # Fallback if API isn't running
  st.error("Could not connect to backend. Is FastAPI running?")
  st.stop()

#2. User Input (Dropdowns)
col1,col2 = st.columns(2)

with col1:
  home_team = st.selectbox("🏠 Home Team", team_list)

with col2:
  away_team = st.selectbox("✈️ Away Team", team_list)

#3. Predict Button
if st.button (":yellow[Predict Winner]"):
  if home_team == away_team:
    st.warning("Please choose different teams.")
  else:
    with st.spinner("Analyzing stats and predicting result....📶🔮"):
      try:
        #Call FastAPI
        payload = {"home_team":home_team,"away_team": away_team}
        res = requests.post(f"{API_URL}/predict", json=payload)
        result = res.json() 
        probs = result['probabilities']
        st.markdown("### 🎲 Outcome Probabilities")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
          st.metric(f"🏠 {home_team}", f"{probs.get('H', 0)}%")
        with col_b:
          st.metric("🤝 Draw", f"{probs.get('D', 0)}%")
        with col_c:
          st.metric(f"✈️ {away_team}", f"{probs.get('A', 0)}%")
      except Exception as e:
       st.error("Error in connecting to the server, pls try again later.")

# Use #python -m streamlit run app.py to the run the streamlit app

      
      
