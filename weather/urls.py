# weather/urls.py
from django.urls import path
from .views import WeatherDetailView
from .models import Weather


urlpatterns = [
    path('<slug:zip_code>', WeatherDetailView.as_view(), name='weather'),
]