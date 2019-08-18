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

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=CustomUser)