from .utils import train_test_split, create_data, confidence_threshold
from models.classifier import classifier_match, filter_match
import numpy as np

FEAT_COLS_1X2 = [
    'h2h_over_15', 'h2h_over_25', 'h2h_atm_over_25', 'h2h_atm_win',
    'h2h_a_atm_win', 'h2h_a_htm_win', 'h2h_htm_win', 'h2h_btts',
    'h2h_htm_btts', 'league_goal_diff', 'league_draw', 'away_score_away_mean',
    'btts_home_mean', 'btts_away_mean', 'ovr_cleansheet_home_mean',
    'home_score_home_avg', 'away_score_away_avg', 'home_goal_diff',
    'away_goal_diff', 'home_wins', 'away_wins', 'home_win_home_avg',
    'away_win_away_avg', 'home_draw', 'away_draw', 'wins_home_roll_mean',
    'over_15_away_away_roll_mean', 'ovr_cleansheet_away_roll_mean',
    'over_15_away_roll_mean', 
]

COLS_1X2_WITH_ODDS = FEAT_COLS_1X2 + ['y_pred', 'proba0', 'proba1', 'proba2', 'odds_win', ]

def predict_match_result(train_features, pred_features, final_df):
    X = train_features[FEAT_COLS_1X2]
    y = train_features['match_result']
    X_pred = pred_features[FEAT_COLS_1X2] 
    train_size = int(0.8 * len(train_features))
    X_train, y_train, X_test, y_test = train_test_split(X, y, train_size)

    # Initial train
    y_pred, y_proba, pred_df = classifier_match(X_train, X_test, y_train, y_test, X_pred, pred_features)

    pred_df['odds_win'] = (pred_df['odds_win_2'] + pred_df['odds_win_1'] - pred_df['odds_draw'] )
    F_pred = pred_df[COLS_1X2_WITH_ODDS]
    F_train, f_train, F_test, f_test = create_data(train_features, y_test, y_pred, y_proba, COLS_1X2_WITH_ODDS)
    f_proba, f_pred, pred_df = filter_match(F_train, F_test, f_train, f_test, F_pred, pred_df)
   
    confidence = confidence_threshold(f_pred, np.max(f_proba, axis=1), f_test, start=0.80)
    pick = pred_df[(pred_df['proba'] >= confidence)]
    final_df['pred1x2'] = f_pred
    final_df['proba0'] = f_proba[:, 0]
    final_df['proba1'] = f_proba[:, 1]
    final_df['proba2'] = f_proba[:, 2]
    pred_df = pred_df.rename(columns={'proba': 'proba1x2', 'prediction': 'pred1x2'})
    return pick, pred_df, final_df, f_test
    

    