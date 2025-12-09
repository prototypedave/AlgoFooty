import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from .home.process import predict_home_result
from .away.process import predict_away_result
from .over.process import predict_over_2_5
from dotenv import load_dotenv
import os


load_dotenv()

DROP_COLS = ["home_expected_goals_(xg)", "away_expected_goals_(xg)", "home_big_chances",
             "away_big_chances", "home_passes", "away_passes", "home_xg_on_target_(xgot)",
             "away_xg_on_target_(xgot)", "home_blocked_shots", "away_blocked_shots",
             "home_shots_inside_the_box", "away_shots_inside_the_box",
             "home_shots_outside_the_box", "away_shots_outside_the_box", 
             "home_hit_the_woodwork", "away_hit_the_woodwork", "home_touches_in_opposition_box",
             "away_touches_in_opposition_box", "home_accurate_through_passes",
             "away_accurate_through_passes", "home_offsides", "away_offsides",
             "home_free_kicks", "away_free_kicks", "home_long_passes", "away_long_passes",
             "home_passes_in_final_third", "away_passes_in_final_third", "home_crosses",
             "away_crosses", "home_expected_assists_(xa)", "away_expected_assists_(xa)",
             "home_throw-ins", "away_throw-ins", "home_fouls", "away_fouls", "home_tackles",
             "away_tackles", "home_duels_won", "away_duels_won", "home_clearances",
             "away_clearances", "home_interceptions", "away_interceptions",
             "home_errors_leading_to_shot", "away_errors_leading_to_shot", 
             "home_errors_leading_to_goal", "away_errors_leading_to_goal", "home_goalkeeper_saves",
             "away_goalkeeper_saves", "home_xgot_faced", "away_xgot_faced", 
             "home_goals_prevented", "away_goals_prevented"
        ]
NUN_COLS = ["home_red_cards", "away_red_cards", "home_yellow_cards", "away_yellow_cards",
            "home_headed_goals", "away_headed_goals"]


def run():
    process_records()


def get_data_records() -> tuple:
    from sqlalchemy import create_engine
    engine = create_engine(os.getenv("DB_CONN"))
    df = pd.read_sql(f"SELECT * FROM {os.getenv('LEAGUE_DB_TABLE')}", con=engine)
    today = (datetime.now() - timedelta(days=0)).date()
    query = f"""
        SELECT *
        FROM new_pred
        WHERE DATE(match_time) = '{today}'
    """
    pred = pd.read_sql(query, con=engine)
    return df, pred


def process_records():
    df, pred = get_data_records()
    df, pred = clean(df, pred)
    df, pred = get_results(df, pred)
    predict_home_result(df, pred)
    predict_away_result(df, pred)
    predict_over_2_5(df, pred)


