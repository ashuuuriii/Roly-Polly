from django.urls import path

from .views import (
    new_event_view,
    NewEventSuccessView,
    EventVoteView,
    UnlockVoteView,
    ChoiceAddView,
    DashboardView,
    EventDetailView,
    EventDeleteView,
    EventEditView,
)


urlpatterns = [
    path("edit/<uuid:uuid_slug>", EventEditView.as_view(), name="edit"),
    path("delete/<uuid:uuid_slug>", EventDeleteView.as_view(), name="delete"),
    path("<uuid:uuid_slug>", EventDetailView.as_view(), name="event"),
    path("dashboard", DashboardView.as_view(), name="dashboard"),
    path("unlock/<uuid:uuid_slug>", UnlockVoteView.as_view(), name="unlock"),
    path("vote/<uuid:uuid_slug>", EventVoteView.as_view(), name="vote"),
    path("add/<uuid:uuid_slug>", ChoiceAddView.as_view(), name="add"),
    path("success/<uuid:uuid_slug>", NewEventSuccessView.as_view(), name="success"),
    path("create_event", new_event_view, name="create_event"),
]
