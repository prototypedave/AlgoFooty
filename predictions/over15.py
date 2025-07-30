from models.classifier import classifier_model, filter_predictions
from .utils import train_test_split, create_data, confidence_threshold

FEAT_COLS_15 = [
    'h2h_over_15', 'h2h_htm_over_15', 'h2h_atm_over_15', 'h2h_under_35', 
    'h2h_htm_under_35', 'h2h_atm_under_35', 'h2h_a_atm_win', 'h2h_htm_win', 
    'h2h_htm_btts', 'country_over_15_tm', 'country_over_15', 'league_total_goals', 
    'league_goal_diff', 'league_wins', 'league_htm_win', 'league_draw', 
    'league_over_15', 'league_under_25', 'league_htm_score', 'league_atm_score', 
    'goal_diff_home_mean', 'wins_home_mean', 'home_win_home_mean', 'draw_home_mean', 
    'home_cleansheet_home_mean', 'under_15_home_mean', 'under_25_home_mean', 
    'under_35_home_mean', 'home_score_home_avg', 'over_15_home_home_avg', 
    'home_cleansheet_home_avg', 'goal_diff_home_roll_mean', 'home_score_home_roll_mean', 
    'over_15_home_home_roll_mean', 'wins_away_mean', 'btts_away_mean', 
    'over_15_tm_away_mean', 'away_cleansheet_away_mean', 'over_35_away_mean', 
    'away_over_15_tm', 'away_cleansheet_away_avg', 'under_35_away_roll_mean',
    'under_25_away_roll_mean', 'over_25_away_roll_mean', 'ovr_cleansheet_away_roll_mean', 
    'away_cleansheet_away_roll_mean', 'btts_away_roll_mean', 'goal_diff_away_roll_mean', 
    'away_over_25', 'home_over_25', 'away_under_15', 'home_under_15',
]

COLS_15_WITH_ODDS = FEAT_COLS_15 + ['y_pred', 'y_proba', 'odds_over_15', 'odds_under_15', 'odds_over_25', ]

def predict_over_15(train_features, pred_features):
    """
        Predicts matches that will end in a total goals of 2 or more
    """
    X = train_features[FEAT_COLS_15]
    y = train_features['over_15']
    X_pred = pred_features[FEAT_COLS_15] 
    train_size = int(0.8 * len(train_features))
    X_train, y_train, X_test, y_test = train_test_split(X, y, train_size)

    # First train without odds
    y_pred, y_proba, pred_df = classifier_model(X_train, X_test, y_train, y_test, X_pred, pred_features)

    # Train with odds
    F_pred = pred_df[COLS_15_WITH_ODDS]
    F_train, f_train, F_test, f_test = create_data(train_features, y_test, y_pred, y_proba, COLS_15_WITH_ODDS)
    f_proba, f_pred, pred_df = filter_predictions(F_train, F_test, f_train, f_test, F_pred, pred_df)

    confidence = confidence_threshold(f_pred, f_proba, f_test, start=0.90)
    return pred_df[(pred_df['proba'] >= confidence)], f_pred, f_proba, pred_df, f_test