from airflow.decorators import dag, task
from config.database import engine  # import centralisé
from datetime import datetime
from src.ingestion.open_meteo import fetch_weather_raw
from src.transformations.open_meteo import process_hourly, process_daily
from src.loaders.loader import load_to_postgres

@dag(schedule="@daily", start_date=datetime(2026,3,16), catchup=False)
def weather_pipeline():

    @task
    def extract():
        return fetch_weather_raw()

    @task
    def transform(response):
        hourly = process_hourly(response)
        daily = process_daily(response)
        return {"hourly": hourly, "daily": daily}


    @task
    def load_to_db(cleaned_data):
        load_to_postgres(cleaned_data["hourly"], "hourly_weather", engine)
        load_to_postgres(cleaned_data["daily"], "daily_weather", engine)

    extractedDatas = extract()
    cleanedDatas = transform(extractedDatas)
    load_to_db(cleanedDatas)

pipeline = weather_pipeline()