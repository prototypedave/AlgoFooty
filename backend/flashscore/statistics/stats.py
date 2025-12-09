from dotenv import load_dotenv
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os

load_dotenv()

def retrieve_tables(engine, tb):
    query = f"""
        SELECT * FROM {tb}"""
    return pd.read_sql(query, con=engine)

def get_records():
    from sqlalchemy import create_engine
    engine = create_engine(os.getenv("DB_CONN"))
    home = retrieve_tables(engine, os.getenv("OVER_SURE_TABLE"))

    home = home.dropna(subset=["win"])
    home = home[(home["proba"] > 0.82)].copy()
    print(len(home))
    ovr_home_wins = len(home[home["win"] == "true"]) / len(home)
    print(ovr_home_wins)
    #print(home)

def run():
    get_records()


if __name__ == "__main__":
    run()
