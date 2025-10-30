import pandas as pd
import numpy as np
from .predictions import tf_train, tf_predict
from sqlalchemy import create_engine

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
    save_predictions(over)
    

def assemble_prev_results(df: pd.DataFrame, pref="h") -> np.array:
    cols = [f"{pref}_ov_25_0", f"{pref}_ov_25_1", f"{pref}_ov_25_2", f"{pref}_ov_25_3"]
    return df[cols].values[..., np.newaxis]


def save_predictions(over: pd.DataFrame) -> None:
    save_cols = ["home_team", "away_team", "league", "round", "country", "odds", "match_time", "win", "home_score", "away_score", "proba"]
    over = over.drop_duplicates(subset=["home_team", "away_team", "match_time"], keep="first")
        
    over = over.rename(columns={'over/under_over_25': "odds"})
    over["win"] = pd.NA
    over["home_score"] = pd.NA
    over["away_score"] = pd.NA

    # update club icons !!!
   
    conn = create_engine("postgresql+psycopg2://postgres:your_password@localhost:5432/final")
    over[save_cols].to_sql("over_pred", con=conn, if_exists="append", index=False)