def get_odds_probabilities(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["home_prob_raw"] = 1 / df["1x2_home_win"]
    df["draw_prob_raw"] = 1 / df["1x2_draw"]
    df["away_prob_raw"] = 1 / df["1x2_away_win"]
    df["overround"] = df["home_prob_raw"] + df["draw_prob_raw"] + df["away_prob_raw"] # margin

    df["home_prob"] = df["home_prob_raw"] / df["overround"]
    df["draw_prob"] = df["draw_prob_raw"] / df["overround"]
    df["away_prob"] = df["away_prob_raw"] / df["overround"]

    df["fav_diff"] = df[["home_prob", "draw_prob", "away_prob"]].max(axis=1) - df[["home_prob", "draw_prob", "away_prob"]].min(axis=1)

    df["draw_bias"] = df["draw_prob"] / (df["home_prob"] + df["away_prob"]) # not efficient for home win
    df["log_odds_ratio"] = np.log(df["1x2_home_win"] / df["1x2_away_win"])

    probs = df[["home_prob", "draw_prob", "away_prob"]].clip(1e-10, 1)  
    df["entropy"] = -(
        (probs["home_prob"] * np.log(probs["home_prob"])) +
        (probs["draw_prob"] * np.log(probs["draw_prob"])) +
        (probs["away_prob"] * np.log(probs["away_prob"]))
    )

    df["over_25_prob"] = (1 / df['over/under_over_25']) 
    df["under_25_prob"] = (1 / df['over/under_under_25']) 
    df["total_overround"] = df["over_25_prob"] + df["under_25_prob"]
    df["over_25_prob"] = df["over_25_prob"] / df["total_overround"]
    df["under_25_prob"] = df["under_25_prob"] / df["total_overround"]
    df["over_fav_diff"] = df[["over_25_prob", "under_25_prob"]].max(axis=1) - df[["over_25_prob", "under_25_prob"]].min(axis=1)

    df["btts_yes_prob"] = (1 / df['both_teams_to_score_yes']) 
    df["btts_no_prob"] = (1 / df['both_teams_to_score_no']) 
    df["total_bttsround"] = df["btts_yes_prob"] + df["btts_no_prob"]
    df["btts_yes_prob"] = df["btts_yes_prob"] / df["total_bttsround"]
    df["btts_no_prob"] = df["btts_no_prob"] / df["total_bttsround"]
    df["btts_fav_diff"] = df[["btts_yes_prob", "btts_no_prob"]].max(axis=1) - df[["btts_yes_prob", "btts_no_prob"]].min(axis=1)

    return df


def get_previous_team_results(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    pref_cols = ["h_win", "a_win", "h2h_win", "h_lost", "a_lost", "h2h_lost"]
    met_side_one_cols = ["home_h", "away_h", "h2h_h", "home_o", "away_o", "h2h_o"]
    met_side_two_cols = ["home_o", "away_o", "h2h_o", "home_h", "away_h", "h2h_h"]
    for i in range(4):
        for j, k, l in zip(pref_cols, met_side_one_cols, met_side_two_cols):
            df[f"{j}_{i}"] = (df[f"{k}_score_{i}"] > df[f"{l}_score_{i}"]).astype(int)
        df[f"h_draw_{i}"] = (df[f"home_h_score_{i}"] == df[f"home_o_score_{i}"]).astype(int)
        df[f"a_draw_{i}"] = (df[f"away_h_score_{i}"] == df[f"away_o_score_{i}"]).astype(int)
        df[f"h2h_draw_{i}"] = (df[f"h2h_h_score_{i}"] == df[f"h2h_o_score_{i}"]).astype(int)
        df[f"h_ov_25_{i}"] = df[[f"home_h_score_{i}", f"home_o_score_{i}"]].sum(axis=1) / 2.5
        df[f"a_ov_25_{i}"] = df[[f"away_h_score_{i}", f"away_o_score_{i}"]].sum(axis=1) / 2.5
        df[f"h2h_ov_25_{i}"] = df[[f"h2h_h_score_{i}", f"h2h_o_score_{i}"]].sum(axis=1)
        df[f"h_btts_{i}"] = ((df[f"home_h_score_{i}"] > 0) & (df[f"home_o_score_{i}"])).astype(int)
        df[f"a_btts_{i}"] = ((df[f"away_h_score_{i}"] > 0) & (df[f"away_o_score_{i}"])).astype(int)
        df[f"h2h_btts_{i}"] = ((df[f"h2h_h_score_{i}"] > 0) & (df[f"h2h_o_score_{i}"])).astype(int)
    return df


def get_previous_form(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for i, j in zip(["home_games", "away_games"], ["home", "away"]):
        for k, l in zip(["won", "lost", "drawn"], ["w_rate", "l_rate", "d_rate"]):
            df[f"{j}_{l}"] = df[f"{i}_{k}"] / df[f"{i}_played"]

    df = get_form_difference(df)
    return df


def get_form_difference(df: pd.DataFrame) -> pd.DataFrame:
    df = get_means(df)
    met_cols = [ "games_points", "games_goal_diff", "w_rate", "l_rate", "d_rate", 
                "games_goals_scored", "games_goals_conceded", "r_w_rate", 
                "r_l_rate", "r_score", "r_conceded", "r_points", "rank"]
    pref_cols = ["points_diff", "goals_diff", "win_rate_diff", "loss_rate_diff", 
                 "draw_rate_diff", "scoring_diff", "conceding_diff", 
                 "diff_roll_w_rate", "diff_roll_l_rate", "scoring_r_diff", 
                 "conceding_r_diff", "r_points_diff", "diff_rank"]
    for i, j in zip(["home", "away"], ["away", "home"]):
        for k, l in zip(met_cols, pref_cols):
            df[f"{i}_{l}"] = df[f"{i}_{k}"] - df[f"{j}_{k}"]
    
    return df


def get_over(df: pd.DataFrame) -> pd.DataFrame:
    for i in range(4):
        for j in ["home", "away", "h2h"]:
            df[f"{j}_over_{i}"] = (df[[f"{j}_h_score_{i}", f"{j}_o_score_{i}"]].sum(axis=1) > 2.5).astype(int)
    return df


def get_means(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for i, j in zip(["home", "away", "h2h"], ["h", "a", "h2h"]):
        df[f"{i}_ovr"] = (df[f"{j}_win_0"] + df[f"{j}_win_1"] + df[f"{j}_win_2"] + df[f"{j}_win_3"]) / 4
        df[f"{i}_r_w_rate"] = (df[f"{j}_win_0"] + df[f"{j}_win_1"] + df[f"{j}_win_2"] + df[f"{j}_win_3"]) / 4 
        df[f"{i}_r_l_rate"] = (df[f"{j}_lost_0"] + df[f"{j}_lost_1"] + df[f"{j}_lost_2"] + df[f"{j}_lost_3"]) / 4 
        df[f"{i}_last_3"] = (df[f"{j}_win_0"] + df[f"{j}_win_1"] + df[f"{j}_win_2"]) / 3
    
        df[f"{i}_r_score"] = (df[f"{i}_h_score_0"] + df[f"{i}_h_score_1"] + df[f"{i}_h_score_2"] )  
        df[f"{i}_r_conceded"] = (df[f"{i}_o_score_0"] + df[f"{i}_o_score_1"] + df[f"{i}_o_score_2"])
        df[f"{i}_r_over"] = df[[f"{i}_over_0", f"{i}_over_1", f"{i}_over_2", f"{i}_over_3"]].sum(axis=1) / 4
        df[f"{i}_r_btts"] = df[[f"{j}_btts_0", f"{j}_btts_1", f"{j}_btts_2", f"{j}_btts_3"]].sum(axis=1) / 4
    
        df["home_r_points"] = (((df["h_win_0"] * 3) + df["h_draw_0"]) + ((df["h_win_1"] * 3) + df["h_draw_1"]) + ((df["h_win_2"] * 3) + df["h_draw_2"]))
        df["away_r_points"] = (((df["a_win_0"] * 3) + df["a_draw_0"]) + ((df["a_win_1"] * 3) + df["a_draw_1"]) + ((df["a_win_2"] * 3) + df["a_draw_2"]))
   
    return df


def get_over_met(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["home_games_over"] = df["home_games_goals_scored"] + df["home_games_goals_conceded"]
    df["away_games_over"] = df["away_games_goals_scored"] + df["away_games_goals_conceded"]
    for i in ["over", "goals_scored", "goals_conceded"]:
        df[f"home_games_avg_{i}"] = df[f"home_games_{i}"] / df["home_games_played"]
        df[f"away_games_avg_{i}"] = df[f"away_games_{i}"] / df["away_games_played"]
    df["home_fav_over"] = df["home_games_avg_goals_scored"] + df["away_games_avg_goals_conceded"]
    df["away_fav_over"] = df["away_games_avg_goals_scored"] + df["home_games_avg_goals_conceded"]
    df["home_fav_btts"] = df["home_games_avg_goals_scored"] - df["away_games_avg_goals_conceded"]
    df["away_fav_btts"] = df["away_games_avg_goals_scored"] - df["home_games_avg_goals_conceded"]
    df["game_over"] = df["home_fav_over"] + df["away_fav_over"]
    df["avg_scored"] = df[["home_games_avg_goals_scored", "away_games_avg_goals_scored"]].sum(axis=1)
    df["avg_conceded"] = df[["home_games_avg_goals_conceded", "away_games_avg_goals_conceded"]].sum(axis=1)
    df["gh"] = (df["avg_scored"] + df["avg_conceded"]) / 2
    return df

def get_results(df: pd.DataFrame, pred: pd.DataFrame) -> pd.DataFrame:
    df["match_home"] = (df["home_score"] > df["away_score"]).astype(int)
    df["match_away"] = (df["away_score"] > df["home_score"]).astype(int)
    df["match_draw"] = (df["home_score"] == df["away_score"]).astype(int)
    df["total"] = df["home_score"] + df["away_score"]
    df["match_25"] = (df["total"] > 2.5).astype(int)
    df["match_btts"] = ((df["home_score"] > 0) & (df["away_score"] > 0)).astype(int)
    df["match_result"] = ((df["home_score"] > df["away_score"]).astype(int) - (df["away_score"] > df["home_score"]).astype(int))
    df["match_result"] = df["match_result"].map({1: 1, 0: 0, -1: 2})
    
    df, pred = get_over_met(df), get_over_met(pred)
    df, pred = get_over(df), get_over(pred)
    df, pred = get_odds_probabilities(df), get_odds_probabilities(pred)
    df, pred = get_previous_team_results(df), get_previous_team_results(pred)
    df, pred = get_previous_form(df), get_previous_form(pred)
    return df, pred


def clean(d: pd.DataFrame, pred: pd.DataFrame) -> pd.DataFrame:
    d = d.drop_duplicates(subset=["home_team", "away_team", "match_time"]).reset_index(drop=True)
    pred = pred.drop_duplicates(subset=["home_team", "away_team", "match_time"]).reset_index(drop=True)
    d = d.drop(columns=DROP_COLS)
    d[NUN_COLS] = d[NUN_COLS].fillna(0)
    d = d.dropna()
    #d = d.sort_values(by="match_time").tail(5000)
    pred = pred.dropna()
    return d, pred


if __name__ == "__main__":
    run()
