"""
Pages app view functions.

The module provides two simple views that render static pages.
"""
from django.shortcuts import render


def about(request):
    """Render the *About* page."""
    return render(request, "pages/about.html")


def rules(request):
    """Render the *Rules* page."""
    return render(request, "pages/rules.html")
