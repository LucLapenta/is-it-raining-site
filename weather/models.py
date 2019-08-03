import json
import geopy
import requests
import pytz


from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Profile

class WeatherStation(models.Model):
    zip_code = models.CharField(max_length=5, null=True, unique=True)
    weather_station = models.CharField(max_length=3, null=True)
    timezone = models.CharField(default="America/New York", max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    grid_x = models.IntegerField()
    grid_y = models.IntegerField()

class Weather(models.Model):
    zip_code = models.CharField(max_length=5, null=True, unique=True)
    name = models.CharField(max_length=50, null=True)
    start_time=models.TimeField()
    end_time=models.TimeField()
    is_daytime=models.BooleanField(default=True)
    temperature=models.IntegerField()
    temperature_unit=models.CharField(max_length=5, default="F")
    wind_speed=models.CharField(max_length=10, default="0 mph")
    wind_direction=models.CharField(max_length=10, default="N")
    short_forecast=models.TextField()
    detailed_forecast=models.TextField()

@receiver(post_save, sender=Profile)
def create_weather_station(sender, **kwargs):
    profile = kwargs['instance']
    zip_code = profile.zip_code
    
    if len(WeatherStation.objects.filter(zip_code=zip_code)) == 0:
        geolocator = Nominatim(user_agent="is_it_raining_bot")
        location = geolocator.geocode(zip_code)
        latitude = location.latitude
        longitude = location.longitude

        tf = TimezoneFinder()
        tz = tf.timezone_at(lat=latitude, lng=longitude)
        timezone = pytz.timezone(tz)

        url = 'https://api.weather.gov/points/'+ str(latitude) + '%2C' + str(longitude)
        r = requests.get(url)

        location_data = json.loads(r.text)
        weather_station = location_data['properties']['cwa']
        grid_x = location_data['properties']['gridX']
        grid_y = location_data['properties']['gridY']
        WeatherStation.objects.create(zip_code=zip_code, latitude=latitude, longitude=longitude, timezone=timezone, weather_station=weather_station, grid_x=grid_x, grid_y=grid_y)    