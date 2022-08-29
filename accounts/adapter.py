from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse

from .tasks import send_email_async


class CustomAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        msg = self.render_mail(template_prefix, email, context)
        send_email_async.delay(msg)

    def get_login_redirect_url(self, request):
        return reverse('dashboard')
