from sklearn.model_selection import train_test_split
from nba_api.stats.endpoints import PlayerGameLog
from nba_api.stats.static import players

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
        if len(player_data) > 0:
            player_id = player_data[0]['id']
            return player_id
        else:
            print(f'The given id for {self.player_name} is not valid')
            return None

    def get_player_df(self):
        season_str = f"{self.season}-{str(self.season + 1)[-2:]}"
        game_log = PlayerGameLog(player_id=self.player_id, season=season_str)
        df = game_log.get_data_frames()[0]
        
        return df[['PTS', 'REB', 'AST', 'STL', 'BLK', 'FG_PCT', 'FT_PCT']]

    def display_stats(self):
        if self.df is not None:
            self.df.index = self.df.index + 1
            return self.df.head()
        else:
            return "No data available"