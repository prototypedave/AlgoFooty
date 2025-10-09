from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import IsolationForest
from sklearn.calibration import CalibratedClassifierCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score, log_loss
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
import random

random.seed(42)
np.random.seed(42)

MODEL_PARAMS = {
    "n_estimators": 500,
    "max_depth": 6,
    "learning_rate": 0.05,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "eval_metric": "logloss",
    "random_state": 42,
    "n_jobs": 1,
    "tree_method": "hist"
}

def classifier_model(df, df_pred, feature_cols, target_col="target", target_class=1, report=False):
    # --- Split data ---
    df = df.sort_values("match_time").reset_index(drop=True)
    if len(df) < 20:
        raise ValueError("Not enough samples for train/val/test split")

    train_size = int(len(df) * 0.7)
    val_size = int(len(df) * 0.15)

    train_df = df.iloc[:train_size]
    val_df = df.iloc[train_size:train_size + val_size]
    test_df = df.iloc[train_size + val_size:]

    # --- Features and target ---
    feature_cols = sorted(feature_cols)
    X_train, y_train = train_df[feature_cols], train_df[target_col]
    X_val, y_val = val_df[feature_cols], val_df[target_col]
    X_test, y_test = test_df[feature_cols], test_df[target_col]
    X_pred = df_pred[feature_cols]

    # --- Handle constant columns ---
    if X_train.var().eq(0).any():
        X_train = X_train.loc[:, X_train.var() != 0]
        feature_cols = X_train.columns.tolist()
        X_val = X_val[feature_cols]
        X_test = X_test[feature_cols]
        X_pred = X_pred[feature_cols]

    # --- Standardize ---
    stdsc = StandardScaler()
    X_train = pd.DataFrame(stdsc.fit_transform(X_train), columns=feature_cols)
    X_val = pd.DataFrame(stdsc.transform(X_val), columns=feature_cols)
    X_test = pd.DataFrame(stdsc.transform(X_test), columns=feature_cols)
    X_pred = pd.DataFrame(stdsc.transform(X_pred), columns=feature_cols)

    # --- Base model for feature selection ---
    base_model = XGBClassifier(**MODEL_PARAMS)
    base_model.fit(X_train, y_train)

    selector = SelectFromModel(base_model, prefit=True, threshold="median")
    selected_feat_mask = selector.get_support()

    if selected_feat_mask.sum() == 0:
        selected_features = X_train.columns
    else:
        selected_features = X_train.columns[selected_feat_mask]

    # --- Select features ---
    X_train_sel = X_train[selected_features]
    X_val_sel = X_val[selected_features]
    X_test_sel = X_test[selected_features]
    X_pred_sel = X_pred[selected_features]

    log_reg = LogisticRegression()
    log_reg.fit(X_train_sel, y_train)
    print(log_reg.score(X_test_sel, y_test))

    # --- Train with early stopping ---
    eval_set = [(X_val_sel, y_val)]
    model = XGBClassifier(**MODEL_PARAMS, early_stopping_rounds=50)
    model.fit(X_train_sel, y_train, eval_set=eval_set, verbose=False)
    best_iter = model.get_booster().best_iteration
    if report:
        print(f"Best iteration: {best_iter}")

    # --- Calibrate model ---
    method = "sigmoid" if len(X_val_sel) < 1000 else "isotonic"
    calibrated_model = CalibratedClassifierCV(estimator=model, method=method, cv="prefit")
    calibrated_model.fit(X_val_sel, y_val)

    # --- Outlier detection (optional if enough samples) ---
    if len(X_pred_sel) > 500:
        outlier_detector = IsolationForest(contamination=0.02, random_state=42)
        outlier_detector.fit(X_train_sel)
        outliers_pred = outlier_detector.predict(X_pred_sel) == -1
        print(f"Outliers removed: {outliers_pred.sum()} / {len(X_pred_sel)}")
        X_pred_clean = X_pred_sel[~outliers_pred]
        df_pred_clean = df_pred.loc[~outliers_pred].copy()
    else:
        X_pred_clean = X_pred_sel
        df_pred_clean = df_pred.copy()

    # --- Validation metrics ---
    target_class_idx = list(calibrated_model.classes_).index(target_class)
    y_val_proba = calibrated_model.predict_proba(X_val_sel)[:, target_class_idx]
    y_val_pred = calibrated_model.predict(X_val_sel)

    if report:
        print("Validation ROC-AUC:", roc_auc_score(y_val, y_val_proba))
        print("Validation Accuracy:", accuracy_score(y_val, y_val_pred))
        print("Validation LogLoss:", log_loss(y_val, y_val_proba))
        print("Validation Classification Report:")
        print(classification_report(y_val, y_val_pred))

    # --- Test metrics ---
    y_test_proba = calibrated_model.predict_proba(X_test_sel)[:, target_class_idx]
    y_test_pred = calibrated_model.predict(X_test_sel)

    if report:
        print("Test ROC-AUC:", roc_auc_score(y_test, y_test_proba))
        print("Test Accuracy:", accuracy_score(y_test, y_test_pred))
        print("Test LogLoss:", log_loss(y_test, y_test_proba))
        print("Test Classification Report:")
        print(classification_report(y_test, y_test_pred))

    # --- Predictions ---
    pred_labels = calibrated_model.predict(X_pred_clean)
    pred_probs = calibrated_model.predict_proba(X_pred_clean)[:, target_class_idx]

    df_pred_clean["predicted_label"] = pred_labels
    df_pred_clean["predicted_prob"] = pred_probs
    final_df = df_pred_clean.sort_values(by="predicted_prob", ascending=False)

    if report:
        print(final_df[["home_team", "away_team", "predicted_label", "predicted_prob", "country"]])

    return final_df

