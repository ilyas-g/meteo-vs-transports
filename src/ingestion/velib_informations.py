import requests_cache
from retry_requests import retry

INFO_URL = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_information.json"

def fetch_velib_informations():
    # Récupère les données brutes de l'API Velib avec cache et retry.
    # Ne fait aucun traitement sur les données.

    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

    try:
        response = retry_session.get(INFO_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data['data']['stations']  # renvoie la liste brute
    except Exception as e:
        print(f"❌ Erreur lors de l'appel API Velib: {e}")
        return []