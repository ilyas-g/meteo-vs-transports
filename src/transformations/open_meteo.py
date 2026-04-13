import pandas as pd
import numpy as np

def process_hourly(response):
    hourly = response["hourly"]

    df = pd.DataFrame({
        "date": pd.to_datetime(hourly["time"]),
        "temperature_2m": hourly["temperature_2m"],
        "relative_humidity_2m": hourly["relative_humidity_2m"],
        "dew_point_2m": hourly["dew_point_2m"],
        "apparent_temperature": hourly["apparent_temperature"],
        "precipitation": hourly["precipitation"],
        "rain": hourly["rain"],
        "snowfall": hourly["snowfall"],
        "weather_code": hourly["weather_code"],
    })

    return df.replace({np.nan: None})


def process_daily(response):
    daily = response["daily"]

    df = pd.DataFrame({
        "date": pd.to_datetime(daily["time"]),
        "weather_code": daily["weather_code"],
        "temperature_2m_max": daily["temperature_2m_max"],
        "temperature_2m_min": daily["temperature_2m_min"],
        "apparent_temperature_max": daily["apparent_temperature_max"],
        "apparent_temperature_min": daily["apparent_temperature_min"],
        "precipitation_probability_max": daily["precipitation_probability_max"],
        "wind_speed_10m_max": daily["wind_speed_10m_max"],
        "wind_gusts_10m_max": daily["wind_gusts_10m_max"],
        "precipitation_sum": daily["precipitation_sum"],
        "snowfall_sum": daily["snowfall_sum"],
        "showers_sum": daily["showers_sum"],
        "rain_sum": daily["rain_sum"],
    })

    return df.replace({np.nan: None})