from nba_api.stats.endpoints import LeagueDashTeamStats
from nba_api.stats.static import teams

class OpponentStats:
    def __init__(self, team_name, season):
        self.team_name = team_name
        self.season = season
        self.team_id = self.get_team_id()
        if self.team_id:
            self.defensive_rating = self.get_defensive_rating(self.season)
        else:
            self.defensive_rating = None

    def get_team_id(self):
        team_data = teams.find_teams_by_full_name(self.team_name)
        if len(team_data) > 0:
            team_id = team_data[0]['id']
            return team_id
        else:
            print(f'The given id for {self.team_name} is not valid')
            return None

    def get_defensive_rating(self, season):
        season_str = f"{season}-{str(season + 1)[-2:]}"
        stats = LeagueDashTeamStats(
            season=season_str,
            measure_type_detailed_defense='Advanced',
            per_mode_detailed='PerGame',  # Per game stats
            season_type_all_star='Regular Season'
        )

        df = stats.get_data_frames()[0]
        
        team_df = df[df['TEAM_ID'] == self.team_id]
        
        if not team_df.empty:
            # Return the team's defensive rating
            defensive_rating = team_df[['DEF_RATING']].iloc[0]
            return int(defensive_rating)
        else:
            print(f"No data found for team ID: {self.team_id}")
            return None

if __name__ == "__main__":
    stats = OpponentStats("Miami Heat", 2022)
    print(stats.defensive_rating)