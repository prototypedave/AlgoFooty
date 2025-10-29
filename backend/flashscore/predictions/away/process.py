import pandas as pd
import numpy as np
from .predictions import tf_train, tf_predict
from sklearn.preprocessing import StandardScaler

def predict_away_result(df: pd.DataFrame, pred: pd.DataFrame) -> None:
    df = df.sort_values("match_time")
    feat_home_df, feat_home_pred = assemble_prev_results(df, pref="h"), assemble_prev_results(pred, pref="h")
    feat_away_df, feat_away_pred = assemble_prev_results(df, pref="a"), assemble_prev_results(pred, pref="a")
    feat_h2h_df, feat_h2h_pred = assemble_prev_results(df, pref="h2h"), assemble_prev_results(pred, pref="h2h")

    cols = ["home_prob", "away_prob", "draw_prob"]
    feat_odd_df, feat_odd_pred = df[cols].values, pred[cols].values
    cols = ["home_w_rate", "home_l_rate", "home_d_rate", "away_w_rate", "away_l_rate", "away_d_rate",
        "away_win_rate_diff", "away_loss_rate_diff", "away_draw_rate_diff", 
        "away_points_diff", "away_scoring_diff", "away_conceding_diff", "away_goals_diff", "home_r_w_rate", "away_r_w_rate",
        "away_diff_roll_w_rate", "away_scoring_r_diff",  "away_diff_rank"
    ]
    feat_context_df, feat_context_pred = df[cols].values, pred[cols].values
    feat_home_away_df = np.concatenate((feat_home_df, feat_away_df), axis=-1)
    feat_home_away_pred = np.concatenate((feat_home_pred, feat_away_pred), axis=-1)
    
    model = tf_train(feat_home_away_df, feat_h2h_df, feat_odd_df, feat_context_df, df["match_away"].values)
    tf_away = tf_predict(model, feat_home_away_pred, feat_h2h_pred, feat_odd_pred, feat_context_pred, pred)
    print(tf_away)


def assemble_prev_results(df: pd.DataFrame, pref="h"):
    cols = [[f"{pref}_win_0", f"{pref}_win_1", f"{pref}_win_2", f"{pref}_win_3"], 
            [f"{pref}_draw_0", f"{pref}_draw_1", f"{pref}_draw_2", f"{pref}_draw_3"],
            [f"{pref}_lost_0", f"{pref}_lost_1", f"{pref}_lost_2", f"{pref}_lost_3"]]
    return np.stack((df[cols[0]].values, df[cols[1]].values, df[cols[2]].values), axis=-1) # win, draw, lost