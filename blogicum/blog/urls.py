"""
Blog app URL configuration.

This module defines the URL patterns for the `blog` application. It maps
URLs to view functions that render the blog index, individual post
details, and posts filtered by category.

"""
from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("posts/<int:post_id>/", views.post_detail,
         name="post_detail"),
    path("category/<slug:category_slug>/",
         views.category_posts, name="category_posts"),
]
