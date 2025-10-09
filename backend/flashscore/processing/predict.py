from processing.model import classifier_model
import pandas as pd

def predict(df, pred_df, cols, engine):
    df = df.sort_values("match_time").copy()
    pred_df = pred_df.copy()
    pred_df["home_score"] = pd.NA
    pred_df["away_score"] = pd.NA
    pred_df["won"] = pd.NA

    home_win = classifier_model(df, pred_df, cols, target_col='match_home', target_class=1, report=False)
    home_win = home_win.query("(home_games_goals_scored > home_games_goals_conceded) and h2h_win > 0.6 and" \
    "(home_check > away_check) ")
    if not home_win.empty:
        home_win.to_sql("home", con=engine, if_exists="append", index=False)
    
    away_win = classifier_model(df, pred_df, cols, target_col='match_away', target_class=1, report=False)
    away_win = away_win.query(" (away_games_goals_scored > away_games_goals_conceded) and away_check > home_check" \
    " and h2h_lost > 0.6 and (away_games_points - home_games_points) > 2").copy()
    if not away_win.empty:
        away_win.to_sql("away", con=engine, if_exists="append", index=False)

    btts = classifier_model(df, pred_df, cols, target_col='btts', target_class=1, report=False)
    btts = btts.query("home_btts > 0.4 and away_btts > 0.4 and home_games_goals_scored > home_games_goals_conceded" \
    " and away_games_goals_scored > away_games_goals_conceded")
    if not btts.empty:
        btts.to_sql("btts", con=engine, if_exists="append", index=False)
    
    over = classifier_model(df, pred_df, cols, target_col='over_25', target_class=1, report=False)
    over = over.query("(home_games_played * 3) <= (home_games_goals_scored + home_games_goals_conceded)" \
    " and (away_games_played * 3) <= (away_games_goals_scored + away_games_goals_conceded) and home_25 > 0.4 and away_25 > 0.4")
    if not over.empty:
        over.to_sql("over_two_five", con=engine, if_exists="append", index=False)
    