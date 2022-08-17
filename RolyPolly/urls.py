from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include('allauth.urls')),
    path("events/", include('events.urls')),
    path("", include("pages.urls")),
]
urlpatterns += staticfiles_urlpatterns()
