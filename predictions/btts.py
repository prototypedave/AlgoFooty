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

def predict_btts(train_features, pred_features):
    X = train_features[FEAT_COLS_BTTS]
    y = train_features['btts']
    X_pred = pred_features[FEAT_COLS_BTTS]
    
    train_size = int(0.8 * len(train_features))
    X_train = X.iloc[:train_size]
    y_train = y.iloc[:train_size]
    X_test = X.iloc[train_size:]
    y_test = y.iloc[train_size:]
    y_pred, y_proba, pred_df = classifier_model(X_train, X_test, y_train, y_test, X_pred, pred_features)

    odds_test = train_features.iloc[train_size:].copy()
    odds_test['y_pred'] = y_pred
    odds_test['y_proba'] = y_proba
    odds_test['odds_btts'] = odds_test['odds_over_15'] - odds_test['odds_btts_yes'] 
    pred_df['odds_btts'] =  pred_df['odds_over_15'] - pred_df['odds_btts_yes'] 


    X = odds_test[['y_pred', 'y_proba', 'odds_btts', ] + FEAT_COLS_BTTS]
    F_pred = pred_df[['y_pred', 'y_proba', 'odds_btts',] + FEAT_COLS_BTTS]
    y = y_test
    
    train_size = int(0.8 * len(odds_test))
    X_train = X.iloc[:train_size]
    y_train = y.iloc[:train_size]
    X_test = X.iloc[train_size:]
    y_test = y.iloc[train_size:]
    y_proba, y_pred, pred_df = filter_predictions(X_train, X_test, y_train, y_test, F_pred, pred_df)

    confident_acc = 0
    check = 0.80
    
    while confident_acc < 1:
        confident_mask = (y_proba >= check) 
        confident_preds = y_pred[confident_mask]
        confident_actuals = y_test[confident_mask]

        #print(f"🔍 Total confident predictions: {len(confident_preds)}")
        if len(confident_preds) > 0:
            confident_acc = (confident_preds == confident_actuals).mean()
            if check < 1.0 and confident_acc < 1.0:
                check += 0.005
                check = 1 if check > 1 else check
            elif check == 1 and confident_acc < 1:
                break
            #print(f"✅ Accuracy on 90%+ confident predictions: {confident_acc}" )
        #else:
        #    print("⚠️ No predictions with 90%+ confidence.")
    val = 0
    if (check + 0.02) < 1:
        val = check + 0.02
    elif (check + 0.01) < 1:
        val = check + 0.01
    elif (check + 0.005) < 1:
        val = check + 0.005
    else:
        val = 1
    over = pred_df[(pred_df['proba'] >= val)]

    confident_acc = 0
    check = 0.02
    
    while confident_acc < 1:
        confident_mask = (y_proba <= check) 
        confident_preds = y_pred[confident_mask]
        confident_actuals = y_test[confident_mask]

        #print(f"🔍 Total confident predictions: {len(confident_preds)}")
        if len(confident_preds) > 0:
            confident_acc = (confident_preds == confident_actuals).mean()
            if check > 0.0 and confident_acc < 1.0:
                check -= 0.005
                check = 0 if check < 0 else check
            elif check == 0 and confident_acc < 1:
                break
            #print(f"✅ Accuracy on 90%+ confident predictions: {confident_acc}" )
        #else:
        #    print("⚠️ No predictions with 90%+ confidence.")
    val = 0
    if (check - 0.02) > 0:
        val = check - 0.02
    elif (check - 0.01) > 0:
        val = check - 0.01
    elif (check - 0.005) > 0:
        val = check - 0.005
    else:
        val = 0
    under = pred_df[(pred_df['proba'] <= val)]

    return pd.concat([over, under], ignore_index=True), y_proba, y_pred, pred_df, y_test
