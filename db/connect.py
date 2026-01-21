# Connexion à Postgres

import pandas as pd

def insert_weather(df: pd.DataFrame, engine):
    df.to_sql(
        "weather_hourly",
        engine,
        if_exists="append",
        index=False,
        chunksize=1000
    )