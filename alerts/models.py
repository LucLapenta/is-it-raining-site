from django.db import models
from django.conf import settings

class Alert(models.Model):
    RAIN = 'Rain'
    SNOW = 'Snow'
    COLD = 'Cold'
    HEAT = 'Heat'
    WEATHER_CHOICES = [
        (RAIN, 'Rain'),
        (SNOW, 'Snow'),
        (COLD, 'Cold'),
        (HEAT, 'Heat'),
    ]

    DAILY = 24
    TWICE_DAILY = 12
    THREE_TIMES_DAILY = 8
    INTERVAL_CHOICES = [
        (DAILY, 24),
        (TWICE_DAILY, 12),
        (THREE_TIMES_DAILY, 8),
    ]
    
    weather_type = models.CharField(max_length=6, choices=WEATHER_CHOICES, default=RAIN)
    interval = models.IntegerField(choices=INTERVAL_CHOICES, default=DAILY)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    alert_time = models.TimeField(default='05:00 PM')