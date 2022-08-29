from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class UserSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'user_settings.html'