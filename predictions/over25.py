from models.classifier import classifier_model, filter_predictions
from .utils import train_test_split, create_data, confidence_threshold
import pandas as pd

FEAT_COLS_25 = [
    'h2h_over_15', 'h2h_htm_over_15', 'h2h_over_25', 'h2h_htm_over_25', 
    'country_under_15', 'league_btts', 'league_over_15_htm', 'league_over_15_atm', 
    'league_htm_cleansheet', 'league_ovr_cleansheet', 'league_under_35', 
    'league_htm_score', 'over_15_tm_away_mean', 'over_25_home_mean', 
    'home_score_home_avg', 'away_score_away_avg', 'home_goal_diff', 'away_goal_diff',
    'away_wins', 'home_draw', 'away_draw', 'away_btts', 'home_over_15_tm', 
    'away_over_15_tm', 'home_cleansheet_home_avg', 'away_cleansheet_away_avg',
    'home_ovr_cleansheet', 'home_score_home_roll_mean', 'goal_diff_home_roll_mean',
    'wins_home_roll_mean', 'btts_home_roll_mean', 'over_15_tm_away_roll_mean',
    'away_cleansheet_away_roll_mean', 'over_15_home_roll_mean', 'home_over_15', 
    'home_over_25', 'away_over_15',
]

COLS_25_WITH_ODDS = FEAT_COLS_25 + ['y_pred', 'y_proba', 'odds_over_25', 
                        'odds_under_25', 'odds_over_15', 'odds_under_15' ]

def predict_over_25(train_features, pred_features, final_df):
    X = train_features[FEAT_COLS_25]
    y = train_features['over_25']
    X_pred = pred_features[FEAT_COLS_25] 
    train_size = int(0.8 * len(train_features))
    X_train, y_train, X_test, y_test = train_test_split(X, y, train_size)

    # Initial model training
    y_pred, y_proba, pred_df = classifier_model(X_train, X_test, y_train, y_test, X_pred, pred_features)

    # Odds train
    F_pred = pred_df[COLS_25_WITH_ODDS]
    F_train, f_train, F_test, f_test = create_data(train_features, y_test, y_pred, y_proba, COLS_25_WITH_ODDS)
    f_proba, f_pred, pred_df = filter_predictions(F_train, F_test, f_train, f_test, F_pred, pred_df)
    
    # High confidence over
    confidence = confidence_threshold(f_pred, f_proba, f_test, start=0.87)
    over = pred_df[(pred_df['proba'] >= confidence)]

    # High confidence under
    confidence = confidence_threshold(f_pred, f_proba, f_test, start=0.02, mode='low')
    under = pred_df[(pred_df['proba'] <= confidence)]

    final_df['pred25'] = f_pred
    final_df['proba25'] = f_proba
    pred_df = pred_df.rename(columns={'y_pred': 'pred25', 'y_proba': 'proba25'}).drop(columns=['prediction'])
    return pd.concat([over, under], ignore_index=True), pred_df, final_df, f_test
