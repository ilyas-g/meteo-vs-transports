from http.client import responses
import pandas as pd
import numpy as np
import requests
import requests_cache
from retry_requests import retry

STATUS_URL = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_status.json"

def fetch_velib_stations():
    # Setup the Velib API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

    print("Fetching Velib data...")

    try:
        response = retry_session.get(STATUS_URL, timeout=10)  # Timeout de 10 secondes
        response.raise_for_status()  # Vérifier les erreurs HTTP
        data = response.json()
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
    df['last_reported'] = pd.to_datetime(df['last_reported'], unit='s').dt.strftime('%d-%m-%Y')
    df['date'] = pd.Timestamp.today().strftime('%d-%m-%Y')
    # Supprimer les colonnes redondantes (camelCase)
    df = df.drop(columns=['numBikesAvailable', 'numDocksAvailable'])
    df = df.drop(columns=['num_bikes_available_types'])

    # Process the num_bikes_available_types to create separate columns for each bike type
    # This is a placeholder for the actual processing logic, which will depend on the structure of num_bikes_available_types
    # C'EST A UTILSER POUR TRAITER LES TYPES DE VÉLOS DISPONIBLES, SI NÉCESSAIRE
    # for _, row in df.iterrows():
    #     for d in row['num_bikes_available_types']:
    #         bike_type, cnt = next(iter(d.items()))
    #         # INSERT into station_bike_counts …
    
    cols = df.columns.tolist()
    cols.insert(1, cols.pop(cols.index('stationCode')))
    cols.insert(2, cols.pop(cols.index('date')))
    df = df[cols]
    # # df = df.astype('object').replace({np.nan: None})

    print(df.head())  # Print the first few rows of the DataFrame
    print(df.columns.tolist())  # Print the column names
    # return df_stations

fetch_velib_stations()