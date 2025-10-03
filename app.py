import streamlit as st
import pandas as pd
import plotly.express as px
import os

DATA_DIR = "data"

CSV_FILES = {
    "Batting Best Averages": os.path.join(DATA_DIR, "batting_best_averages.csv"),
    "Batting Highest Innings": os.path.join(DATA_DIR, "batting_highest_innings.csv"),
    "Batting Top Tournament": os.path.join(DATA_DIR, "batting_top_tournament.csv"),
    "Bowling Top Wicket Takers": os.path.join(DATA_DIR, "bowling_top_wicket_takers.csv"),
}

@st.cache_data
def load_data():
    data = {}
    for name, path in CSV_FILES.items():
        data[name] = pd.read_csv(path)
    return data

data = load_data()

st.sidebar.title("🏏 Asia Cup 2025 Dashboard")

page = st.sidebar.radio(
    "Navigate",
    list(CSV_FILES.keys())
)

teams = sorted(set(data["Batting Top Tournament"]["team"].unique()) |
               set(data["Bowling Top Wicket Takers"]["team"].unique()))
team_filter = st.sidebar.multiselect("Filter by team", teams, default=teams)

if page == "Batting Best Averages":
    df = data[page].copy()
    df = df[df["team"].isin(team_filter)]

    st.header("Batting Best Averages")
    fig = px.bar(df, x="player", y="average", color="team", title="Best Batting Averages")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df)

elif page == "Batting Highest Innings":
    df = data[page].copy()
    df["score_int"] = df["score"].astype(str).str.replace("*", "", regex=False).astype(int)
    df = df[df["team"].isin(team_filter)]

    st.header("Highest Individual Innings")
    fig = px.bar(df, x="player", y="score_int", color="team", title="Top Individual Scores")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df)

elif page == "Batting Top Tournament":
    df = data[page].copy()
    df = df[df["team"].isin(team_filter)]

    st.header("Top Run Scorers (Tournament)")
    fig = px.bar(df.sort_values("runs", ascending=False), x="player", y="runs",
                 color="team", title="Total Runs in Tournament")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df)

elif page == "Bowling Top Wicket Takers":
    df = data[page].copy()
    df = df[df["team"].isin(team_filter)]

    st.header("Top Wicket Takers")
    fig = px.bar(df.sort_values("wickets", ascending=False), x="player", y="wickets",
                 color="team", title="Most Wickets")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df)

st.sidebar.markdown("---")
st.sidebar.info("""
Asia Cup 2025 Dashboard built with:
- Streamlit
- Pandas
- Plotly
""")
