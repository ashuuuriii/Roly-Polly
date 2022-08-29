from django.views.generic import TemplateView
from django.conf import settings
from django.http import FileResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from django.shortcuts import render


@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)  # one day
def favicon(request):
    file = (settings.BASE_DIR / "static/media/favicon" / "favicon.ico").open("rb")
    return FileResponse(file)


class HomePageView(TemplateView):
    template_name = "index.html"


class AboutView(TemplateView):
    template_name = "about.html"


class FaqView(TemplateView):
    template_name = "faq.html"

def handler_404(request, exception):
    return render(request, 'error_pages/404.html', status=404)

def handler_403(request, exception):
    return render(request, 'error_pages/403.html', status=403)

def handler_500(request):
    return render(request, 'error_pages/500.html', status=500)