from psycopg2.extras import execute_values

SQL_DAILY_UPSERT = """
INSERT INTO daily_weather (
    date, weather_code, temperature_2m_max, temperature_2m_min,
    apparent_temperature_max, apparent_temperature_min,
    rain_sum, snowfall_sum, showers_sum,
    precipitation_sum, precipitation_probability_max,
    wind_gusts_10m_max, wind_speed_10m_max
)
VALUES %s
ON CONFLICT (date) DO UPDATE SET
    weather_code = EXCLUDED.weather_code,
    temperature_2m_max = EXCLUDED.temperature_2m_max,
    temperature_2m_min = EXCLUDED.temperature_2m_min,
    apparent_temperature_max = EXCLUDED.apparent_temperature_max,
    apparent_temperature_min = EXCLUDED.apparent_temperature_min,
    rain_sum = EXCLUDED.rain_sum,
    snowfall_sum = EXCLUDED.snowfall_sum,
    showers_sum = EXCLUDED.showers_sum,
    precipitation_sum = EXCLUDED.precipitation_sum,
    precipitation_probability_max = EXCLUDED.precipitation_probability_max,
    wind_gusts_10m_max = EXCLUDED.wind_gusts_10m_max,
    wind_speed_10m_max = EXCLUDED.wind_speed_10m_max
"""

SQL_HOURLY_UPSERT = """
INSERT INTO hourly_weather (
    date, temperature_2m, relative_humidity_2m, dew_point_2m, apparent_temperature, 
    precipitation, rain, snowfall, weather_code
)
VALUES %s
ON CONFLICT (date) DO UPDATE SET
    weather_code = EXCLUDED.weather_code,
    temperature_2m = EXCLUDED.temperature_2m,
    relative_humidity_2m = EXCLUDED.relative_humidity_2m,
    dew_point_2m = EXCLUDED.dew_point_2m,
    apparent_temperature = EXCLUDED.apparent_temperature,
    precipitation = EXCLUDED.precipitation,
    rain = EXCLUDED.rain,
    snowfall = EXCLUDED.snowfall
"""


def upsert_daily(engine, daily_df):
    conn = engine.raw_connection()
    cursor = conn.cursor()
    try:
        data = [tuple(row) for row in daily_df.itertuples(index=False, name=None)]
        execute_values(cursor, SQL_DAILY_UPSERT, data)
        conn.commit()
        print("✓ Data daily weather fetched successfully!")
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def upsert_hourly(engine, hourly_df):
    conn = engine.raw_connection()
    cursor = conn.cursor()

    # Convertir les types numpy en types Python natifs
    hourly_df = hourly_df.astype({
        "temperature_2m": float,
        "rain": float,
        "snowfall": float,
    })

    try:
        execute_values(cursor, SQL_HOURLY_UPSERT, hourly_df.to_records(index=False))
        conn.commit()
        print("✓ Data hourly weather fetched successfully!")
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
