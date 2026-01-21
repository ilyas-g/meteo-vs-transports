import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 48.8534,
	"longitude": 2.3488,
	"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "daylight_duration", "sunshine_duration", "rain_sum", "snowfall_sum", "showers_sum", "precipitation_sum", "precipitation_hours", "precipitation_probability_max", "wind_gusts_10m_max", "wind_speed_10m_max", "sunset", "sunrise"],
	"hourly": ["temperature_2m", "rain", "snowfall"],
	"models": "meteofrance_seamless",
	"current": ["temperature_2m", "is_day", "rain", "precipitation"],
	"timezone": "Europe/Berlin",
	"past_days": 92,
    "forecast_days": 4
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# Process current data. The order of variables needs to be the same as requested.
current = response.Current()
current_temperature_2m = current.Variables(0).Value()
current_is_day = current.Variables(1).Value()
current_rain = current.Variables(2).Value()
current_precipitation = current.Variables(3).Value()

print(f"\nCurrent time: {current.Time()}")
print(f"Current temperature_2m: {current_temperature_2m}")
print(f"Current is_day: {current_is_day}")
print(f"Current rain: {current_rain}")
print(f"Current precipitation: {current_precipitation}")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_rain = hourly.Variables(1).ValuesAsNumpy()
hourly_snowfall = hourly.Variables(2).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}

hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["rain"] = hourly_rain
hourly_data["snowfall"] = hourly_snowfall

print("okokokokok")
print(response)
print("okokokokok")
print(hourly)
print("okokokokok")

hourly_dataframe = pd.DataFrame(data = hourly_data)
hourly_dataframe.fillna(0, inplace=True)
print("\nHourly data\n", hourly_dataframe)

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_weather_code = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
daily_apparent_temperature_max = daily.Variables(3).ValuesAsNumpy()
daily_apparent_temperature_min = daily.Variables(4).ValuesAsNumpy()
daily_daylight_duration = daily.Variables(5).ValuesAsNumpy()
daily_sunshine_duration = daily.Variables(6).ValuesAsNumpy()
daily_rain_sum = daily.Variables(7).ValuesAsNumpy()
daily_snowfall_sum = daily.Variables(8).ValuesAsNumpy()
daily_showers_sum = daily.Variables(9).ValuesAsNumpy()
daily_precipitation_sum = daily.Variables(10).ValuesAsNumpy()
daily_precipitation_hours = daily.Variables(11).ValuesAsNumpy()
daily_precipitation_probability_max = daily.Variables(12).ValuesAsNumpy()
daily_wind_gusts_10m_max = daily.Variables(13).ValuesAsNumpy()
daily_wind_speed_10m_max = daily.Variables(14).ValuesAsNumpy()
daily_sunset = daily.Variables(15).ValuesInt64AsNumpy()
daily_sunrise = daily.Variables(16).ValuesInt64AsNumpy()

daily_data = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end =  pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}

daily_data["weather_code"] = daily_weather_code
daily_data["temperature_2m_max"] = daily_temperature_2m_max
daily_data["temperature_2m_min"] = daily_temperature_2m_min
daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
daily_data["daylight_duration"] = daily_daylight_duration
daily_data["sunshine_duration"] = daily_sunshine_duration
daily_data["rain_sum"] = daily_rain_sum
daily_data["snowfall_sum"] = daily_snowfall_sum
daily_data["showers_sum"] = daily_showers_sum
daily_data["precipitation_sum"] = daily_precipitation_sum
daily_data["precipitation_hours"] = daily_precipitation_hours
daily_data["precipitation_probability_max"] = daily_precipitation_probability_max
daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max
daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
daily_data["sunset"] = daily_sunset
daily_data["sunrise"] = daily_sunrise

daily_dataframe = pd.DataFrame(data = daily_data)
# daily_dataframe.fillna(0, inplace=True)
daily_dataframe = daily_dataframe.dropna()
daily_dataframe = daily_dataframe.sort_values("date").reset_index(drop=True)

# Il faut ensuite relancer la dataframe et voir si la valeur réelle n'a pas été rajoutée. Si c'est le cas, changez la valeur du NaN (donc 0 ici) 
# par la valeur réelle, pour ensuite mettre à jour la database.
print("\nDaily data\n", daily_dataframe)