from .utils import train_test_split, create_data, confidence_threshold
from models.classifier import classifier_model, filter_predictions
import pandas as pd

FEAT_COLS_BTTS = [
    'h2h_over_15', 'h2h_htm_over_15', 'h2h_htm_over_25', 'h2h_atm_over_25', 
    'h2h_atm_win', 'h2h_htm_win', 'h2h_btts', 'h2h_htm_btts', 'country_wins',
    'country_over_15_tm', 'country_over_25', 'country_over_35', 'league_htm_cleansheet',
    'league_over_15_htm', 'league_over_15', 'league_over_25', 'league_under_15',
    'league_under_25', 'ovr_cleansheet_away_mean', 'over_15_away_mean', 
    'over_25_home_mean', 'under_25_home_mean', 'home_score_home_avg', 'away_win_away_avg',
    'home_btts', 'away_btts', 'over_15_home_home_avg', 'over_15_away_away_avg',
    'home_score_home_roll_mean',
]

COLS_BTTS_WITH_ODDS = FEAT_COLS_BTTS + ['y_pred', 'y_proba', 'odds_btts', ]

def predict_btts(train_features, pred_features, final_df):
    X = train_features[FEAT_COLS_BTTS]
    y = train_features['btts']
    X_pred = pred_features[FEAT_COLS_BTTS]   
    train_size = int(0.8 * len(train_features))
    X_train, y_train, X_test, y_test = train_test_split(X, y, train_size)

    # Btts training
    y_pred, y_proba, pred_df = classifier_model(X_train, X_test, y_train, y_test, X_pred, pred_features)
 
    pred_df['odds_btts'] =  pred_df['odds_over_15'] - pred_df['odds_btts_yes'] 
    F_pred = pred_df[COLS_BTTS_WITH_ODDS]
    F_train, f_train, F_test, f_test = create_data(train_features, y_test, y_pred, y_proba, COLS_BTTS_WITH_ODDS)
    f_proba, f_pred, pred_df = filter_predictions(F_train, F_test, f_train, f_test, F_pred, pred_df)
    
    # High confidence over
    confidence = confidence_threshold(f_pred, f_proba, f_test, start=0.90)
    btts = pred_df[(pred_df['proba'] >= confidence)]

    # High confidence under
    confidence = confidence_threshold(f_pred, f_proba, f_test, start=0.02, mode='low')
    no_btts = pred_df[(pred_df['proba'] <= confidence)]

    final_df['pred_btts'] = f_pred
    final_df['proba_btts'] = f_proba
    pred_df = pred_df.rename(columns={'y_pred': 'pred_btts', 'y_proba': 'proba_btts'}).drop(columns=['prediction'])
    return pd.concat([btts, no_btts], ignore_index=True), pred_df, final_df, f_test
    