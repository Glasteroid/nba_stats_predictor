import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonType
from nba_api.stats.static import players
import wx

# Define the PlayerStats class as you have already done
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
        game_logs = playergamelog.PlayerGameLog(player_id=self.player_id, season=self.season, season_type_all_star=SeasonType.regular)
        df = game_logs.get_data_frames()[0]
        df = df.drop(['SEASON_ID', 'Player_ID', 'Game_ID', 'FG3M', 'FG3A', 'FTM', 'FTA', 'VIDEO_AVAILABLE', 'GAME_DATE', 'MATCHUP', 'WL', 'FGM', 'FGA', 'PF'], axis=1, errors='ignore')
        df = df.iloc[::-1]
        df = df.reset_index(drop=True)
        return df

    def display_stats(self):
        if self.df is not None:
            self.df.index = self.df.index + 1
            return self.df.head()
        else:
            return "No data available"

# Function to predict points
def predict_points(input_data):
    # Example data for training (this would be your actual dataset)
    data = {
        'season_avg_pts': [23, 21, 25, 30],
        'season_avg_ast': [5, 4, 6, 7],
        'season_avg_reb': [6, 5, 7, 8],
        'season_avg_min': [3, 2, 4, 3],
        'is_home_game': [1, 0, 1, 0],
        'opp_def_rating': [110.2, 108.0, 113.0, 109.5],
        'opp_ppg_allowed': [106.5, 104.5, 110.2, 105.0],
        'opp_fg_pct_allowed': [0.442, 0.450, 0.440, 0.455],
        'team_off_rating': [114.6, 112.3, 116.5, 118.0],
        'team_ppg': [113.3, 111.0, 115.5, 112.0],
        'team_pace': [101.1, 99.5, 102.0, 100.0],
        'target_pts': [28, 24, 30, 32]
    }

    # Create DataFrame from the example data
    df = pd.DataFrame(data)

    # Split data into features (X) and target (y)
    X = df.drop(columns=['target_pts'])
    y = df['target_pts']

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize XGBoost Regressor model
    model = xgb.XGBRegressor()

    # Train (fit) the model
    model.fit(X_train, y_train)

    # Create DataFrame from the input data
    df_input = pd.DataFrame([input_data])

    # Predict the points
    predicted_pts = model.predict(df_input)[0]
    return predicted_pts

# Create wxPython GUI
class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(400, 300))
        
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Create text controls for input
        self.player_name_label = wx.StaticText(self.panel, label="Player Name:")
        self.player_name_text = wx.TextCtrl(self.panel)
        
        self.season_label = wx.StaticText(self.panel, label="Season (e.g., 2023):")
        self.season_text = wx.TextCtrl(self.panel)
        
        # Button to trigger prediction
        self.predict_button = wx.Button(self.panel, label="Predict Points")
        self.predict_button.Bind(wx.EVT_BUTTON, self.on_predict)

        # Output area
        self.output_text = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE, size=(300, 100), value="Prediction will appear here")

        # Layout the components
        self.sizer.Add(self.player_name_label, 0, wx.ALL, 5)
        self.sizer.Add(self.player_name_text, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.season_label, 0, wx.ALL, 5)
        self.sizer.Add(self.season_text, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.predict_button, 0, wx.ALL | wx.CENTER, 5)
        self.sizer.Add(self.output_text, 0, wx.ALL | wx.EXPAND, 5)

        self.panel.SetSizer(self.sizer)
        self.Show()

    def on_predict(self, event):
        # Get the user inputs
        player_name = self.player_name_text.GetValue()
        season = self.season_text.GetValue()

        # Validate input
        if not player_name or not season:
            wx.MessageBox("Please enter both player name and season", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Create a PlayerStats object and fetch the data
        player_stats = PlayerStats(player_name, season)
        player_stats_df = player_stats.display_stats()

        # Here, we assume you have your feature columns ready and they are in the input_data dictionary
        input_data = {
            "season_avg_pts": 23,  # You can replace this with actual data from player_stats_df
            "season_avg_ast": 5,
            "season_avg_reb": 6,
            "season_avg_min": 3,
            "is_home_game": 1,
            "opp_def_rating": 110.2,
            "opp_ppg_allowed": 106.5,
            "opp_fg_pct_allowed": 0.442,
            "team_off_rating": 114.6,
            "team_ppg": 113.3,
            "team_pace": 101.1
        }

        # Predict the points using the trained model
        predicted_pts = predict_points(input_data)
        
        # Display the result in the output text control
        self.output_text.SetValue(f"Predicted Points: {predicted_pts:.2f}")

# Run the wxPython application
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None, title="NBA Player Points Prediction")
    app.MainLoop()
