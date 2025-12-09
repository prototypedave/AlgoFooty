import pandas as pd
import math
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


load_dotenv()

def retrieve_predictions(engine, tb, date):
    query = f"""
        SELECT *
        FROM {tb}
        WHERE DATE(match_time) = '{date}'
        """
    return pd.read_sql(query, con=engine)

def assign_prediction_obj(df, pred, odds):
    df["match_time"] = (
        pd.to_datetime(df["match_time"]).dt.tz_localize("America/New_York").dt.tz_convert("UTC")  
    )
    records = []
    for l, k, j, m, n, i, o, p, q, r, s, t, u, v in zip(df["home_team"], df["away_team"], 
                                         df["proba"], odds, df["match_time"], 
                                         df["win"], df["country"], df["round"],
                                         df["league"], df["home_img"], df["away_img"],
                                         df["home_score"], df["away_score"], df["win"]):
        records.append({
            "home": l, "away": k, "probability": j,
            "odds": m, "prediction": pred, "date": n,
            "won": i, "country": o, "round": p,
            "league": q, "hicon": r, "aicon": s,
            "hscore": t, "ascore": u, "win": v
        })
    return records

def todays_predictions(day):
    predictions = []
    date = (datetime.now() - timedelta(days=day)).date()
    engine = create_engine(os.getenv("DB_CONN"))

    home_wins = retrieve_predictions(engine, os.getenv("HOME_TABLE"), date)
    home_wins = home_wins.drop_duplicates(subset=["home_team", "away_team", "match_time"])
    odds = home_wins["odds"].values
    predictions.extend(assign_prediction_obj(home_wins, "home win", odds))
    total_odds = math.prod(odds)

    away_wins = retrieve_predictions(engine, os.getenv("AWAY_TABLE"), date)
    away_wins = away_wins.drop_duplicates(subset=["home_team", "away_team", "match_time"])
    odds = away_wins["odds"].values
    predictions.extend(assign_prediction_obj(away_wins, "away win", odds))
    total_odds = total_odds * math.prod(odds)

    over = retrieve_predictions(engine, os.getenv("OVER_TABLE"), date)
    over = over.drop_duplicates(subset=["home_team", "away_team", "match_time"])
    odds = over["odds"].values
    predictions.extend(assign_prediction_obj(over, "over 2.5", odds))
    total_odds = total_odds * math.prod(odds)

    return predictions


def todays_sure_predictions(day):
    predictions = []
    date = (datetime.now() - timedelta(days=day)).date()
    engine = create_engine(os.getenv("DB_CONN"))

    home_wins = retrieve_predictions(engine, os.getenv("HOME_SURE_TABLE"), date)
    home_wins = home_wins.drop_duplicates(subset=["home_team", "away_team", "match_time"])
    odds = home_wins["odds"].values
    predictions.extend(assign_prediction_obj(home_wins, "home win", odds))
    total_odds = math.prod(odds)

    away_wins = retrieve_predictions(engine, os.getenv("AWAY_SURE_TABLE"), date)
    away_wins = away_wins.drop_duplicates(subset=["home_team", "away_team", "match_time"])
    odds = away_wins["odds"].values
    predictions.extend(assign_prediction_obj(away_wins, "away win", odds))
    total_odds = total_odds * math.prod(odds)

    over = retrieve_predictions(engine, os.getenv("OVER_SURE_TABLE"), date)
    over = over.drop_duplicates(subset=["home_team", "away_team", "match_time"])
    odds = over["odds"].values
    predictions.extend(assign_prediction_obj(over, "over 2.5", odds))
    total_odds = total_odds * math.prod(odds)

    return predictions


if __name__ == '__main__':
    print(todays_sure_predictions(0))
