from api.open_meteo import fetch_weather
from db.weather_repository import upsert_daily, upsert_hourly
from config.database import engine


def run():
    hourly_df, daily_df = fetch_weather()
    upsert_daily(engine, daily_df)
    upsert_hourly(engine, hourly_df)
