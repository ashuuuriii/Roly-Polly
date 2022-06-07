from django.urls import path

from .views import NewEventFormView


urlpatterns = [
    path("create_new", NewEventFormView.as_view(), name="create_event"),
]
