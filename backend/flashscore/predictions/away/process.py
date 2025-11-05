import pandas as pd
import numpy as np
from .predictions import tf_train, tf_predict
from sqlalchemy import create_engine

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
    save_predictions(tf_away)


def assemble_prev_results(df: pd.DataFrame, pref="h"):
    cols = [[f"{pref}_win_0", f"{pref}_win_1", f"{pref}_win_2", f"{pref}_win_3"], 
            [f"{pref}_draw_0", f"{pref}_draw_1", f"{pref}_draw_2", f"{pref}_draw_3"],
            [f"{pref}_lost_0", f"{pref}_lost_1", f"{pref}_lost_2", f"{pref}_lost_3"]]
    return np.stack((df[cols[0]].values, df[cols[1]].values, df[cols[2]].values), axis=-1) # win, draw, lost


def save_predictions(away: pd.DataFrame) -> None:
    save_cols = ["home_team", "away_team", "league", "round", "country", "odds", "match_time", "win", "home_score", "away_score", "proba", "home_img", "away_img"]
    away = away.drop_duplicates(subset=["home_team", "away_team", "match_time"], keep="first")
        
    away = away.rename(columns={'1x2_away_win': "odds"})
    away["win"] = pd.NA
    away["home_score"] = pd.NA
    away["away_score"] = pd.NA

    # update club icons !!!
   
    conn = create_engine("postgresql+psycopg2://postgres:your_password@localhost:5432/final")
    away[save_cols].to_sql("away_pred", con=conn, if_exists="append", index=False)