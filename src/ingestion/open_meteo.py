import openmeteo_requests
from retry_requests import retry
from config.database import DATABASE_URL
import requests_cache

URL = "https://api.open-meteo.com/v1/forecast"
# params = { ... }  # pareil que ton dictionnaire

# Définir les paramètres localement pour éviter les problèmes de mutation
params = {
    "latitude": 48.866667,
    "longitude": 2.333333,
    "daily": [
        "weather_code", "temperature_2m_max", "temperature_2m_min", 
        "apparent_temperature_max", "apparent_temperature_min", 
        "precipitation_probability_max", "wind_speed_10m_max", 
        "wind_gusts_10m_max", "precipitation_sum", "snowfall_sum", 
        "showers_sum", "rain_sum"
    ],
    "hourly": [
        "temperature_2m", "relative_humidity_2m", "dew_point_2m", 
        "apparent_temperature", "precipitation", "rain", "snowfall", 
        "weather_code"
    ],
    "models": "meteofrance_seamless",
    "current": "temperature_2m",
    "timezone": "Europe/Berlin",
    "past_days": 31,
}

def fetch_weather_raw():
    # Récupère les données brutes depuis l'API Open-Meteo

    # cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)

    cache_session = requests_cache.CachedSession(
        backend='sqlite',
        cache_name='/tmp/cache',
        expire_after=3600
    )
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    client = openmeteo_requests.Client(session=retry_session)
    
    responses = client.weather_api(URL, params=params)
    return responses[0].to_dict() 