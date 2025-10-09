import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import Table, MetaData, update

def update_results(df: pd.DataFrame, engine):
    home = pd.read_sql(query_const("home"), con=engine)
    home = update_df(df, home)
    home["won"] = home["home_score"] > home["away_score"]
    update_table(engine, "home", home)

    away = pd.read_sql(query_const("away"), con=engine)
    away = update_df(df, away)
    away["won"] = away["away_score"] > away["home_score"]
    update_table(engine, "away", away)
    
    btts = pd.read_sql(query_const("btts"), con=engine)
    btts = update_df(df, btts)
    btts["won"] = (btts["away_score"] > 0) & (btts["home_score"] > 0)
    update_table(engine, "btts", btts)
    
    over = pd.read_sql(query_const("over_two_five"), con=engine)
    over = update_df(df, over)
    over["won"] = (over["home_score"] + over["away_score"]) >= 3
    update_table(engine, "over_two_five", over)
    
    
def query_const(table):
    prev = (datetime.now() - timedelta(days=1)).date()
    return f"""
        SELECT *
        FROM {table}
        WHERE DATE(match_time) = '{prev}'
        """

def update_df(df, met):
    key_cols = ["home_team", "away_team", "match_time"]
    update_cols = ["home_score", "away_score"]
    merged = met.merge(
        df[key_cols + update_cols],
        on=key_cols,
        how="left",
        suffixes=("", "_new")
    )

    # Fill missing values in df_base with those from df_updates
    for col in update_cols:
        merged[col] = (
            merged[col].astype(object)
            .combine_first(merged[f"{col}_new"].astype(object))
        )


    # Drop the extra _new columns
    merged = merged.drop(columns=[f"{col}_new" for col in update_cols])
    return merged

def update_table(engine, tb, df):
    metadata = MetaData()
    table = Table(tb, metadata, autoload_with=engine)
    with engine.begin() as conn:
        for _, r in df.iterrows():
            stmt = (
                update(table)
                .where(
                    (table.c.home_team == r["home_team"]) &
                    (table.c.away_team == r["away_team"]) &
                    (table.c.match_time == r["match_time"])
                )
                .values(
                    home_score=r["home_score"],
                    away_score=r["away_score"],
                    won=r["won"]
                )
            )
            conn.execute(stmt)
