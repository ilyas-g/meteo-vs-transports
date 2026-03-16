import pandas as pd
import numpy as np

def process_hourly(response):
    """Transforme la partie hourly en DataFrame"""
    hourly = response.Hourly()
    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time() + response.UtcOffsetSeconds(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd() + response.UtcOffsetSeconds(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ),
        "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
        "relative_humidity_2m": hourly.Variables(1).ValuesAsNumpy(),
        "dew_point_2m": hourly.Variables(2).ValuesAsNumpy(),
        "apparent_temperature": hourly.Variables(3).ValuesAsNumpy(),
        "precipitation": hourly.Variables(4).ValuesAsNumpy(),
        "rain": hourly.Variables(5).ValuesAsNumpy(),
        "snowfall": hourly.Variables(6).ValuesAsNumpy(),
        "weather_code": hourly.Variables(7).ValuesAsNumpy(),
    }
    df = pd.DataFrame(hourly_data)
    return df.astype('object').replace({np.nan: None})


def process_daily(response):
    """Transforme la partie daily en DataFrame"""
    daily = response.Daily()
    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time() + response.UtcOffsetSeconds(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd() + response.UtcOffsetSeconds(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        ),
        "weather_code": daily.Variables(0).ValuesAsNumpy(),
        "temperature_2m_max": daily.Variables(1).ValuesAsNumpy(),
        "temperature_2m_min": daily.Variables(2).ValuesAsNumpy(),
        "apparent_temperature_max": daily.Variables(3).ValuesAsNumpy(),
        "apparent_temperature_min": daily.Variables(4).ValuesAsNumpy(),
        "precipitation_probability_max": daily.Variables(5).ValuesAsNumpy(),
        "wind_speed_10m_max": daily.Variables(6).ValuesAsNumpy(),
        "wind_gusts_10m_max": daily.Variables(7).ValuesAsNumpy(),
        "precipitation_sum": daily.Variables(8).ValuesAsNumpy(),
        "snowfall_sum": daily.Variables(9).ValuesAsNumpy(),
        "showers_sum": daily.Variables(10).ValuesAsNumpy(),
        "rain_sum": daily.Variables(11).ValuesAsNumpy(),
    }
    df = pd.DataFrame(daily_data)
    return df.astype('object').replace({np.nan: None})