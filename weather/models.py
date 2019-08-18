from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Profile
from weather.weather_service import get_weather_location

class WeatherStation(models.Model):
    zip_code = models.CharField(max_length=5, null=True, unique=True)
    weather_station = models.CharField(max_length=3, null=True)
    timezone = models.CharField(default="America/New York", max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    grid_x = models.IntegerField()
    grid_y = models.IntegerField()

    def get_forecast_url(self):
        return 'https://api.weather.gov/gridpoints/'+ str(self.weather_station) + '/' + str(self.grid_x) + ',' + str(self.grid_y) + '/forecast'


class Weather(models.Model):
    """ model to store the data recieved from the weather.gov API. 

        typically data will be returned from the API in 8 hour increments.
        Each model will contain data for the corresponding time window for a given zip code
    """
    zip_code = models.CharField(max_length=5, null=True)
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

    #class Meta():
        #unique_together = ('zip_code', 'start_time')

    def get_latest(self, zip_code):
        return Weather.objects.filter(zip_code=zip_code).orderby('-id')[0]

@receiver(post_save, sender=Profile)
def create_weather_station(sender, **kwargs):
    profile = kwargs['instance']
    zip_code = profile.zip_code
    
    if len(WeatherStation.objects.filter(zip_code=zip_code)) == 0:
        
        new_station = get_weather_location(zip_code)
        WeatherStation.objects.create(**new_station)    