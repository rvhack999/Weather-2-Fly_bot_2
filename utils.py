""" различные функции. """
import openmeteo_requests
import requests_cache
from datetime import datetime, timedelta
from retry_requests import retry

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


def get_weather(lat, lon):
    """ Функция получения списка параметров погоды """

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": float(lat),
        "longitude": float(lon),
        "hourly": ["temperature_2m", "precipitation", "wind_speed_10m", "wind_speed_80m", "wind_speed_120m",
                   "wind_speed_180m", "wind_gusts_10m", "temperature_80m", "temperature_120m", "temperature_180m"],
        "wind_speed_unit": "ms",
        "forecast_days": 1,
        # "timezone": 'GMT'
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    hourly = response.Hourly()
    hourly_temperature_2m = [calc_cof_t(i) for i in hourly.Variables(0).ValuesAsNumpy()]
    hourly_wind_speed_10m = [calc_cof_w(i) for i in hourly.Variables(2).ValuesAsNumpy()]
    hourly_wind_speed_80m = [calc_cof_w(i) for i in hourly.Variables(3).ValuesAsNumpy()]
    hourly_wind_speed_120m = [calc_cof_w(i) for i in hourly.Variables(4).ValuesAsNumpy()]
    hourly_wind_speed_180m = [calc_cof_w(i) for i in hourly.Variables(5).ValuesAsNumpy()]
    hourly_wind_gusts_10m = [calc_cof_w(i) for i in hourly.Variables(6).ValuesAsNumpy()]
    hourly_temperature_80m = [calc_cof_t(i) for i in hourly.Variables(7).ValuesAsNumpy()]
    hourly_temperature_120m = [calc_cof_t(i) for i in hourly.Variables(8).ValuesAsNumpy()]
    hourly_temperature_180m = [calc_cof_t(i) for i in hourly.Variables(9).ValuesAsNumpy()]

    hourly_date = [(datetime.now() + timedelta(hours=i)).strftime("%Y-%m-%d %H:%M:%S") for i in range(25)]
    hourly_data = list(zip(
        hourly_date,
        hourly_temperature_2m,
        hourly_temperature_80m,
        hourly_temperature_120m,
        hourly_temperature_180m,
        hourly_wind_gusts_10m,
        hourly_wind_speed_10m,
        hourly_wind_speed_80m,
        hourly_wind_speed_120m,
        hourly_wind_speed_180m,
    ))

    out = {i[0]: round(sum(i[1:]) / len(i[1:]), 2) for i in hourly_data if 0 not in i if sum(i[1:]) / len(i[1:]) > 0.7}

    return out


def calc_cof_t(t):
    if t < -30:
        return 0
    elif -30 <= t < -20:
        return 0.25
    elif -20 <= t < -10:
        return 0.5
    elif -10 <= t < 0:
        return 0.75
    elif t > 0:
        return 1


def calc_cof_w(w):
    if 5 <= w:
        return 0
    elif 3 <= w < 5:
        return 0.25
    elif 2 <= w < 3:
        return 0.5
    elif 1 <= w < 2:
        return 0.75
    elif w < 1:
        return 1

