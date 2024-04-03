import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt

import get_NBA_data as NBA
import draw_chart

# Streamlit app
st.set_page_config(page_title="NBA Analytics", layout="wide", initial_sidebar_state="expanded")
st.title('NBA Player Shooting Map :basketball:')

# Set up Streamlit sidebar
with st.sidebar:
    # Image
    st.image("assets/images_5.png")

    st.toast(f'Getting Players List !:page_facing_up:')
    # Get all NBA players Names
    players_dict = NBA.get_players_names()

    # Player selection
    selected_player = st.selectbox('Select a player :man-bouncing-ball:', list(players_dict.keys()), index=None)

    if selected_player != None:
        st.toast(f'Getting Seasons Played !:calendar:')
        # Get player ID
        player_id = players_dict[selected_player]

        # Get seasons for the selected player
        player_seasons = NBA.get_player_seasons(player_id)

        # Season selection
        selected_season = st.selectbox('Select a season :spiral_calendar_pad:', player_seasons, index=None)

if "selected_season" in locals() and selected_season != None:
    st.toast(f'Getting Player Data !:card_file_box:')
    # Get player shooting details
    player_shotchart_df, league_avg = NBA.get_player_shotchartdetail(selected_player, selected_season)



col1, col2 = st.columns([0.3, 0.7])
with col1:
    st.header("Player Stats")

    if selected_player != None and selected_season != None:
        st.text(f'{selected_player} {selected_season} season stats')
        career_stats = NBA.get_seasons_stats(player_id)
        idx = career_stats.index[career_stats['SEASON_ID'] == selected_season].tolist()
        print(idx)

        GP = career_stats[career_stats['SEASON_ID'] == selected_season]['GP']
        if idx[0] == 0:
            GP_Diff = 0
        else:
            GP_prev = career_stats.loc[idx[0]-1]['GP']
            GP_Diff = (GP.iloc[0] - GP_prev).item()
        print(GP_Diff)
        print(GP)
        st.metric(label="Games Played", value=GP.iloc[0], delta=GP_Diff)

        PPG = round(career_stats[career_stats['SEASON_ID'] == selected_season]['PTS']/GP, 1)
        if idx[0] == 0:
            PPG_Diff = 0
        else:
            PPG_prev = career_stats.loc[idx[0]-1]['PTS']/GP_prev
            PPG_Diff = round((PPG.iloc[0] - PPG_prev).item(), 1)
        st.metric(label="Points per Game", value=PPG, delta=PPG_Diff)

        APG = round(career_stats[career_stats['SEASON_ID'] == selected_season]['AST']/GP, 1)
        if idx[0] == 0:
            APG_Diff = 0
        else:
            APG_prev = career_stats.loc[idx[0]-1]['AST']/GP_prev
            APG_Diff = round((APG.iloc[0] - APG_prev).item(), 1)
        st.metric(label="Assits per Game", value=APG, delta=APG_Diff)

        RPG = round(career_stats[career_stats['SEASON_ID'] == selected_season]['REB']/GP, 1)
        if idx[0] == 0:
            RPG_Diff = 0
        else:
            RPG_prev = career_stats.loc[idx[0]-1]['REB']/GP_prev
            RPG_Diff = round((RPG.iloc[0] - RPG_prev).item(), 1)
        st.metric(label="Rebounds per Game", value=RPG, delta=RPG_Diff)

        SPG = round(career_stats[career_stats['SEASON_ID'] == selected_season]['STL'] / GP, 1)
        if idx[0] == 0:
            SPG_Diff = 0
        else:
            SPG_prev = career_stats.loc[idx[0] - 1]['STL'] / GP_prev
            SPG_Diff = round((SPG.iloc[0] - SPG_prev).item(), 1)
        st.metric(label="Steals per Game", value=SPG, delta=SPG_Diff)

with col2:
    st.header("Shooting Maps")
    # Chart type choice
    chart_choice = st.radio("Chart Choice :bar_chart:", ["Shot Chart", "Hex Map", "Shot Zone", "HeatMap"], index=None, horizontal=True)

    # Placeholder for the figure
    fig_placeholder = st.empty()
    ''
    # Initialize figure variables
    fig_shot_chart = None
    fig_hex_map = None
    fig_shot_zone = None
    fig_heat_Map = None
    # Display the selected figure
    if chart_choice == "Shot Chart":
        st.toast(f'Plotting Started !:bar_chart:')

        # Draw shooting map
        fig_shot_chart = plt.figure(figsize=(12, 11))
        draw_chart.shot_chart(player_shotchart_df, title=f"{selected_player} Shot Chart of {selected_season} season")

        fig_placeholder.pyplot(fig_shot_chart)
    elif chart_choice == "Hex Map":
        st.toast(f'Plotting Started !:bar_chart:')

        # Draw hex map
        fig_hex_map = plt.figure(figsize=(12, 11))
        draw_chart.hexmap_chart(player_shotchart_df, league_avg, title=f"{selected_player} Hex Map of {selected_season} season")

        fig_placeholder.pyplot(fig_hex_map)
    elif chart_choice == "Shot Zone":
        st.toast(f'Plotting Started !:bar_chart:')

        # Draw shot zone
        fig_shot_zone = plt.figure(figsize=(12, 11))
        draw_chart.shot_zones(player_shotchart_df, league_avg, title=f"{selected_player} Shot Zone Map of {selected_season} season")

        fig_placeholder.pyplot(fig_shot_zone)
    elif chart_choice == "HeatMap":
        st.toast(f'Plotting Started !:bar_chart:')

        # Draw HeatMap
        fig_heat_Map = plt.figure(figsize=(12, 11))
        draw_chart.heatmap(player_shotchart_df, title=f"{selected_player} HeatMap of {selected_season} season")

        fig_placeholder.pyplot(fig_heat_Map)