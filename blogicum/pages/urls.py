"""
Pages app URL configuration.

This module defines the URL patterns for the `pages` application.
It maps static pages such as ``about`` and ``rules`` to their
respective view functions.

"""
from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("pages/about/", views.about, name="about"),
    path("pages/rules/", views.rules, name="rules"),
]
