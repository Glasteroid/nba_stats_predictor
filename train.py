import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from opponent_stats import OpponentStats
from player_stats import PlayerStats

def get_player_df(player_name, season):
    return PlayerStats(player_name=player_name, season=season)

def get_opponent_df(team_name, season):
    return OpponentStats(team_name=team_name, season=season)

if __name__ == "__main__":
    # gather input data
    player_input = input("Which player would you like to predict stats for: ")
    opponent_input = input("Which opponent is the player going against: ")
    season_input = int(input("Which season would you like to predict stats for: "))

    player_stats = get_player_df(player_input, season_input)
    opponent_stats = get_opponent_df(opponent_input, season_input)
    
    # gather data into data frames/int
    X = player_stats.df
    if X is None or X.empty:
        raise ValueError("Failed to retrieve player or opponent stats. Please check the inputs and try again.")
    
    y = opponent_stats.team_df
    if y is None:
        raise ValueError("Failed to retrieve player or opponent stats. Please check the inputs and try again.")
    
    y = X['PTS']
    X = X.drop(columns=['PTS'])
    
    defensive_features = ["DEF_RATING", "OPP_PTS", "OPP_FG_PCT", "OPP_REB", "OPP_TOV"]
    for feature in defensive_features:
        if feature in opponent_stats.team_df.columns:
            X[feature] = opponent_stats.team_df[feature].values[0]  # apply the same value to each row

    # split data into training and testing data - 20% of data is used to test the model predictions
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = xgb.XGBRegressor(objective='reg:squarederror')
    model.fit(X_train, y_train)
    
    prediction = model.predict(X_test)
    print(f"Predicted points: {prediction}")
    
    from sklearn.metrics import mean_absolute_error
    mae = mean_absolute_error(y_test, prediction)
    print(f"MAE: {mae}")
