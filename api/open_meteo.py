import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

URL = "https://api.open-meteo.com/v1/forecast"

PARAMS = {
    "latitude": 48.8534,
    "longitude": 2.3488,
    "daily": [
        "weather_code", "temperature_2m_max", "temperature_2m_min",
        "apparent_temperature_max", "apparent_temperature_min",
        "rain_sum", "snowfall_sum", "showers_sum",
        "precipitation_sum", "precipitation_hours",
        "precipitation_probability_max",
        "wind_gusts_10m_max", "wind_speed_10m_max",
    ],
    "hourly": ["temperature_2m", "rain", "snowfall"],
    "models": "meteofrance_seamless",
    "timezone": "Europe/Berlin",
    "past_days": 92,
    "forecast_days": 4
}


def fetch_weather():
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    client = openmeteo_requests.Client(session=retry_session)

    response = client.weather_api(URL, PARAMS)[0]

    # ---------- HOURLY ----------
    hourly = response.Hourly()
    hourly_df = pd.DataFrame({
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ),
        "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
        "rain": hourly.Variables(1).ValuesAsNumpy(),
        "snowfall": hourly.Variables(2).ValuesAsNumpy(),
    })

    # ---------- DAILY ----------
    daily = response.Daily()

    # 1️⃣ mapping réel : nom de variable -> index
    daily_var_index = {
        daily.Variables(i).Variable(): i
        for i in range(daily.VariablesLength())
    }

    # 2️⃣ contrat des variables attendues
    daily_variables = {
        "weather_code": "int",
        "temperature_2m_max": "float",
        "temperature_2m_min": "float",
        "apparent_temperature_max": "float",
        "apparent_temperature_min": "float",
        "rain_sum": "float",
        "snowfall_sum": "float",
        "showers_sum": "float",
        "precipitation_sum": "float",
        "precipitation_hours": "float",
        "precipitation_probability_max": "float",
        "wind_gusts_10m_max": "float",
        "wind_speed_10m_max": "float",
    }

    # 3️⃣ base du DataFrame
    daily_df = pd.DataFrame({
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        )
    })

    # 4️⃣ remplissage dynamique
    for var_name, var_type in daily_variables.items():
        if var_name in daily_var_index:
            idx = daily_var_index[var_name]
            daily_df[var_name] = daily.Variables(idx).ValuesAsNumpy()
        else:
            daily_df[var_name] = pd.NA

    # 5️⃣ conversion NA -> None (pour psycopg2)
    daily_df = daily_df.where(pd.notna(daily_df), None)

    # 6️⃣ synchronisation avec les colonnes SQL
    sql_columns = [
        "date",
        "weather_code",
        "temperature_2m_max",
        "temperature_2m_min",
        "apparent_temperature_max",
        "apparent_temperature_min",
        "rain_sum",
        "snowfall_sum",
        "showers_sum",
        "precipitation_sum",
        "precipitation_hours",
        "precipitation_probability_max",
        "wind_gusts_10m_max",
        "wind_speed_10m_max",
    ]

    daily_df = daily_df[sql_columns]

    # 7️⃣ final date conversion
    daily_df["date"] = daily_df["date"].dt.date

    return hourly_df, daily_df
