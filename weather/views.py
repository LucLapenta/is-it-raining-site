from django.shortcuts import render
from django.views.generic.detail import DetailView

from weather.models import Weather
# Create your views here.

class WeatherDetailView(DetailView):

    model = Weather
    template = 'weather_detail.html'
    slug_url_kwarg = 'zip_code'
    slug_field = 'zip_code'

    def get_object(self):
        zip_code = str(self.kwargs['zip_code'])
        test = Weather.objects.filter(zip_code=zip_code).order_by('-id')[0]
        return test



    