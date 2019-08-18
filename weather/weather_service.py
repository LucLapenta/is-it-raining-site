import json
import geopy
import requests
import pytz

from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

request_headers = {
    'User-Agent': 'is_it_raining_bot_v1'
}

def get_weather_location(zip_code:str):
    """ function to make API call to weather.gov api to get the weather station for a given zip code.
    """
    location_dict = {}

    try:
        # Find approximate latitude and longitude based on zip code.
        geolocator = Nominatim(user_agent="is_it_raining_bot")
        location = geolocator.geocode(zip_code)

        latitude = location.latitude
        longitude = location.longitude

        location_dict['latitude'] = location.latitude
        location_dict['longitude'] = location.longitude

        # Find timezone of given zip code, not needed now, but should store for later.
        tf = TimezoneFinder()
        tz = tf.timezone_at(lat=latitude, lng=longitude)
        location_dict['timezone'] = pytz.timezone(tz)

        # Make API call to api.weather.gov to find the closest weather station to the lat/long of the zip code.
        url = 'https://api.weather.gov/points/'+ str(latitude) + '%2C' + str(longitude)
        r = requests.get(url, headers=request_headers)

        location_data = json.loads(r.text)

        # Save weather station code name, and grid parameters for future API calls
        location_dict['weather_station'] = location_data['properties']['cwa']
        location_dict['grid_x'] = location_data['properties']['gridX']
        location_dict['grid_y'] = location_data['properties']['gridY']

        return location_dict

    except Exception:
        # TODO add improved error handling (404 response, 200 but invalid data)
        return {}

def get_weather(weather_station:str, grid_x:int, grid_y:int):
    """ Gets the current forecast for a given weather station/area. 

        Args:
            weather_station: 
                Three letter abbreviation for the relevant weather station. 
                ex. BOX -> Boston, MA
            
            grid_x: 
                might be relative distance X from weather station? parameter is collected
                from get_weather_location() api call
            
            grid_y:
                might be relative distance Y from weather station? parameter is collected
                from get_weather_location() api call

        Returns:
            weather_data:
                json formatted array of weather data. Data is returned as an array of 8 hour
                weather periods, which periods are relevant depends on when the data is queried, 
                and how far into the future we should look.
    """
    try:
        base_url = 'https://api.weather.gov/gridpoints/'
        url = base_url + str(weather_station) + '/'
        url += str(grid_x) + ',' + str(grid_y) + '/forecast'

        r = requests.get(url, headers=request_headers)
        weather_data = json.loads(r.text)

        return weather_data['properties']['periods']

    except Exception:
        # TODO add improved error handling (404 response, 200 but invalid data)
        return {}