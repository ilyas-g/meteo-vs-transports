from http.client import responses
import pandas as pd
import numpy as np
import requests
import requests_cache
from retry_requests import retry

INFO_URL = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_information.json"

def fetch_velib():
    # Setup the Velib API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

    print("Fetching Velib data...")

    try:
        response = retry_session.get(INFO_URL, timeout=10)  # Timeout de 10 secondes
        response.raise_for_status()  # Vérifier les erreurs HTTP
        data = response.json()
        print("✓ Data fetched successfully!")

        stations_data = data['data']['stations']

        df = pd.DataFrame(stations_data)
        df['date'] = pd.Timestamp.today().date()
        df = df.drop(columns=['rental_methods'])
        # df = df.astype('object').replace({np.nan: None})
        print(df.head())


        # print(data['data']['stations'])  # Time to live for the data
    except requests.exceptions.Timeout:
        print("❌ Timeout: La requête a pris trop de temps")
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Impossible de se connecter à l'API")
    except Exception as e:
        print(f"❌ Error: {e}")
    # Process the data as needed
    # For example, you can convert it to a DataFrame
    # stations_data = data['data']['stations']
    # df_stations = pd.DataFrame(stations_data)

    # print(df_stations.head())  # Print the first few rows of the DataFrame
    # return df_stations

fetch_velib()