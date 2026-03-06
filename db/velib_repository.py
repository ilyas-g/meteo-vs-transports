from psycopg2.extras import execute_values

SQL_STATIONS_UPSERT = """
INSERT INTO station_status(
    station_id, date, num_bikes_available, num_docks_available, 
    is_installed, is_returning, is_renting, last_reported
)
VALUES %s
ON CONFLICT (station_id, date) DO UPDATE SET
    station_id = EXCLUDED.station_id,
    date = EXCLUDED.date,
    num_bikes_available = EXCLUDED.num_bikes_available,
    num_docks_available = EXCLUDED.num_docks_available,
    is_installed = EXCLUDED.is_installed,
    is_renting = EXCLUDED.is_renting,
    is_returning = EXCLUDED.is_returning,
    last_reported = EXCLUDED.last_reported
"""

SQL_INFORMATIONS_UPSERT = """
INSERT INTO station_information (
    station_id, station_code, name, lat, lon, capacity
)
VALUES %s
ON CONFLICT (station_id) DO UPDATE SET
    station_id = EXCLUDED.station_id,
    station_code = EXCLUDED.station_code,
    name = EXCLUDED.name,
    lat = EXCLUDED.lat,
    lon = EXCLUDED.lon,
    capacity = EXCLUDED.capacity
"""

def upsert_stations(engine, stations_df):
    conn = engine.raw_connection()
    cursor = conn.cursor()
    try:
        data = [tuple(row) for row in stations_df.itertuples(index=False, name=None)]
        execute_values(cursor, SQL_STATIONS_UPSERT, data)
        conn.commit()
        print("✓ Data stations fetched successfully!")
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

def upsert_informations(engine, informations_df):
    conn = engine.raw_connection()
    cursor = conn.cursor()
    try:
        data = [tuple(row) for row in informations_df.itertuples(index=False, name=None)]
        execute_values(cursor, SQL_INFORMATIONS_UPSERT, data)
        conn.commit()
        print("✓ Data informations fetched successfully!")
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
