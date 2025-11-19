from .deep_tf import train_tf_model
from .deep_torch import train_model
import pandas as pd
import torch

def tf_train(seq_home_away, seq_h2h, odds, context, y):
    #assert seq_home_away.shape[0] == seq_h2h.shape[0] == odds.shape[0] == context.shape[0]
    return train_tf_model(seq_home_away, seq_h2h, odds, context, y)


def tf_predict(model, seq_home_away, seq_h2h, odds, context, pred_df):
    assert seq_home_away.shape[0] == seq_h2h.shape[0] == odds.shape[0] == context.shape[0] == pred_df.shape[0]
    pred_df["proba"] = model.predict([seq_h2h, seq_home_away, odds, context])
    #print(pred_df[["home_team", "away_team", "proba"]].sort_values("proba"))
    print(btts_selection(pred_df))
    return pred_df.sort_values("proba").tail(1)

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
        pred_df["proba"] = model(seq_h2h, seq_home_away, odds, context)
    print(pred_df[["home_team", "away_team", "proba"]].sort_values("proba"))


def btts_selection(pred: pd.DataFrame) -> pd.DataFrame:
    pred = pred[pred["proba"] > 0.54].copy()
    return pred[(pred["h_btts_0"] == 1) & (pred["a_btts_0"] == 1) & (pred["h2h_btts_0"] == 1) & (pred["h2h_r_btts"] > 0.4)]
    