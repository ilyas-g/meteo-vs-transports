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

    stations_data = data['data']['stations']
    df_stations = pd.DataFrame(stations_data)
    df_stations['last_reported'] = pd.to_datetime(df_stations['last_reported'], unit='s')
    # df_stations['recorded_at'] = pd.to_datetime(df_stations['recorded_at'], unit='s')
    df_stations['date'] = pd.Timestamp.today().strftime('%Y-%m-%d')
    # Supprimer les colonnes redondantes (camelCase)
    df_stations = df_stations.drop(columns=['numBikesAvailable', 'numDocksAvailable'])
    rename_mapping = {
        'numBikesAvailable': 'num_bikes_available',
        'numDocksAvailable': 'num_docks_available'
    }
    df_stations = df_stations.rename(columns={k: v for k, v in rename_mapping.items() if k in df_stations.columns})
    df_stations = df_stations.drop(columns=['num_bikes_available_types'])
    df_stations = df_stations.drop(columns=['stationCode'])

    # Suppression de la colonne station_opening_hours qui n'est pas nécessaire pour le suivi de l'état des stations
    # dû à un manque de données dans l'API (toutes les valeurs sont nulles)
    df_stations = df_stations.drop(columns=['station_opening_hours'])

    df_stations["is_installed"] = df_stations["is_installed"].astype(bool)
    df_stations["is_returning"] = df_stations["is_returning"].astype(bool)
    df_stations["is_renting"] = df_stations["is_renting"].astype(bool)

    # Process the num_bikes_available_types to create separate columns for each bike type
    # This is a placeholder for the actual processing logic, which will depend on the structure of num_bikes_available_types
    # C'EST A UTILSER POUR TRAITER LES TYPES DE VÉLOS DISPONIBLES, SI NÉCESSAIRE
    # for _, row in df_stations.iterrows():
    #     for d in row['num_bikes_available_types']:
    #         bike_type, cnt = next(iter(d.items()))
    #         # INSERT into station_bike_counts …
    
    cols = df_stations.columns.tolist()
    cols.insert(1, cols.pop(cols.index('date')))
    df_stations = df_stations[cols]
    # cols = df_informations.columns.tolist()
    # print(cols)
    return df_stations

fetch_velib_stations()