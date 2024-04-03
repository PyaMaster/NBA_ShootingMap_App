import pandas as pd
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.grid import grid
from streamlit_modal import Modal
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

    st.info("this web app aim to provide an interactive and visually appealing way for users to explore NBA player statistics and shooting performance for different seasons.")

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

    modal = Modal(key="About Key", title="About this WebApp :question:")
    about_app = st.button(label="About this WebApp :question:")
    if about_app:
        with modal.container():
            st.markdown("""
🏀 This web app offers users an engaging and visually immersive experience, empowering them to delve into the intricacies of NBA player statistics and shooting performance across various seasons. Through a user-friendly interface, individuals can effortlessly navigate through an extensive database of player data, selecting their preferred NBA player and specific seasons of interest.

📊 With intuitive controls, users can access comprehensive statistics, including points per game, field goal percentage, and three-point percentage, meticulously curated for each player and season. These statistics serve as valuable insights into a player's performance and skill development over time, facilitating informed analysis and comparison.

🎯 Moreover, the web app goes beyond traditional statistical presentation by integrating dynamic visualizations of shooting maps. Utilizing innovative visualization techniques such as shot charts, hex maps, shot zones, and heatmaps, users gain deeper insights into a player's shooting tendencies, hotspots, and efficiency across the court.

🖥️ The interactive nature of the web app allows users to interactively explore and manipulate the data, enabling them to customize their analysis according to their preferences. Whether scrutinizing individual player performance or comparing multiple players across different seasons, the app provides a versatile platform for in-depth exploration and discovery.

🌟 Overall, the web app combines user-friendly design, rich statistical content, and captivating visualizations to offer basketball enthusiasts, analysts, and fans alike an immersive journey into the world of NBA player statistics and shooting performance.
""")

if "selected_season" in locals() and selected_season != None:
    st.toast(f'Getting Player Data !:card_file_box:')
    # Get player shooting details
    player_shotchart_df, league_avg = NBA.get_player_shotchartdetail(selected_player, selected_season)



col1, col2 = st.columns([0.3, 0.7])
with col1:
    #st.header("Player Stats")
    colored_header(label="Player Stats :1234:", color_name="orange-70", description="Player statistics presentation, comparing current season with last season's performance")

    if selected_player != None and selected_season != None:
        col1_grid = grid(1, 2, 2, 2, 2, 2, 2, vertical_align="bottom")

        col1_grid.markdown(f'<span style="font-size:larger"><span style="color:orange; font-weight:bold">{selected_player}</span> NBA <span style="font-weight:bold">{selected_season}</span> season statistics</span>', unsafe_allow_html=True)
        career_stats = NBA.get_seasons_stats(player_id)
        idx = career_stats.index[career_stats['SEASON_ID'] == selected_season].tolist()
        print(idx)

        #stat_line = col1_grid.button("Statline", use_container_width=True, disabled=True)
        #shooting_stats = col1_grid.button("Shooting Stats", use_container_width=True, disabled=True)

        col1_grid.subheader("Statline")
        col1_grid.subheader("Shooting Stats")

        GP = career_stats[career_stats['SEASON_ID'] == selected_season]['GP']
        if idx[0] == 0:
            GP_Diff = 0
        else:
            GP_prev = career_stats.loc[idx[0]-1]['GP']
            GP_Diff = (GP.iloc[0] - GP_prev).item()
        print(GP_Diff)
        print(GP)
        col1_grid.metric(label="Games Played", value=GP.iloc[0], delta=GP_Diff)

        FGA = round(career_stats[career_stats['SEASON_ID'] == selected_season]['FGA']/GP, 1)
        if idx[0] == 0:
            FGA_Diff = 0
        else:
            FGA_prev = career_stats.loc[idx[0]-1]['FGA']/GP_prev
            FGA_Diff = round((FGA.iloc[0] - FGA_prev).item(), 1)
        col1_grid.metric(label="Field Goals Attempted per Game", value=FGA.iloc[0], delta=FGA_Diff)

        PPG = round(career_stats[career_stats['SEASON_ID'] == selected_season]['PTS']/GP, 1)
        if idx[0] == 0:
            PPG_Diff = 0
        else:
            PPG_prev = career_stats.loc[idx[0]-1]['PTS']/GP_prev
            PPG_Diff = round((PPG.iloc[0] - PPG_prev).item(), 1)
        col1_grid.metric(label="Points per Game", value=PPG, delta=PPG_Diff)

        FGP = round(career_stats[career_stats['SEASON_ID'] == selected_season]['FG_PCT']*100, 1)
        if idx[0] == 0:
            FGP_Diff = 0
        else:
            FGP_prev = career_stats.loc[idx[0]-1]['FG_PCT']*100
            FGP_Diff = round((FGP.iloc[0] - FGP_prev).item(), 1)
        col1_grid.metric(label="Field Goals Percentage", value=f'{FGP.iloc[0]} %', delta=FGP_Diff)

        APG = round(career_stats[career_stats['SEASON_ID'] == selected_season]['AST']/GP, 1)
        if idx[0] == 0:
            APG_Diff = 0
        else:
            APG_prev = career_stats.loc[idx[0]-1]['AST']/GP_prev
            APG_Diff = round((APG.iloc[0] - APG_prev).item(), 1)
        col1_grid.metric(label="Assits per Game", value=APG, delta=APG_Diff)

        FG3A = round(career_stats[career_stats['SEASON_ID'] == selected_season]['FG3A'] / GP, 1)
        if idx[0] == 0:
            FG3A_Diff = 0
        else:
            FG3A_prev = career_stats.loc[idx[0] - 1]['FG3A'] / GP_prev
            FG3A_Diff = round((FG3A.iloc[0] - FG3A_prev).item(), 1)
        col1_grid.metric(label="3 Points Attempted per Game", value=FG3A.iloc[0], delta=FG3A_Diff)

        RPG = round(career_stats[career_stats['SEASON_ID'] == selected_season]['REB']/GP, 1)
        if idx[0] == 0:
            RPG_Diff = 0
        else:
            RPG_prev = career_stats.loc[idx[0]-1]['REB']/GP_prev
            RPG_Diff = round((RPG.iloc[0] - RPG_prev).item(), 1)
        col1_grid.metric(label="Rebounds per Game", value=RPG, delta=RPG_Diff)

        FG3_PCT = round(career_stats[career_stats['SEASON_ID'] == selected_season]['FG3_PCT'] * 100, 1)
        if idx[0] == 0:
            FG3_PCT_Diff = 0
        else:
            FG3_PCT_prev = career_stats.loc[idx[0] - 1]['FG3_PCT'] * 100
            FG3_PCT_Diff = round((FG3_PCT.iloc[0] - FG3_PCT_prev).item(), 1)
        col1_grid.metric(label="3 Points Percentage", value=f'{FG3_PCT.iloc[0]} %', delta=FG3_PCT_Diff)

        SPG = round(career_stats[career_stats['SEASON_ID'] == selected_season]['STL'] / GP, 1)
        if idx[0] == 0:
            SPG_Diff = 0
        else:
            SPG_prev = career_stats.loc[idx[0] - 1]['STL'] / GP_prev
            SPG_Diff = round((SPG.iloc[0] - SPG_prev).item(), 1)
        col1_grid.metric(label="Steals per Game", value=SPG, delta=SPG_Diff)

        FT_PCT = round(career_stats[career_stats['SEASON_ID'] == selected_season]['FT_PCT'] * 100, 1)
        if idx[0] == 0:
            FT_PCT_Diff = 0
        else:
            FT_PCT_prev = career_stats.loc[idx[0] - 1]['FT_PCT'] * 100
            FT_PCT_Diff = round((FT_PCT.iloc[0] - FT_PCT_prev).item(), 1)
        col1_grid.metric(label="Free Throw Percentage", value=f'{FT_PCT.iloc[0]} %', delta=FT_PCT_Diff)

        style_metric_cards()

