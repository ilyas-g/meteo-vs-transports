# Nettoyage / transformation pandas

import pandas as pd

def prepare_weather_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df["date"] = pd.to_datetime(df["date"])
    return df