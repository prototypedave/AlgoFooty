import pandas as pd
from processing.predict import predict

NONE_TO_ZERO_COLS = ['red_cards', 'yellow_cards']

AVOID_COLS = [
    'both_teams_to_score_yes', 'both_teams_to_score_no',
    'home_expected_goals_(xg)', 'away_expected_goals_(xg)',
    'home_ball_possession', 'away_ball_possession', 'home_total_shots',
    'away_total_shots', 'home_shots_on_target', 'away_shots_on_target',
    'home_big_chances', 'away_big_chances', 'home_corner_kicks',
    'away_corner_kicks', 'home_passes', 'away_passes',
    'home_xg_on_target_(xgot)', 'away_xg_on_target_(xgot)',
    'home_shots_off_target', 'away_shots_off_target', 'home_blocked_shots',
    'away_blocked_shots', 'home_shots_inside_the_box',
    'away_shots_inside_the_box', 'home_shots_outside_the_box',
    'away_shots_outside_the_box', 'home_hit_the_woodwork',
    'away_hit_the_woodwork', 'home_touches_in_opposition_box',
    'away_touches_in_opposition_box', 'home_accurate_through_passes',
    'away_accurate_through_passes', 'home_offsides', 'away_offsides',
    'home_free_kicks', 'away_free_kicks', 'home_long_passes',
    'away_long_passes', 'home_passes_in_final_third',
    'away_passes_in_final_third', 'home_crosses', 'away_crosses',
    'home_expected_assists_(xa)', 'away_expected_assists_(xa)',
    'home_throw-ins', 'away_throw-ins', 'home_fouls', 'away_fouls',
    'home_tackles', 'away_tackles', 'home_duels_won', 'away_duels_won',
    'home_clearances', 'away_clearances', 'home_interceptions',
    'away_interceptions', 'home_errors_leading_to_shot',
    'away_errors_leading_to_shot', 'home_errors_leading_to_goal',
    'away_errors_leading_to_goal', 'home_goalkeeper_saves',
    'away_goalkeeper_saves', 'home_xgot_faced', 'away_xgot_faced',
    'home_goals_prevented', 'away_goals_prevented',
    "home_headed_goals", "away_headed_goals"
]

def process_games(df: pd.DataFrame, pred_df:pd.DataFrame, engine):
    df = fill_na_with_zero(df, NONE_TO_ZERO_COLS)
    df = df.drop(columns=AVOID_COLS)
    df = (
        df
        .sort_values(['home_team','away_team','match_time'], ascending=[True,True,True])
        .drop_duplicates(subset=['home_team', 'away_team', 'match_time'], keep='last')
        .reset_index(drop=True)
    )
    df = df.dropna()
    pred_df = pred_df.dropna()
    df.loc[:, 'match_time'] = pd.to_datetime(df['match_time'])
    df = compute_metrics(df)
    pred_df["home_check"] = pred_df["home_win"] + pred_df["home_draw"]
    pred_df["away_check"] = pred_df["away_win"] + pred_df["away_draw"]
    df = df.sort_values(['match_time'])

    pred_df.loc[:, "match_time"] = pd.to_datetime(pred_df['match_time'])
    pred_df = pred_df.drop_duplicates(subset=["home_team", "away_team", "match_time"])

    feature_cols = [col for col in df.columns if col not in ["match_result", 
        "total_goals", "over_15", "over_25", "over_35", "btts", "match_home",
        "match_draw", "match_away", "match_time", "home_team", "away_team", "country",
        "index", "home_score", "away_score", 'home_yellow_cards', 'away_yellow_cards', 
        'home_red_cards', 'away_red_cards', "league", "round"]]
    df[feature_cols] = df[feature_cols].apply(pd.to_numeric, errors='coerce')
    pred_df[feature_cols] = pred_df[feature_cols].apply(pd.to_numeric, errors='coerce')
    
    pred_df['match_time'] = pd.to_datetime(pred_df['match_time'], errors='coerce')
    predict(df, pred_df, feature_cols, engine)    


def fill_na_with_zero(df: pd.DataFrame, cols: list):
    df = df.copy()
    for col in cols:
        df["home_" + col] = df["home_" + col].fillna(0)
        df["away_" + col] = df["away_" + col].fillna(0)
    
    return df


def compute_metrics(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    df['match_result'] = ((df['home_score'] > df['away_score']).astype(int)
                          - (df['away_score'] > df['home_score']).astype(int))
    df['total_goals'] = df['home_score'] + df['away_score']
    df['over_15'] = (df['total_goals'] >= 2).astype(int)
    df['over_25'] = (df['total_goals'] >= 3).astype(int)
    df['over_35'] = (df['total_goals'] >= 4).astype(int)
    df['btts'] = ((df['home_score'] > 0) & (df['away_score'] > 0)).astype(int)
    df['match_home'] = (df['home_score'] > df['away_score']).astype(int)
    df['match_draw'] = (df['home_score'] == df['away_score']).astype(int)
    df['match_away'] = (df['away_score'] > df['home_score']).astype(int)
    
    return df

