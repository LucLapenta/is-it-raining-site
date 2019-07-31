from django import forms
from django.forms import ModelForm, TimeInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile, Alert
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        del self.fields['password']

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')
    
class UserProfileForm(UserChangeForm):

    class Meta:
        model = Profile
        fields = ('phone_number', 'zip_code', 'cell_phone_provider')

class AlertModelForm(ModelForm):
    
    #alert_time = forms.TimeField(input_formats = ( '%I:%M %p', ))

    class Meta:
        model = Alert
        exclude = ['user']
        """widgets = {
            'alert_time': TimeInput(format='%I:%M %p'),
        }"""
       
    
   

        