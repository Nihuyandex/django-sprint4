"""
Pages app views.

Static pages are rendered with CBVs; error pages use custom templates.
"""

from django.shortcuts import render
from django.views.generic import TemplateView


class About(TemplateView):
    """Render the *About* page."""

    template_name = "pages/about.html"


class Rules(TemplateView):
    """Render the *Rules* page."""

    template_name = "pages/rules.html"


def page_not_found(request, exception):
    """Render the 404 error page."""
    return render(request, "pages/404.html", status=404)


def csrf_failure(request, reason=""):
    """Render the 403 page for a failed CSRF check."""
    return render(request, "pages/403csrf.html", status=403)


def server_error(request):
    """Render the 500 error page."""
    return render(request, "pages/500.html", status=500)
