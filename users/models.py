from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    phone_number = PhoneNumberField(null=True, blank=False)
    zip_code = models.CharField(max_length=5, null=True)
    ATT = '@mms.att.net'
    TMOBILE = '@tmomail.net'
    VERIZON = '@vtext.com'
    SPRINT = '@page.nextel.com'
    CELL_PHONE_CARRIER_CHOICES = [
        (ATT, 'AT&T'),
        (TMOBILE, 'T-Mobile'),
        (VERIZON, 'Verizon'),
        (SPRINT, 'Sprint'),
    ]

    cell_phone_provider = models.CharField(max_length=15, choices=CELL_PHONE_CARRIER_CHOICES, default=ATT)

    def __str__(self):
        return self.user.username

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

    DAILY = 'Daily'
    WEEKLY = 'Weekly'
    INTERVAL_CHOICES = [
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
    ]
    
    weather_type = models.CharField(max_length=6, choices=WEATHER_CHOICES, default=RAIN)
    interval = models.CharField(max_length=6, choices=INTERVAL_CHOICES, default=DAILY)
    search_length = models.IntegerField(default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    alert_time = models.TimeField(default='05:00 PM')


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=CustomUser)