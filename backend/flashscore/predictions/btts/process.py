import pandas as pd
import numpy as np
from .predictions import tf_train, tf_predict, torch_train, torch_predict
from sklearn.preprocessing import StandardScaler

def predict_btts(df: pd.DataFrame, pred: pd.DataFrame) -> None:
    df = df.sort_values("match_time").copy()

    train_size = int(len(df) * 0.8)
    cols = ["home_goals_diff", "btts_fav_diff", "home_w_rate", "home_l_rate", "home_d_rate", "away_w_rate", 
            "away_l_rate", "away_d_rate", "home_rank", "away_rank", "home_games_goals_scored",
            "home_games_goals_conceded", "away_games_goals_scored", "away_games_goals_conceded",
            "home_games_points", "away_games_points"]
    feat_game_df, feat_game_pred = df[cols].values, pred[cols].values

    cols = ["btts_yes_prob", "btts_no_prob"]
    feat_odd_df, feat_odd_pred = df[cols].values, pred[cols].values
    feat_h2h_df, feat_h2h_pred = assemble_prev_results(df, "h2h"), assemble_prev_results(pred, "h2h")
    feat_home_df, feat_home_pred = assemble_prev_results(df), assemble_prev_results(pred)
    feat_away_df, feat_away_pred = assemble_prev_results(df, "a"), assemble_prev_results(pred, "a")
    feat_home_away_df = np.concatenate((feat_home_df, feat_away_df), axis=-1)
    feat_home_away_pred = np.concatenate((feat_home_pred, feat_away_pred), axis=-1)
    
    scaler = StandardScaler()
    feat_game_df, feat_game_pred = scaler.fit_transform(feat_game_df), scaler.transform(feat_game_pred)
    #model = tf_train(feat_home_away_df, feat_h2h_df, feat_odd_df, feat_game_df, df["match_btts"].values)
    #btts = tf_predict(model, feat_home_away_pred, feat_h2h_pred, feat_odd_pred, feat_game_pred, pred)
    model = torch_train(feat_home_away_df, feat_h2h_df, feat_odd_df, feat_game_df, df["match_btts"].values)
    btts = torch_predict(model, feat_home_away_pred, feat_h2h_pred, feat_odd_pred, feat_game_pred, pred)
    

def assemble_prev_results(df: pd.DataFrame, pref="h"):
    cols = [f"{pref}_btts_0", f"{pref}_btts_1", f"{pref}_btts_2", f"{pref}_btts_3"]
    return df[cols].values[..., np.newaxis]