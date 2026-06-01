# This file is basically the frontend of our end-to-end ML system
# The Backend from main.py is connected to app.py

# First import the  streamlit library
import streamlit as st
import time
import requests
time.sleep(1)  # wait 1 second to avoid rate limiting
st.set_page_config(page_title="FootySense", page_icon="⚽📊")
API_URL = "https://footysense-api.onrender.com"
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

# 1. Now we will fetch teams from backend (WITH COLD-START RETRY LOGIC)
team_list = []
with st.spinner("⏳ Waking up the prediction engine... Please wait up to 45 seconds for the free server."):
    for attempt in range(5):  # Try 5 times (50 seconds total buffer)
        try:
            # We add a 10-second timeout so it doesn't hang infinitely
            response = requests.get(f"{API_URL}/teams", timeout=10)
            if response.status_code == 200:
                teams_data = response.json()['teams']
                # Extract names (assuming format [('Arsenal,'), ('Chelsea',)])
                team_list = sorted([team[0] for team in teams_data])
                break  # Success! We got the data, exit the loop.
        except Exception:
            time.sleep(10)  # Wait 10 seconds before trying again

# Fallback if API completely fails after 50 seconds
if not team_list:
    st.error("Could not connect to backend. Is FastAPI running? Please refresh the page.")
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
        # 3. Predict Button (Inside the try block)
        result = res.json() 
        probs = result['probabilities']
        
        st.markdown("### 🎲 Outcome Probabilities")
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
          # We change 'H' to 'Home Win' to match the backend!
          st.metric(f"🏠 {home_team}", f"{probs.get('Home Win', 0)}%")
        
        with col_b:
          # We change 'D' to 'Draw'
          st.metric("🤝 Draw", f"{probs.get('Draw', 0)}%")
        
        with col_c:
          # We change 'A' to 'Away Win'
          st.metric(f"✈️ {away_team}", f"{probs.get('Away Win', 0)}%")
      except Exception as e:
        st.error("Error in connecting to the server, pls try again later.")

# Use #python -m streamlit run app.py to the run the streamlit app