from django.views.generic import TemplateView
from django.urls import reverse
from django.shortcuts import render

from users.models import CustomUser, Profile
from weather.models import Weather

from weather.views import WeatherDetailView

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # get zip code from user profile
        if self.request.user.is_authenticated:
            zip_code = self.request.user.profile.zip_code
            context['latest_weather'] = Weather.objects.filter(zip_code=zip_code).order_by('-id')[0]

        return context