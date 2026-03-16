from src.open_meteo import fetch_weather
from db.weather_repository import upsert_daily, upsert_hourly
from config.database import engine


def weather_run():
    print("Fetching weather data...")
    hourly_dataframe, daily_dataframe = fetch_weather()
    upsert_daily(engine, daily_dataframe)
    upsert_hourly(engine, hourly_dataframe)
