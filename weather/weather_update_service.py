import json
from datetime import datetime

from .models import Weather, WeatherStation
from weather.weather_service import get_weather


def update_weather():
    """ looks through all weather station objects, queries and saves/updates 
        the relevant forecast for each location.

        This method should be run asynchronously on a schedule as to not interfere with the web application.

    """
    queryset = WeatherStation.objects.all()

    for station in queryset:
        
        weather = get_weather(station.weather_station, station.grid_x, station.grid_y)
        for weather_period in weather:

            new_weather = {}
            new_weather['start_time'] = datetime.strptime(weather_period['startTime'],  "%Y-%m-%dT%H:%M:%S%z")
            new_weather['end_time'] = datetime.strptime(weather_period['endTime'],  "%Y-%m-%dT%H:%M:%S%z")
            new_weather['is_daytime'] = weather_period['isDaytime']
            new_weather['temperature'] = weather_period['temperature']
            new_weather['temperature_unit'] = weather_period['temperatureUnit']
            new_weather['wind_speed'] = weather_period['windSpeed']
            new_weather['wind_speed'] = weather_period['windDirection']
            new_weather['short_forecast'] = weather_period['shortForecast']
            new_weather['detailed_forecast'] = weather_period['detailedForecast']

            queryset = Weather.objects.filter(zip_code=station.zip_code, start_time=new_weather['start_time'])
            if queryset.count() > 0:
                # time period already exists
                quesryset[0].update(**new_weather)
            else:
                Weather.objects.create(**new_weather)

            # TODO log something here to indicate weather update failed

def schedule_notification():
    """
    """
    pass            