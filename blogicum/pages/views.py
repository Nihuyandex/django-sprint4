"""
Pages app view functions.

The module provides two simple views that render static pages.
"""

from django.views.generic import TemplateView


class About(TemplateView):
    """Render the *About* page."""

    template_name = "pages/about.html"


class Rules(TemplateView):
    """Render the *Rules* page."""

    template_name = "pages/rules.html"
