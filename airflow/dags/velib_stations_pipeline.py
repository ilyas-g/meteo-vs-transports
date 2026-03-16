from airflow.decorators import dag, task
from config.database import engine  # import centralisé
from datetime import datetime
from src.ingestion.velib_stations import fetch_velib_stations
from src.transformations.velib_stations import process_velib_status
from src.loaders.loader import load_to_postgres

@dag(schedule="@5min", start_date=datetime(2026,3,16), catchup=False)
def velib_status_pipeline():

    @task
    def extract():
        return fetch_velib_stations()

    @task
    def transform(raw_data):
        return process_velib_status(raw_data)

    @task
    def load_to_db(cleaned_data):
        load_to_postgres(cleaned_data, "station_status", engine)

    extractedDatas = extract()
    cleanedDatas = transform(extractedDatas)
    load_to_db(cleanedDatas)

pipeline = velib_status_pipeline()