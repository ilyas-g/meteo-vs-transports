from api.open_meteo import fetch_hourly_temperature
from services.weather_processing import prepare_weather_dataframe
from db.postgres import get_engine
from db.weather_repository import insert_weather

def main():
    df = fetch_hourly_temperature(
        latitude=48.8534,
        longitude=2.3488,
        city="Paris"
    )

    df = prepare_weather_dataframe(df)

    engine = get_engine()
    insert_weather(df, engine)

if __name__ == "__main__":
    main()


# pyenv activate meteo-env