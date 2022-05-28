from django.views.generic import TemplateView
from django.conf import settings
from django.http import FileResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET


@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)  # one day
def favicon(request):
    file = (settings.BASE_DIR / "media/favicon" / "favicon.ico").open("rb")
    return FileResponse(file)


class HomePageView(TemplateView):
    template_name = "index.html"


class AboutView(TemplateView):
    template_name = "about.html"


class FaqView(TemplateView):
    template_name = "faq.html"
