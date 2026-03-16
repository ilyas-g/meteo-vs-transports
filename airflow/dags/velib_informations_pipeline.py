from airflow.decorators import dag, task
from config.database import engine  # import centralisé
from datetime import datetime
from src.ingestion.velib_informations import fetch_velib_informations
from src.transformations.velib_informations import process_velib_stations
from src.loaders.loader import load_to_postgres

@dag(schedule="@daily", start_date=datetime(2026,3,16), catchup=False)
def velib_informations_pipeline():

    @task
    def extract():
        return fetch_velib_informations()

    @task
    def transform(raw_data):
        return process_velib_stations(raw_data)

    @task
    def load_to_db(cleaned_data):
        load_to_postgres(cleaned_data, "station_information", engine)

    extractedDatas = extract()
    cleanedDatas = transform(extractedDatas)
    load_to_db(cleanedDatas)

pipeline = velib_informations_pipeline()