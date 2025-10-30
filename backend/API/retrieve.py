import pandas as pd
import math
from datetime import datetime, timedelta
from sqlalchemy import create_engine

def retrieve_predictions(engine, tb, date):
    query = f"""
        SELECT *
        FROM {tb}
        WHERE DATE(match_time) = '{date}'
        """
    return pd.read_sql(query, con=engine)

def assign_prediction_obj(df, pred, odds):
    records = []
    for l, k, j, m, n, i, o, p, q in zip(df["home_team"], df["away_team"], 
                                         df["proba"], odds, df["match_time"], 
                                         df["win"], df["country"], df["round"],
                                         df["league"]):
        records.append({
            "home": l, "away": k, "probability": j,
            "odds": m, "prediction": pred, "date": n,
            "won": i, "country": o, "round": p,
            "league": q
        })
    return records

def todays_predictions(day):
    predictions = []
    date = (datetime.now() - timedelta(days=day)).date()
    engine = create_engine("postgresql+psycopg2://postgres:your_password@localhost:5432/final")

    home_wins = retrieve_predictions(engine, "home_pred", date)
    home_wins = home_wins.drop_duplicates(subset=["home_team", "away_team", "match_time"])
    odds = home_wins["odds"].values
    predictions.extend(assign_prediction_obj(home_wins, "home win", odds))
    total_odds = math.prod(odds)

    away_wins = retrieve_predictions(engine, "away_pred", date)
    away_wins = away_wins.drop_duplicates(subset=["home_team", "away_team", "match_time"])
    odds = away_wins["odds"].values
    predictions.extend(assign_prediction_obj(away_wins, "away win", odds))
    total_odds = total_odds * math.prod(odds)

    over = retrieve_predictions(engine, "over_pred", date)
    over = over.drop_duplicates(subset=["home_team", "away_team", "match_time"])
    odds = over["odds"].values
    predictions.extend(assign_prediction_obj(over, "over 2.5", odds))
    total_odds = total_odds * math.prod(odds)

    return predictions, total_odds