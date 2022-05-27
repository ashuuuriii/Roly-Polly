from django.urls import path
from .views import HomePageView, AboutView, FaqView


urlpatterns = [
    path("about", AboutView.as_view(), name="about"),
    path("faq", FaqView.as_view(), name="faq"),
    path("", HomePageView.as_view(), name="home"),
]
