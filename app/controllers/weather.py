import requests
import openmeteo_requests
import requests_cache
from retry_requests import retry

cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

## getting current latitude and longitude
def get_lat_lng():
    url = "https://ipinfo.io/json"
    response = requests.get(url)
    data = response.json()
    lat_lng = data["loc"].split(",")
    latitude = float(lat_lng[0])
    longitude = float(lat_lng[1])
    return latitude, longitude

## getting info weather based on the latitude and longitude
def get_current_weather():
    latitude, longitude = get_lat_lng()
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m"
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()
    current_temperature = current.Variables(0).Value()
    return current_temperature

def get_pokemon_type_by_temperature():
    temperature = get_current_weather()
    if temperature >= 30:
        return "fire"
    elif temperature >= 20:
        return "rock"
    elif temperature >= 10:
        return "normal"
    elif temperature >= 0:
        return "water"
    else:
        return "ice"

