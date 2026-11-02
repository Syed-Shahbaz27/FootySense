# This file is basically the frontend of our end-to-end ML system
# The Backend from main.py is connected to app.py

# First import the  streamlit library

import time
import requests
import streamlit as st

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="FootySense",
    page_icon="⚽",
    layout="centered"
)

# Your existing FastAPI backend on Render
API_URL = "https://footysense-api.onrender.com"

# Retry configuration
MAX_ATTEMPTS = 5
RETRY_DELAY = 2


# --------------------------------------------------
# 2. PAGE TITLE AND PROJECT INFORMATION
# --------------------------------------------------

st.title("📊⚽ FootySense: Match Predictor")

st.write(
    "Predict English Premier League match outcomes "
    "using Machine Learning."
)

with st.sidebar:
    st.header("Project Info")

    st.markdown("**Tech Stack**")
    st.code(
        "Python + Streamlit + FastAPI + SQLite + Scikit-Learn",
        language="text"
    )

    st.markdown("---")

    st.subheader("Built by Syed Shahbaz Jilani")
    st.subheader("Majan University College, Oman")

    st.markdown("---")

    st.header("How does this work?")

    st.write(
        "Select two teams to face off. FootySense uses "
        "historical performance statistics to estimate "
        "the probabilities of a home win, draw, or away win."
    )


# --------------------------------------------------
# 3. FETCH TEAMS FROM THE FASTAPI BACKEND
# --------------------------------------------------

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_teams():
    """
    Fetch the available teams from FastAPI.

    Retries failed requests, including HTTP 503 responses.
    Successfully retrieved team lists are cached for one hour.
    """

    last_error = None

    for attempt in range(MAX_ATTEMPTS):

        try:
            response = requests.get(
                f"{API_URL}/teams",
                timeout=8
            )

            # Convert HTTP errors such as 503 into exceptions
            response.raise_for_status()

            data = response.json()
            teams_data = data.get("teams", [])

            # Extract team names and remove duplicates
            teams = sorted({
                str(team[0]).strip()
                for team in teams_data
                if isinstance(team, (list, tuple))
                and len(team) > 0
                and team[0]
            })

            if teams:
                return teams

            raise ValueError("The backend returned an empty team list.")

        except (
            requests.RequestException,
            ValueError,
            TypeError,
            AttributeError
        ) as error:

            last_error = error

            # Wait before retrying, including after HTTP 503
            if attempt < MAX_ATTEMPTS - 1:
                time.sleep(RETRY_DELAY)

    # Raise an error instead of caching an unsuccessful response
    raise RuntimeError(
        "Could not retrieve teams from the prediction server."
    ) from last_error


# --------------------------------------------------
# 4. LOAD TEAMS
# --------------------------------------------------

with st.spinner("⏳ Connecting to the FootySense prediction engine..."):

    try:
        team_list = fetch_teams()

    except RuntimeError:

        st.error(
            "The prediction server is temporarily unavailable."
        )

        st.info(
            "Please wait a little and refresh the page. "
            "The server may be starting up."
        )

        st.stop()


# --------------------------------------------------
# 5. TEAM SELECTION
# --------------------------------------------------

st.markdown("### ⚽ Select Your Match")

col1, col2 = st.columns(2)

with col1:
    home_team = st.selectbox(
        "🏠 Home Team",
        team_list,
        index=0
    )

with col2:
    away_team = st.selectbox(
        "✈️ Away Team",
        team_list,
        index=1 if len(team_list) > 1 else 0
    )


# --------------------------------------------------
# 6. PREDICTION
# --------------------------------------------------

if st.button("🔮 Predict Winner", use_container_width=True):

    if home_team == away_team:

        st.warning("Please select two different teams.")

    else:

        payload = {
            "home_team": home_team,
            "away_team": away_team
        }

        with st.spinner("Analyzing historical statistics..."):

            try:

                # Send the prediction request to FastAPI
                response = requests.post(
                    f"{API_URL}/predict",
                    json=payload,
                    timeout=45
                )

                # Handle HTTP errors before reading the response
                response.raise_for_status()

                result = response.json()
                probabilities = result.get("probabilities")

                if not isinstance(probabilities, dict):
                    raise ValueError(
                        "Invalid prediction response."
                    )

                home_probability = probabilities.get("Home Win")
                draw_probability = probabilities.get("Draw")
                away_probability = probabilities.get("Away Win")

                if any(
                    value is None
                    for value in (
                        home_probability,
                        draw_probability,
                        away_probability
                    )
                ):
                    raise ValueError(
                        "The prediction response is missing probabilities."
                    )

                # Display prediction results
                st.markdown("### 📊 Outcome Probabilities")

                col_a, col_b, col_c = st.columns(3)

                with col_a:
                    st.metric(
                        f"🏠 {home_team}",
                        f"{home_probability}%"
                    )

                with col_b:
                    st.metric(
                        "🤝 Draw",
                        f"{draw_probability}%"
                    )

                with col_c:
                    st.metric(
                        f"✈️ {away_team}",
                        f"{away_probability}%"
                    )

            except requests.Timeout:

                st.error(
                    "The prediction server took too long to respond. "
                    "Please try again."
                )

            except requests.HTTPError as error:

                status_code = (
                    error.response.status_code
                    if error.response is not None
                    else "Unknown"
                )

                st.error(
                    f"The prediction server returned HTTP {status_code}. "
                    "Please try again shortly."
                )

            except requests.RequestException:

                st.error(
                    "Could not connect to the prediction server. "
                    "Please check again shortly."
                )

            except (ValueError, TypeError):

                st.error(
                    "The server returned an unexpected prediction response. "
                    "Please try again."
                )


# Use #python -m streamlit run app.py to the run the streamlit app
