import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import Table, MetaData, update
from sqlalchemy import create_engine
import asyncio

async def retrieve_data_for_results(engine, days):
    prev = (datetime.now() - timedelta(days=days)).date()
    print(prev)
    query = f"""
        SELECT *
        FROM new_league
        WHERE DATE(match_time) = '{prev}'
    """
    return pd.read_sql(query, con=engine)


async def update_results(days: int = 1):
    engine = create_engine("postgresql+psycopg2://postgres:your_password@localhost:5432/final")
    df = await retrieve_data_for_results(engine, days)
    def safe_numeric(df, cols):
        for c in cols:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        return df

    # --- HOME ---
    home = pd.read_sql(query_const("home_pred", days), con=engine)
    home = update_df(df, home)
    home = safe_numeric(home, ["home_score", "away_score"])
    home["win"] = home.apply(
        lambda x: (
            x["home_score"] > x["away_score"]
            if pd.notnull(x["home_score"]) and pd.notnull(x["away_score"])
            else None
        ),
        axis=1
    )
    update_table(engine, "home_pred", home)

    # --- AWAY ---
    away = pd.read_sql(query_const("away_pred", days), con=engine)
    away = update_df(df, away)
    away = safe_numeric(away, ["home_score", "away_score"])
    away["win"] = away.apply(
        lambda x: (
            x["away_score"] > x["home_score"]
            if pd.notnull(x["away_score"]) and pd.notnull(x["home_score"])
            else None
        ),
        axis=1
    )
    update_table(engine, "away_pred", away)

    # --- OVER ---
    over = pd.read_sql(query_const("over_pred", days), con=engine)
    over = update_df(df, over)
    over = safe_numeric(over, ["home_score", "away_score"])
    over["win"] = over.apply(
        lambda x: (
            (x["home_score"] + x["away_score"]) >= 3
            if pd.notnull(x["home_score"]) and pd.notnull(x["away_score"])
            else None
        ),
        axis=1
    )
    update_table(engine, "over_pred", over)

    
    
def query_const(table, days):
    prev = (datetime.now() - timedelta(days=days)).date()
    return f"""
        SELECT *
        FROM {table}
        WHERE DATE(match_time) = '{prev}'
        """

def update_df(df, met):
    key_cols = ["home_team", "away_team", "match_time"]
    update_cols = ["home_score", "away_score"]

    df = df.copy()
    met = met.copy()

    for col in ["home_team", "away_team"]:
        df[col] = df[col].astype(str).str.strip()
        met[col] = met[col].astype(str).str.strip()

    df['match_time'] = pd.to_datetime(df['match_time']).dt.tz_localize(None)
    met['match_time'] = pd.to_datetime(met['match_time']).dt.tz_localize(None)
    merged = met.merge(
        df[key_cols + update_cols],
        on=key_cols,
        how="left",
        suffixes=("", "_new")
    )

    for col in update_cols:
        new_col = f"{col}_new"
        merged[col] = merged[new_col].fillna(merged[col])
    
    merged = merged.drop(columns=[f"{col}_new" for col in update_cols], errors='ignore')
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
                    win=r["win"]
                )
            )
            conn.execute(stmt)


if __name__ == "__main__":
    async def main():
        await update_results()

    asyncio.run(main())