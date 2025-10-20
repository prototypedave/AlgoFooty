import pandas as pd

cols = ["home_team", "away_team", "match_time", "prefer", "probability", "prediction", "odds"]
def get_home_win(predictions: pd.DataFrame) -> tuple:
    pred = predictions.copy()
    home_wins = pred[(pred["home"] == 1) & (pred["overall_result"] == 2)]
    home_wins = home_wins.sort_values(by=["home_win_prob", "over_win_prob"], ascending=False).head(20)
    home_wins = home_wins[(home_wins["home_roll_win"] >= 0.6) | (home_wins["h2h_win"] >= 0.6)]
    home_wins["prefer"] = (
        (home_wins["home_win_prob"] > home_wins["over_win_prob"]) |
        (home_wins["home_win_prob"] > home_wins["btts_win_prob"])
    )
    home_wins["prediction"] = "home win"
    home_wins.rename(columns={"home_win_prob": "probability", "1x2_home_win": "odds"}, inplace=True)
    home_wins = home_wins[cols]
    sure_home = home_wins.head(int(len(home_wins) * 0.25))
    return sure_home, home_wins.iloc[len(sure_home):].head(int(len(home_wins) * 0.5))


def get_away_win(predictions: pd.DataFrame) -> tuple:
    pred = predictions.copy()
    away_wins = pred[(pred["away"] == 1) & (pred["overall_result"] == 0)]
    away_wins = away_wins.sort_values(by=["away_win_prob", "over_win_prob"], ascending=False).head(20)
    away_wins = away_wins[(away_wins["h2h_lost"] >= 0.6)]
    away_wins["prefer"] = (
        (away_wins["away_win_prob"] > away_wins["over_win_prob"]) |
        (away_wins["away_win_prob"] > away_wins["btts_win_prob"])
    )
    away_wins["prediction"] = "away_win"
    away_wins.rename(columns={"away_win_prob": "probability", "1x2_away_win": "odds"}, inplace=True)
    away_wins = away_wins[cols]
    sure_away = away_wins.head(int(len(away_wins) * 0.25))
    return sure_away, away_wins.iloc[len(sure_away):].head(int(len(away_wins) * 0.5))


def get_btts_win(predictions: pd.DataFrame) -> tuple:
    pred = predictions.copy()
    btts_wins = pred[(pred["btts_win"] == 1)]
    btts_wins = btts_wins.sort_values(by=["btts_win_prob", "over_win_prob"], ascending=False).head(20)
    btts_wins = btts_wins[(btts_wins["h2h_btts"] >= 0.6) & (btts_wins["home_roll_btts"] >= 0.6) & (btts_wins["away_roll_btts"] >= 0.6)]
    btts_wins["prefer"] = (
        (btts_wins["btts_win_prob"] > btts_wins["over_win_prob"]) |
        (btts_wins["btts_win_prob"] > btts_wins["home_win_prob"]) | 
        (btts_wins["btts_win_prob"] > btts_wins["away_win_prob"])
    )
    btts_wins["prediction"] = "btts yes"
    btts_wins.rename(columns={"btts_win_prob": "probability", "both_teams_to_score_yes": "odds"}, inplace=True)
    btts_wins = btts_wins[cols]
    sure_btts = btts_wins.head(int(len(btts_wins) * 0.25))
    return sure_btts, btts_wins.iloc[len(sure_btts):].head(int(len(btts_wins) * 0.5))


def get_over_win(predictions: pd.DataFrame) -> tuple:
    pred = predictions.copy()
    over_wins = pred[(pred["over_win"] == 1)]
    over_wins = over_wins.sort_values(by=["over_win_prob", "btts_win_prob", "home_win", "away_win"], ascending=False).head(20)
    over_wins = over_wins[(over_wins["h2h_25"] >= 0.6)]
    over_wins["prefer"] = (
        (over_wins["over_win_prob"] > over_wins["btts_win_prob"]) |
        (over_wins["over_win_prob"] > over_wins["home_win_prob"]) | 
        (over_wins["over_win_prob"] > over_wins["away_win_prob"])
    )
    over_wins["prediction"] = "over 2.5"
    over_wins.rename(columns={"over_win_prob": "probability", 'over/under_over_25': "odds"}, inplace=True)
    over_wins = over_wins[cols]
    sure_over = over_wins.head(int(len(over_wins) * 0.25))
    return sure_over, over_wins.iloc[len(sure_over):].head(int(len(over_wins) * 0.5))

def make_predictions(predictions: pd.DataFrame) -> None:
    sure_home, home_wins = get_home_win(predictions)
    sure_away, away_wins = get_away_win(predictions)
    sure_btts, btts_wins = get_btts_win(predictions)
    sure_over, over_wins = get_over_win(predictions)

    sure_preds = pd.concat([sure_home, sure_away, sure_btts, sure_over], ignore_index=True)
    sure_preds = sure_preds.sort_values(by="prefer", ascending=False)
    sure_preds = sure_preds.drop_duplicates(subset=["home_team", "away_team", "match_time"], keep="first")
    print("SURE PREDICTIONS")
    print(sure_preds)

    other_preds = pd.concat([home_wins, away_wins, btts_wins, over_wins], ignore_index=True)
    other_preds = other_preds.sort_values(by="prefer", ascending=False)
    other_preds = other_preds.drop_duplicates(subset=["home_team", "away_team", "match_time"], keep="first")
    print("OTHER PREDICTIONS")
    print(other_preds)