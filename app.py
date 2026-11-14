
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="RR SuperR Selector",
    page_icon="🏏",
    layout="wide"
)

BASE = os.path.dirname(__file__)

batters = pd.read_csv(os.path.join(BASE, "batters.csv"))
bowlers = pd.read_csv(os.path.join(BASE, "bowlers.csv"))
teams = pd.read_csv(os.path.join(BASE, "team_audit.csv"))

st.title("🏏 Rajasthan Royals | SuperR Selector")
st.subheader("Season 2 — Round 1")
st.caption("Identifying the most reliable players under pressure | IPL 2022–2026 + T20Is 2022–2026")

# Overview
st.header("📊 Tournament Overview")

c1, c2, c3 = st.columns(3)
c1.metric("Matches Analysed", "815")
c2.metric("High-Pressure Deliveries", "14,028")
c3.metric("Chase Deliveries Analysed", "91,934")

st.info(
    "Pressure is evaluated during second-innings chases using "
    "required run rate, wickets remaining and match stage."
)

# Sidebar
st.sidebar.title("Dashboard Navigation")
section = st.sidebar.radio(
    "Choose Section",
    ["Overview", "Batter Rankings", "Bowler Rankings",
     "Player Comparison", "IPL 2026 Team Audit"]
)

if section == "Overview":
    st.header("🏆 Top Performers")

    left, right = st.columns(2)

    with left:
        st.subheader("Top 5 Batters")
        st.dataframe(
            batters[["final_rank", "player_name", "runs_pressure",
                     "strike_rate_pressure", "final_score"]].head(5),
            hide_index=True,
            use_container_width=True
        )

    with right:
        st.subheader("Top 5 Bowlers")
        st.dataframe(
            bowlers[["final_rank", "player_name", "wickets_pressure",
                     "legal_balls_pressure", "final_score"]].head(5),
            hide_index=True,
            use_container_width=True
        )

elif section == "Batter Rankings":
    st.header("🏏 Batter Rankings")

    st.dataframe(
        batters[["final_rank", "player_name", "runs_pressure",
                 "balls_faced_pressure", "strike_rate_pressure",
                 "strike_rate_difference", "pressure_matches",
                 "final_score"]],
        hide_index=True,
        use_container_width=True
    )

    fig = px.bar(
        batters.sort_values("final_score", ascending=True),
        x="final_score",
        y="player_name",
        orientation="h",
        color="final_score",
        title="Top 10 Batters — Pressure Score",
        labels={"final_score": "Final Score", "player_name": "Player"}
    )
    st.plotly_chart(fig, use_container_width=True)

elif section == "Bowler Rankings":
    st.header("🎯 Bowler Rankings")

    st.dataframe(
        bowlers[["final_rank", "player_name", "legal_balls_pressure",
                 "wickets_pressure", "pressure_matches", "final_score"]],
        hide_index=True,
        use_container_width=True
    )

    fig = px.bar(
        bowlers.sort_values("final_score", ascending=True),
        x="final_score",
        y="player_name",
        orientation="h",
        color="final_score",
        title="Top 10 Bowlers — Pressure Score",
        labels={"final_score": "Final Score", "player_name": "Player"}
    )
    st.plotly_chart(fig, use_container_width=True)

elif section == "Player Comparison":
    st.header("⚖️ Player Comparison")

    player_type = st.radio("Select Player Type", ["Batters", "Bowlers"],
                           horizontal=True)

    if player_type == "Batters":
        names = batters["player_name"].tolist()
        selected = st.multiselect("Choose batters to compare", names,
                                  default=names[:2])
        data = batters[batters["player_name"].isin(selected)]

        if not data.empty:
            st.dataframe(data, hide_index=True, use_container_width=True)
            fig = px.bar(data, x="player_name", y="strike_rate_pressure",
                         color="final_score",
                         title="Pressure Strike Rate Comparison")
            st.plotly_chart(fig, use_container_width=True)

    else:
        names = bowlers["player_name"].tolist()
        selected = st.multiselect("Choose bowlers to compare", names,
                                  default=names[:2])
        data = bowlers[bowlers["player_name"].isin(selected)]

        if not data.empty:
            st.dataframe(data, hide_index=True, use_container_width=True)
            fig = px.bar(data, x="player_name", y="wickets_pressure",
                         color="final_score",
                         title="Pressure Wickets Comparison")
            st.plotly_chart(fig, use_container_width=True)

elif section == "IPL 2026 Team Audit":
    st.header("🔍 IPL 2026 Team Audit")
    st.caption("Historical team mapping from the 2026 dataset; this does not confirm IPL 2027 auction availability.")

    st.dataframe(teams, hide_index=True, use_container_width=True)

    search = st.text_input("Search player")
    if search:
        result = teams[
            teams["player_name"].str.contains(search, case=False, na=False)
        ]
        st.dataframe(result, hide_index=True, use_container_width=True)

st.divider()
st.caption("Analysis: IPL 2022–2026 and T20Is 2022–2026 | Candidate rankings are data-driven, not confirmed auction availability.")
