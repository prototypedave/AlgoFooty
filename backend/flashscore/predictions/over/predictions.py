from .deep_tf import train_tf_model
import pandas as pd

def tf_train(seq_home_away, seq_h2h, odds, game, y):
    assert seq_home_away.shape[0] == seq_h2h.shape[0] == odds.shape[0] == game.shape[0]
    return train_tf_model(seq_home_away, seq_h2h, odds, game, y)


def tf_predict(model, seq_home_away, seq_h2h, odds, context, pred_df):
    assert seq_home_away.shape[0] == seq_h2h.shape[0] == odds.shape[0] == context.shape[0] == pred_df.shape[0]
    pred_df["proba"] = model.predict([odds, context, seq_h2h, seq_home_away])
    return over_selection(pred_df)


def over_selection(pred: pd.DataFrame) -> pd.DataFrame:
    pred = pred[pred["proba"] > 0.55].sort_values("proba").copy()
    over = pred[(pred["h2h_r_over"] > 0.6) & (pred["away_r_over"] > 0.6) & (pred["away_over_0"] == 1)]

    if over.empty:
        return pred.tail(1)   
    return over