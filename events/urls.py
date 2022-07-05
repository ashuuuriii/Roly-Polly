from django.urls import path

from .views import new_event_view, NewEventSuccessView, EventVoteView


urlpatterns = [
    path("vote/<uuid:uuid_slug>", EventVoteView.as_view(), name="vote"),
    path("success/<uuid:uuid_slug>", NewEventSuccessView.as_view(), name='success'),
    path("create_event", new_event_view, name="create_event"),
]
