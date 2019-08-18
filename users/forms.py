from django import forms
from django.forms import ModelForm, TimeInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile
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
        fields = ('email', 'first_name', 'last_name')
    
class UserProfileForm(UserChangeForm):
    password = None
    
    class Meta:
        model = Profile
        fields = ('phone_number', 'zip_code', 'cell_phone_provider')


       
    
   

        