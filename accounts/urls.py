from django.urls import path
from .views import UserSettingsView

urlpatterns = [
    path('user_settings', UserSettingsView.as_view(), name='user_settings'),
]