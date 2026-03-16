import pandas as pd

def process_velib_status(raw_stations: list) -> pd.DataFrame:
    """
    Transforme la liste brute de statuts de stations en DataFrame propre.
    """
    if not raw_stations:
        return pd.DataFrame()  # Retourne vide si aucune donnée

    df = pd.DataFrame(raw_stations)

    # Conversion des dates
    if 'last_reported' in df.columns:
        df['last_reported'] = pd.to_datetime(df['last_reported'], unit='s')
    df['date'] = pd.Timestamp.today().strftime('%Y-%m-%d')

    # Colonnes redondantes ou inutiles
    drop_cols = [
        'num_bikes_available_types', 
        'stationCode', 
        'station_opening_hours',
        'numBikesAvailable', 
        'numDocksAvailable'
    ]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    # Renommage des colonnes camelCase
    rename_mapping = {
        'numBikesAvailable': 'num_bikes_available',
        'numDocksAvailable': 'num_docks_available'
    }
    df = df.rename(columns={k: v for k, v in rename_mapping.items() if k in df.columns})

    # Conversion des booléens
    for col in ['is_installed', 'is_returning', 'is_renting']:
        if col in df.columns:
            df[col] = df[col].astype(bool)

    # Process the num_bikes_available_types to create separate columns for each bike type
    # This is a placeholder for the actual processing logic, which will depend on the structure of num_bikes_available_types
    # C'EST A UTILSER POUR TRAITER LES TYPES DE VÉLOS DISPONIBLES, SI NÉCESSAIRE
    # for _, row in df_stations.iterrows():
    #     for d in row['num_bikes_available_types']:
    #         bike_type, cnt = next(iter(d.items()))
    #         # INSERT into station_bike_counts …

    # Réorganisation des colonnes pour que 'date' soit à la 2ème position
    if 'date' in df.columns:
        cols = df.columns.tolist()
        cols.insert(1, cols.pop(cols.index('date')))
        df = df[cols]

    return df