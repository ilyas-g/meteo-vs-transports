import pandas as pd

def process_velib_stations(raw_stations: list) -> pd.DataFrame:
    """
    Transforme la liste brute de stations en DataFrame propre.
    """
    df = pd.DataFrame(raw_stations)

    # Supprimer les colonnes inutiles
    drop_cols = ['station_opening_hours', 'rental_methods']
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    # Remplacer les valeurs manquantes de capacity par 0
    if 'capacity' in df.columns:
        df['capacity'] = df['capacity'].fillna(0)

    return df