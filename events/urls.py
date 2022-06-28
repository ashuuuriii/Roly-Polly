from django.urls import path

from .views import new_event_view, NewEventSuccessView


urlpatterns = [
    path("success/<uuid:uuid_slug>", NewEventSuccessView.as_view(), name='success'),
    path("create_event", new_event_view, name="create_event"),
]
