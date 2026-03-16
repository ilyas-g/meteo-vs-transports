from http.client import responses
import pandas as pd
import numpy as np
import requests
import requests_cache
from retry_requests import retry

INFO_URL = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_information.json"

def fetch_velib_informations():
    # Setup the Velib API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

    try:
        response = retry_session.get(INFO_URL, timeout=10)  # Timeout de 10 secondes
        response.raise_for_status()  # Vérifier les erreurs HTTP
        data = response.json()
        # print(data['data']['stations'])  # Time to live for the data
    except requests.exceptions.Timeout:
        print("❌ Timeout: La requête a pris trop de temps")
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Impossible de se connecter à l'API")
    except Exception as e:
        print(f"❌ Error: {e}")
    # Process the data as needed
    # For example, you can convert it to a DataFrame

    stations_data = data['data']['stations']

    df_informations = pd.DataFrame(stations_data)
    # df_informations = df_informations.drop(columns=['rental_methods'])
    df_informations = df_informations.drop(columns=['station_opening_hours'])
    df_informations = df_informations.drop(columns=['rental_methods'])

    df_informations['capacity'] = df_informations['capacity'].fillna(0)
    # print(df_informations_stations.head())  # Print the first few rows of the DataFrame
    # cols = df_informations.columns.tolist()
    # print(cols)
    return df_informations

fetch_velib_informations()