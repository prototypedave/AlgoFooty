from models.classifier import classifier_model, filter_predictions
from .utils import train_test_split, create_data, confidence_threshold

import pandas as pd

FEAT_COLS_35 = [
    'h2h_over_15', 'h2h_htm_over_15', 'h2h_atm_over_15', 'h2h_over_25',
    'h2h_htm_over_25', 'h2h_under_35', 'h2h_htm_under_35', 'h2h_atm_win',
    'h2h_a_atm_win', 'h2h_htm_win', 'h2h_htm_btts', 'country_wins', 'country_atm_win',
    'country_over_25', 'over_15_tm_away_mean', 'under_35_home_mean', 'home_score_home_avg', 
    'away_score_away_avg', 'home_goal_diff', 'away_goal_diff', 'over_15_away_away_avg', 
    'home_ovr_cleansheet', 'home_cleansheet_home_roll_mean', 'ovr_cleansheet_home_roll_mean',
    'over_35_home_roll_mean', 'home_over_35', 'away_over_35', 'home_under_35', 'away_under_35',
]

COLS_35_WITH_ODDS = FEAT_COLS_35 + ['y_pred', 'y_proba', 'odds_over_35', 'odds_under_35', 
                                    'odds_under_25', 'odds_over_25', ]

def predict_over_35(train_features, pred_features, final_df):
    X = train_features[FEAT_COLS_35]
    y = train_features['under_35']
    X_pred = pred_features[FEAT_COLS_35] 
    train_size = int(0.8 * len(train_features))
    X_train, y_train, X_test, y_test = train_test_split(X, y, train_size)

    # Train the model
    y_pred, y_proba, pred_df = classifier_model(X_train, X_test, y_train, y_test, X_pred, pred_features)

    # Train with odds
    F_pred = pred_df[COLS_35_WITH_ODDS]
    F_train, f_train, F_test, f_test = create_data(train_features, y_test, y_pred, y_proba, COLS_35_WITH_ODDS)
    f_proba, f_pred, pred_df = filter_predictions(F_train, F_test, f_train, f_test, F_pred, pred_df)

    # High confidence over
    confidence = confidence_threshold(f_pred, f_proba, f_test, start=0.95)
    under = pred_df[(pred_df['proba'] >= confidence)]

    # High confidence under
    confidence = confidence_threshold(f_pred, f_proba, f_test, start=0.02, mode='low')
    over = pred_df[(pred_df['proba'] <= confidence)]

    final_df['pred35'] = f_pred
    final_df['proba35'] = f_proba
    pred_df = pred_df.rename(columns={'y_pred': 'pred35', 'y_proba': 'proba35'}).drop(columns=['prediction'])
    return pd.concat([over, under], ignore_index=True), pred_df, final_df, f_test