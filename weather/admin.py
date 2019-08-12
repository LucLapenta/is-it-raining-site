from django.contrib import admin

from .models import WeatherStation, Weather

# Register your models here.
admin.site.register(WeatherStation)
admin.site.register(Weather)