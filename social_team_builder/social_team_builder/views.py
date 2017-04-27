from django.views.generic import TemplateView


class Home(TemplateView):
    """Home page."""
    template_name = "index.html"