with col2:
    #st.header("Shooting Maps")
    colored_header(label="Shooting Maps :world_map:", color_name="orange-70", description="Choose the desired shooting map to visualize among the four options provided")
    col2_grid = grid(4, 1, vertical_align="bottom")

    shot_chart = col2_grid.button("Shot Chart", use_container_width=True)
    hex_map = col2_grid.button("Hex Map", use_container_width=True)
    shot_zone = col2_grid.button("Shot Zone", use_container_width=True)
    heatmap = col2_grid.button("HeatMap", use_container_width=True)

    # Chart type choice
    #chart_choice = col2_grid.radio("Chart Choice :bar_chart:", ["Shot Chart", "Hex Map", "Shot Zone", "HeatMap"], index=None, horizontal=True)

    # Placeholder for the figure
    fig_placeholder = col2_grid.empty()
    ''
    # Initialize figure variables
    fig_shot_chart = None
    fig_hex_map = None
    fig_shot_zone = None
    fig_heat_Map = None
    # Display the selected figure
    if shot_chart:
        st.toast(f'Plotting Started !:bar_chart:')

        # Draw shooting map
        fig_shot_chart = plt.figure(figsize=(12, 11))
        draw_chart.shot_chart(player_shotchart_df, title=f"{selected_player} Shot Chart of {selected_season} season")

        fig_placeholder.pyplot(fig_shot_chart)
    elif hex_map:
        st.toast(f'Plotting Started !:bar_chart:')

        # Draw hex map
        fig_hex_map = plt.figure(figsize=(12, 11))
        draw_chart.hexmap_chart(player_shotchart_df, league_avg, title=f"{selected_player} Hex Map of {selected_season} season")

        fig_placeholder.pyplot(fig_hex_map)
    elif shot_zone:
        st.toast(f'Plotting Started !:bar_chart:')

        # Draw shot zone
        fig_shot_zone = plt.figure(figsize=(12, 11))
        draw_chart.shot_zones(player_shotchart_df, league_avg, title=f"{selected_player} Shot Zone Map of {selected_season} season")

        fig_placeholder.pyplot(fig_shot_zone)
    elif heatmap:
        st.toast(f'Plotting Started !:bar_chart:')

        # Draw HeatMap
        fig_heat_Map = plt.figure(figsize=(12, 11))
        draw_chart.heatmap(player_shotchart_df, title=f"{selected_player} HeatMap of {selected_season} season")

        fig_placeholder.pyplot(fig_heat_Map)