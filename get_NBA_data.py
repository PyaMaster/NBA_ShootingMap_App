# Data and NBA API
import pandas
import pandas as pd
import numpy as np

pd.options.display.max_columns = None
from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playercareerstats

def get_players_names():
    # Get all NBA players
    all_players = players.get_players()

    # Create a dictionary to store player names and their IDs
    players_dict = {}

    # Populate the dictionary with player names as keys and player IDs as values
    for player in all_players:
        players_dict[player['full_name']] = player['id']

    return players_dict

def get_player_seasons(player_id):
    # Player's career stats
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    career_df = career.get_data_frames()[0]

    # Extract seasons from career stats
    seasons = list(career_df['SEASON_ID'].unique())

    return seasons

def get_player_shotchartdetail(player_name, season_id):
    """
    Parameters
    ----------
    player_name: name of the player with Capital
    season_id: ex. 2012-13
    """

    # player dictionary
    nba_players = players.get_players()
    player_dict = [player for player in nba_players if player['full_name'] == player_name][0]

    # career df
    career = playercareerstats.PlayerCareerStats(player_id=player_dict['id'])
    career_df = career.get_data_frames()[0]

    # team id during the season
    team_id = career_df[career_df['SEASON_ID'] == season_id]['TEAM_ID']

    # shotchardtdetail endpoint
    shotchartlist = shotchartdetail.ShotChartDetail(team_id=int(team_id),
                                                    player_id=int(player_dict['id']),
                                                    season_type_all_star='Regular Season',
                                                    season_nullable=season_id,
                                                    context_measure_simple="FGA").get_data_frames()

    return shotchartlist[0], shotchartlist[1]

def get_seasons_stats(player_id):
    # Player's career stats
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    career_df = career.get_data_frames()[0]
    career_df = pandas.DataFrame(career_df)

    return career_df