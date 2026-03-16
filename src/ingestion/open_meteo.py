import openmeteo_requests
from retry_requests import retry
import requests_cache

URL = "https://api.open-meteo.com/v1/forecast"
params = { ... }  # pareil que ton dictionnaire

def fetch_weather_raw():
    # Récupère les données brutes depuis l'API Open-Meteo
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    client = openmeteo_requests.Client(session=retry_session)
    
    responses = client.weather_api(URL, params=params)
    return responses[0]  # renvoie l'objet brut