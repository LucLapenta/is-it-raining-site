from django.urls import include, path

from .models import Alert
from .views import AlertListView, CreateAlertView, UpdateAlertView, DeleteAlertView


urlpatterns = [
    path('all/', AlertListView.as_view(model=Alert), name='alerts'),
    path('create/', CreateAlertView.as_view(model=Alert), name='alert-create'),
    path('<int:pk>/update', UpdateAlertView.as_view(), name='edit_alert'),
    path('<int:pk>/delete', DeleteAlertView.as_view(), name='delete_alert'),
]
