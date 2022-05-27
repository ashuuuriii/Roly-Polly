from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "index.html"


class AboutView(TemplateView):
    template_name = "about.html"


class FaqView(TemplateView):
    template_name = "faq.html"
