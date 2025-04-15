# necessary imports
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import Season, SeasonType
from nba_api.stats.static import players
import pandas as pd

# search for specific player and get data
player_name = "LeBron James"

player_data = players.find_players_by_full_name(player_name)

# check data, if valid player, output id
if (len(player_data) > 0):
    player_id = player_data[0]['id']
    print(f'The given id for {player_name} is {player_id}')
else:
    print(f'The given id for {player_name} is not valid')

# fetches player stats based on some categories
season = '2022'

# fetch logs and create dataframe from it
game_logs = playergamelog.PlayerGameLog(player_id=player_id, season=season, season_type_all_star=SeasonType.regular)

df = game_logs.get_data_frames()[0]

# drop unneeded columns
df = df.drop(['SEASON_ID', 'Player_ID', 'Game_ID', 'FG3M', 'FG3A', 'FTM', 'FTA', 'VIDEO_AVAILABLE'], axis=1)

# reverse dataframe
df = df.iloc[::-1]
df = df.reset_index(drop=True)

print(df.head())