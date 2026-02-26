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

    print("Fetching Velib data...")

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

    print("✓ Data fetched successfully!")
    stations_data = data['data']['stations']

    df = pd.DataFrame(stations_data)
    # df = df.drop(columns=['rental_methods'])
    df = df.drop(columns=['station_opening_hours'])
    # print(df['rental_methods'].head())
    # print(df.head())  # Print the first few rows of the DataFrame
    # print(df.columns.tolist())  # Print the column names
    print(df['rental_methods'].iloc[0])  # Premier élément
    print(type(df['rental_methods'].iloc[0]))  # Type de données
    # stations_data = data['data']['stations']
    # df_stations = pd.DataFrame(stations_data)

    # print(df_stations.head())  # Print the first few rows of the DataFrame
    # return df_stations

fetch_velib_informations()