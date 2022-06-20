from django.urls import path

from .views import new_event_view


urlpatterns = [
    path("create_event", new_event_view, name="create_event"),
]
