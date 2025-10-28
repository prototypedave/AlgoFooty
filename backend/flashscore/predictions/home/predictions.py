from .deep_tf import train_tf_model
from .deep_torch import train_model
import pandas as pd
import torch

def tf_train(seq_home_away, seq_h2h, odds, context, y):
    assert seq_home_away.shape[0] == seq_h2h.shape[0] == odds.shape[0] == context.shape[0]
    return train_tf_model(seq_home_away, seq_h2h, odds, context, y)


def tf_predict(model, seq_home_away, seq_h2h, odds, context, pred_df):
    assert seq_home_away.shape[0] == seq_h2h.shape[0] == odds.shape[0] == context.shape[0] == pred_df.shape[0]
    pred_df["proba"] = model.predict([seq_home_away, seq_h2h, odds, context])
    
    return home_selection(pred_df)

def torch_train(seq_home_away, seq_h2h, odds, context, y):
    train_size = int(seq_home_away.shape[0] * 0.8)
    X_home_away_train, y_train = seq_home_away[: train_size], y[: train_size]
    X_home_away_test, y_test = seq_home_away[train_size: ], y[train_size: ]
    X_h2h_train, X_h2h_test = seq_h2h[: train_size], seq_h2h[train_size: ]
    X_odds_train, X_odds_test = odds[: train_size], odds[train_size: ]
    X_context_train, X_context_test = context[: train_size], context[train_size: ]
    
    return train_model(X_home_away_train, y_train, X_home_away_test, y_test,
                        X_h2h_train, X_h2h_test, X_odds_train, X_odds_test, 
                        X_context_train, X_context_test)


def torch_predict(model, seq_home_away, seq_h2h, odds, context, pred_df):
    def to_tensor(x): return torch.tensor(x, dtype=torch.float32)
    seq_home_away = to_tensor(seq_home_away)
    seq_h2h = to_tensor(seq_h2h)
    odds = to_tensor(odds)
    context = to_tensor(context)

    model.eval()
    with torch.no_grad():
        pred_df["proba"] = model(seq_home_away, seq_h2h, odds, context)

    return home_selection(pred_df)


def home_selection(pred_df: pd.DataFrame) -> tuple:
    pred_df = pred_df[pred_df["proba"] > 0.55].copy()
    winner  = pred_df[(pred_df["h_win_0"] == 1) & (pred_df["h2h_ovr"] > 0.5) & (pred_df["h2h_win_0"] == 1)].copy()
    sub = True
    if winner.empty:
        pred_df.sort_values("proba", ascending=True).head(20)
        winner = pred_df[pred_df["fav_diff"] > 0.5].copy()
        sub = False
    
    return winner, sub