from django import forms
from django.forms import ModelForm, TimeInput

from .models import Alert

class AlertModelForm(ModelForm):
    
    #alert_time = forms.TimeField(input_formats = ( '%I:%M %p', ))

    class Meta:
        model = Alert
        exclude = ['user']
        """widgets = {
            'alert_time': TimeInput(format='%I:%M %p'),
        }"""
