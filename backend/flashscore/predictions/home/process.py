import pandas as pd
import numpy as np
from .predictions import tf_train, tf_predict, torch_train, torch_predict
from sklearn.preprocessing import StandardScaler
from sqlalchemy import create_engine

def predict_home_result(df: pd.DataFrame, pred:pd.DataFrame) -> None:
    df = df.sort_values("match_time")
    feat_home_df, feat_home_pred = assemble_prev_results(df, pref="h"), assemble_prev_results(pred, pref="h")
    feat_away_df, feat_away_pred = assemble_prev_results(df, pref="a"), assemble_prev_results(pred, pref="a")
    feat_h2h_df, feat_h2h_pred = assemble_prev_results(df, pref="h2h"), assemble_prev_results(pred, pref="h2h")
    
    cols = ["home_prob", "away_prob", "draw_prob"]
    feat_odd_df, feat_odd_pred = df[cols].values, pred[cols].values

    cols = ["home_w_rate", "home_l_rate", "home_d_rate", "away_w_rate", "away_l_rate", "away_d_rate",
            "home_win_rate_diff", "home_loss_rate_diff", "home_draw_rate_diff", "home_rank", "away_rank", 
            "home_points_diff", "home_scoring_diff", "home_conceding_diff", "home_goals_diff", "home_r_w_rate", "away_r_w_rate",
            "home_diff_roll_w_rate", "home_scoring_r_diff", "home_conceding_r_diff",
    ]
    feat_context_df, feat_context_pred = df[cols].values, pred[cols].values
    feat_home_away_df = np.concatenate((feat_home_df, feat_away_df), axis=-1)
    feat_home_away_pred = np.concatenate((feat_home_pred, feat_away_pred), axis=-1)
    
    model = tf_train(feat_home_away_df, feat_h2h_df, feat_odd_df, feat_context_df, df["match_home"])
    tf_home, tf_dependant = tf_predict(model, feat_home_away_pred, feat_h2h_pred, feat_odd_pred, feat_context_pred, pred)
   
    scaler = StandardScaler()
    feat_context_df = scaler.fit_transform(feat_context_df)
    feat_context_pred = scaler.transform(feat_context_pred)
    model_torch = torch_train(feat_home_away_df, feat_h2h_df, feat_odd_df, feat_context_df, df["match_home"].values)
    torch_home, torch_dependant = torch_predict(model_torch, feat_home_away_pred, feat_h2h_pred, feat_odd_pred, feat_context_pred, pred)

    #print(tf_home, torch_home)
    save_predictions(tf_home, tf_dependant, torch_home, torch_dependant)


def save_predictions(tf_home, tf_dependant, torch_home, torch_dependant):
    save_cols = ["home_team", "away_team", "league", "round", "country", "odds", "match_time", "win", "home_score", "away_score", "proba", "home_img", "away_img"]
    if tf_dependant and not torch_dependant:
        home = tf_home
    elif torch_dependant and not tf_dependant:
        home = torch_home
    else:
        home = pd.concat([tf_home, torch_home], ignore_index=True).sort_values("proba", ascending=False)
        home = home.drop_duplicates(subset=["home_team", "away_team", "match_time"], keep="first")
        
    home = home.rename(columns={"1x2_home_win": "odds"})
    home["win"] = pd.NA
    home["home_score"] = pd.NA
    home["away_score"] = pd.NA
   
    conn = create_engine("postgresql+psycopg2://postgres:your_password@localhost:5432/final")
    home[save_cols].to_sql("home_pred", con=conn, if_exists="append", index=False)


def assemble_prev_results(df: pd.DataFrame, pref="h"):
    cols = [[f"{pref}_win_0", f"{pref}_win_1", f"{pref}_win_2", f"{pref}_win_3"], 
            [f"{pref}_draw_0", f"{pref}_draw_1", f"{pref}_draw_2", f"{pref}_draw_3"],
            [f"{pref}_lost_0", f"{pref}_lost_1", f"{pref}_lost_2", f"{pref}_lost_3"]]
    return np.stack((df[cols[0]].values, df[cols[1]].values, df[cols[2]].values), axis=-1) # win, draw, lost
 
