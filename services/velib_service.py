from api.velib_metropole_informations import fetch_velib_informations
from api.velib_metropole_stations import fetch_velib_stations
from db.velib_repository import upsert_stations, upsert_informations
from config.database import engine


def velib_run():
    print("Fetching Velib station data...")
    df_stations = fetch_velib_stations()
    if df_stations is None:
        print("Erreur lors de la récupération des données des stations.")
        return
    print("Fetching Velib data informations...")
    df_informations = fetch_velib_informations()
    if df_informations is None:
        print("Erreur lors de la récupération des informations des stations.")
        return
    upsert_stations(engine, df_stations)
    upsert_informations(engine, df_informations)
