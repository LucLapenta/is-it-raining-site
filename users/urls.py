# users/urls.py
from django.urls import path
from .views import SignUpView, AlertListView, CreateAlertView, UpdateAlertView
from .models import Alert

from . import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', views.view_profile, name='profile'),
    path('alerts/', AlertListView.as_view(model=Alert), name='alerts'),
    path('alert/create/', CreateAlertView.as_view(model=Alert), name='alert-create'),
    path(r'^alert/update/(?P<alert_pk>\d+)/', UpdateAlertView.as_view(), name='edit_alert'),
    path('profile/edit/', views.edit_profile, name='edit_profile')
]