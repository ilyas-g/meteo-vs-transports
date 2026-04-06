\connect mvst;

CREATE TABLE daily_weather (
    date DATE PRIMARY KEY,
    weather_code INT NOT NULL,
    temperature_2m_max FLOAT NOT NULL,
    temperature_2m_min FLOAT NOT NULL,
    apparent_temperature_min FLOAT NOT NULL,
    apparent_temperature_max FLOAT NOT NULL,
    precipitation_probability_max FLOAT NOT NULL,
    wind_speed_10m_max FLOAT NOT NULL,
    wind_gusts_10m_max FLOAT NOT NULL,
    precipitation_sum FLOAT NOT NULL,
    snowfall_sum FLOAT NOT NULL,
    showers_sum FLOAT NOT NULL,
    rain_sum FLOAT NOT NULL
);

CREATE TABLE hourly_weather (
    date TIMESTAMPTZ PRIMARY KEY,
    temperature_2m FLOAT NOT NULL,
    relative_humidity_2m FLOAT NOT NULL,
    dew_point_2m FLOAT NOT NULL,
    apparent_temperature FLOAT NOT NULL,
    precipitation FLOAT NOT NULL,
    rain FLOAT NOT NULL,
    snowfall FLOAT NOT NULL,
    weather_code INT NOT NULL
);

CREATE TABLE station_information (
    station_id BIGINT PRIMARY KEY,
    station_code VARCHAR(10),
    name VARCHAR(255) NOT NULL,
    lat FLOAT NOT NULL,
    lon FLOAT NOT NULL,
    capacity INT NOT NULL CHECK (capacity >= 0)
);

CREATE TABLE station_status (
    station_id BIGINT NOT NULL,
    date DATE NOT NULL,
    num_bikes_available INT NOT NULL CHECK (num_bikes_available >= 0),
    num_docks_available INT NOT NULL CHECK (num_docks_available >= 0),
    is_installed BOOLEAN NOT NULL DEFAULT true,
    is_returning BOOLEAN NOT NULL DEFAULT true,
    is_renting BOOLEAN NOT NULL DEFAULT true,
    last_reported TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (station_id, date),
    FOREIGN KEY (station_id) REFERENCES station_information(station_id) ON DELETE CASCADE
);

CREATE INDEX idx_station_date ON station_status(station_id, date);
CREATE INDEX idx_station_status_date ON station_status(date);
CREATE INDEX idx_daily_weather_date ON daily_weather(date);
CREATE INDEX idx_hourly_weather_date ON hourly_weather(date);