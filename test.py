# necessary imports
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import Season, SeasonType
from nba_api.stats.static import players
import pandas as pd

class PlayerStats:
    def __init__(self, player_name, season):
        self.player_name = player_name
        self.season = season
        self.player_id = self.get_player_id()
        self.df = None
        if self.player_id:
            self.df = self.get_player_df()

    def get_player_id(self):
        player_data = players.find_players_by_full_name(self.player_name)

        # check data, if valid player, output id
        if len(player_data) > 0:
            player_id = player_data[0]['id']
            return player_id
        else:
            print(f'The given id for {self.player_name} is not valid')
            return None
            
    def get_player_df(self):
        # fetch logs and create dataframe from it
        game_logs = playergamelog.PlayerGameLog(player_id=self.player_id, season=self.season, season_type_all_star=SeasonType.regular)

        df = game_logs.get_data_frames()[0]

        # drop unneeded columns
        df = df.drop(['SEASON_ID', 'Player_ID', 'Game_ID', 'FG3M', 'FG3A', 'FTM', 'FTA', 'VIDEO_AVAILABLE', 'GAME_DATE', 'MATCHUP', 'WL', 'FGM', 'FGA', 'PF'], axis=1, errors='ignore')

        # reverse dataframe
        df = df.iloc[::-1]
        df = df.reset_index(drop=True)
    
        return df
    
    def display_stats(self):
        if self.df is not None:
            self.df.index = self.df.index + 1
            print(self.df.head())
        else:
            print("No data available")
    
def main():
    player_name = input("Please enter which player you would like to fetch game logs for: ")
    player_season = input("Please enter a season of your choosing (2023 = 2023-2024 season): ")
    
    player_stats = PlayerStats(player_name, player_season)
    player_stats.display_stats()
    
if __name__ == "__main__":
    main()