import streamlit as st          # building the web dashboard
import pandas as pd             # data handling and analysis
import plotly.express as px     # interactive visualizations
import os                       # file and path operations

# CONFIGURATION
DATA_DIR = "data"       # Folder containing all CSV files

# Dictionary mapping each dashboard section to its CSV file path
CSV_FILES = {
    "Batting Best Averages": os.path.join(DATA_DIR, "batting_best_averages.csv"),
    "Batting Highest Innings": os.path.join(DATA_DIR, "batting_highest_innings.csv"),
    "Batting Top Tournament": os.path.join(DATA_DIR, "batting_top_tournament.csv"),
    "Bowling Top Wicket Takers": os.path.join(DATA_DIR, "bowling_top_wicket_takers.csv"),
}

# LOADING DATA ( Load all CSV files and cache the data for faster performance)
@st.cache_data
def load_data():
    data = {}
    for name, path in CSV_FILES.items():    # Loop through each file in the dictionary
        data[name] = pd.read_csv(path)      # Read CSV and store in dictionary
    return data

data = load_data()

# GLOBAL STYLING (CSS)
st.markdown("""
<style>
/* Sidebar hover effect */
section[data-testid="stSidebar"] .stRadio > label:hover {
    background-color: #f0f0f0;
    border-radius: 6px;
    cursor: pointer;
}

/* Background image */
.stApp {
    background: url("https://dnyuz.com/wp-content/uploads/2025/09/India-defeat-Pakistan-by-five-wickets-in-controversy-hit-Asia-Cup-1140x855.jpg");
    background-size: cover;
    background-attachment: fixed;
}

/* White box for readability only on dashboard pages */
.dashboard-box {
    background: rgba(255,255,255,0.85);
    border-radius: 12px;
    padding: 1.5rem;
}

/* =========================== */
/* Colorful Tabs Styling */
/* =========================== */
[data-baseweb="tab-list"] button {
    background-color: #1f77b4;  /* default tab color */
    color: white;
    font-weight: bold;
    border-radius: 10px 10px 0 0;
    margin-right: 5px;
    padding: 8px 15px;
}

[data-baseweb="tab-list"] button:hover {
    background-color: #ff7f0e;  /* hover color */
    color: white;
}

[data-baseweb="tab-list"] button[aria-selected="true"] {
    background-color: #2ca02c;  /* selected tab color */
    color: white;
}
</style>
""", unsafe_allow_html=True)


# SIDEBAR
st.sidebar.title("🏏 Asia Cup 2025 Dashboard")

# Add "Home" as first option
page = st.sidebar.radio(
    "Navigate",
    ["Home"] + list(CSV_FILES.keys())   # Combine "Home" with all dashboard sections
)

# Get all unique team names from batting and bowling data
teams = sorted(set(data["Batting Top Tournament"]["team"].unique()) |
               set(data["Bowling Top Wicket Takers"]["team"].unique()))
# Multi-select widget in sidebar to filter data by selected teams
team_filter = st.sidebar.multiselect("Filter by team", teams, default=teams)

# Home Page (display welcome message by default when we visit this application)
if page == "Home":
    st.markdown(
        """
        <div style="text-align: center; padding: 80px; background: rgba(0,0,0,0.5); border-radius: 35px;">
            <h1 style="color: #FA6005; font-size: 65px;">🏆 Asia Cup 2025</h1>
            <h2 style="color: #05FAFA;">Welcome to Statistics Dashboard</h2>
            <p style="color: orange; font-size: 20px;">Explore batting and bowling performances, top scorers, wicket takers, and more!</p>
        </div>
        """,
        unsafe_allow_html=True      # allowing custom HTML for styling
    )

# Dashboard Pages
elif page == "Batting Best Averages":
    df = data[page].copy()  # copy relevant dataset
    df = df[df["team"].isin(team_filter)] # filter data by selected teams
    with st.container():        #create container for layout

        st.markdown("<h1 style='color: red;'>Batting Best Averages</h1>", unsafe_allow_html=True)

        col1, col2 = st.columns([2,1]) # split layout into two columns in the ratio of 2:1 (bar chart larger, pie chart smaller)
        with col1:   # col1 = bar chart data
            fig = px.bar(df, x="player", y="average", color="team",
                         title="Best Batting Averages", text="average")
            st.plotly_chart(fig, use_container_width=True)
        with col2:   # col2 = pie chart
            pie = px.pie(df, names="player", values="average", color="team",
                         title="Share of Averages")
            st.plotly_chart(pie, use_container_width=True)

        st.dataframe(df)    #display raw data table
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Batting Highest Innings":
    df = data[page].copy()
    df["score_int"] = df["score"].astype(str).str.replace("*", "", regex=False).astype(int)
    df = df[df["team"].isin(team_filter)]
    with st.container():

        st.markdown("<h1 style='color: red;'>Highest Individual Innings</h1>", unsafe_allow_html=True)

        fig = px.bar(df, x="player", y="score_int", color="team",
                     title="Top Individual Scores", text="score")
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(df)
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Batting Top Tournament":
    df = data[page].copy()
    df = df[df["team"].isin(team_filter)]
    with st.container():

        st.markdown("<h1 style='color: red;'>Top Run Scorers (Tournament)</h1>", unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["Bar Chart", "Scatter Plot", "Pie Chart"])
        with tab1:
            fig1 = px.bar(df.sort_values("runs", ascending=False), x="player", y="runs",
                          color="team", title="Total Runs")
            st.plotly_chart(fig1, use_container_width=True)
        with tab2:
            fig2 = px.scatter(df, x="strike_rate", y="average", size="runs", color="team",
                              hover_name="player",
                              title="Average vs Strike Rate (Bubble = Runs)")
            st.plotly_chart(fig2, use_container_width=True)
        with tab3:
            pie = px.pie(df, names="player", values="runs", color="team",
                         title="Runs Contribution per Player")
            st.plotly_chart(pie, use_container_width=True)

        st.dataframe(df)
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Bowling Top Wicket Takers":
    df = data[page].copy()
    df = df[df["team"].isin(team_filter)]
    with st.container():

        st.markdown("<h1 style='color: red;'>Top Wicket Takers</h1>", unsafe_allow_html=True)


        tab1, tab2, tab3 = st.tabs(["Most Wickets", "Avg vs Economy", "Pie Chart"])
        with tab1:
            fig1 = px.bar(df.sort_values("wickets", ascending=False), x="player", y="wickets",
                          color="team", title="Most Wickets")
            st.plotly_chart(fig1, use_container_width=True)
        with tab2:
            fig2 = px.scatter(df, x="economy", y="average", size="wickets", color="team",
                              hover_name="player",
                              title="Bowling Average vs Economy (Bubble = Wickets)")
            st.plotly_chart(fig2, use_container_width=True)
        with tab3:
            pie = px.pie(df, names="player", values="wickets", color="team",
                         title="Wickets Share per Player")
            st.plotly_chart(pie, use_container_width=True)

        st.dataframe(df)
        st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.sidebar.markdown("---")
st.sidebar.info("""
🏏 **Asia Cup 2025 Dashboard**  
Created with the following technologies:

- **Streamlit**: Interactive web app framework for Python  
- **Pandas**: Data manipulation and analysis  
- **Plotly / Plotly Express**: Interactive charts and graphs  
- **CSS / HTML**: Custom styling for background, tabs, and hover effects  
""")
