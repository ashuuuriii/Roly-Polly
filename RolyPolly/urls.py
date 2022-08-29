from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from pages.views import handler_403, handler_404, handler_500

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include('allauth.urls')),
    path("accounts/", include('accounts.urls')),
    path("events/", include('events.urls')),
    path("", include("pages.urls")),
]
urlpatterns += staticfiles_urlpatterns()

handler403 = handler_403
handler404 = handler_404
handler500 = handler_500