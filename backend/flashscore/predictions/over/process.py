import pandas as pd
import numpy as np
from .predictions import tf_train, tf_predict

def predict_over_2_5(df: pd.DataFrame, pred: pd.DataFrame) -> None:
    df = df.sort_values("match_time")
    cols = ["over_25_prob", "under_25_prob"]
    feat_odd_df, feat_odd_pred = df[cols].values, pred[cols].values
    cols = ["home_fav_over", "away_fav_over", "game_over", 
            "avg_scored", "avg_conceded"]
    feat_game_df, feat_game_pred = df[cols].values, pred[cols].values
    feat_h2h_df, feat_h2h_pred = assemble_prev_results(df, pref="h2h"), assemble_prev_results(pred, pref="h2h")
    feat_home_df, feat_home_pred = assemble_prev_results(df, "h"), assemble_prev_results(pred, "h")
    feat_away_df, feat_away_pred = assemble_prev_results(df, "a"), assemble_prev_results(pred, "a")
    feat_home_away_df = np.concatenate((feat_home_df, feat_away_df), axis=-1)
    feat_home_away_pred = np.concatenate((feat_home_pred, feat_away_pred), axis=-1)
    
    model = tf_train(feat_home_away_df, feat_h2h_df, feat_odd_df, feat_game_df, df["match_25"].values)
    over = tf_predict(model, feat_home_away_pred, feat_h2h_pred, feat_odd_pred, feat_game_pred, pred)
    

def assemble_prev_results(df: pd.DataFrame, pref="h"):
    cols = [f"{pref}_ov_25_0", f"{pref}_ov_25_1", f"{pref}_ov_25_2", f"{pref}_ov_25_3"]
    return df[cols].values[..., np.newaxis]