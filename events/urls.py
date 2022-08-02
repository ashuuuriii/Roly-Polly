from django.urls import path

from .views import (
    new_event_view,
    NewEventSuccessView,
    EventVoteView,
    UnlockVoteView,
    ChoiceAddView,
    DashboardView,
)


urlpatterns = [
    path("dashboard", DashboardView.as_view(), name="dashboard"),
    path("unlock/<uuid:uuid_slug>", UnlockVoteView.as_view(), name="unlock"),
    path("vote/<uuid:uuid_slug>", EventVoteView.as_view(), name="vote"),
    path("add/<uuid:uuid_slug>", ChoiceAddView.as_view(), name="add"),
    path("success/<uuid:uuid_slug>", NewEventSuccessView.as_view(), name="success"),
    path("create_event", new_event_view, name="create_event"),
]
