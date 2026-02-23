from http.client import responses
import pandas as pd
import numpy as np
import requests
import requests_cache
from retry_requests import retry

STATUS_URL = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_status.json"

def fetch_velib():
    # Setup the Velib API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

    print("Fetching Velib data...")

    try:
        response = retry_session.get(STATUS_URL, timeout=10)  # Timeout de 10 secondes
        response.raise_for_status()  # Vérifier les erreurs HTTP
        data = response.json()
        

        # stations_data = data['data']['stations']

        # df = pd.DataFrame(stations_data)
        # df['date'] = pd.Timestamp.today().date()
        # df = df.drop(columns=['num_bikes_available_types'])

        # # df = df.astype('object').replace({np.nan: None})
        # print(df)

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
    df['last_reported'] = pd.to_datetime(df['last_reported'], unit='s').dt.date
    df['date'] = pd.Timestamp.today().date()
    df = df.drop(columns=['num_bikes_available_types'])
    # # df = df.astype('object').replace({np.nan: None})

    print(df.head())  # Print the first few rows of the DataFrame
    # print(df.columns.tolist())  # Print the column names
    # return df_stations

fetch_velib()