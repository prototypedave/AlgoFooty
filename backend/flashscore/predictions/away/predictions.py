from .deep_tf import train_tf_model

def tf_train(seq_home_away, seq_h2h, odds, context, y):
    assert seq_home_away.shape[0] == seq_h2h.shape[0] == odds.shape[0] == context.shape[0]
    return train_tf_model(seq_home_away, seq_h2h, odds, context, y)


def tf_predict(model, seq_home_away, seq_h2h, odds, context, pred_df):
    assert seq_home_away.shape[0] == seq_h2h.shape[0] == odds.shape[0] == context.shape[0] == pred_df.shape[0]
    pred_df["proba"] = model.predict([seq_h2h, context, seq_home_away, odds])
    return pred_df.sort_values("proba").tail(1)