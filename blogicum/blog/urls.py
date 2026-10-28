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
    path("", views.IndexListView.as_view(), name="index"),
    path("profile/", views.redirect_to_my_profile, name="my_profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/<slug:profile_slug>/", views.profile, name="profile"),
    path("posts/<int:post_id>/", views.PostDetailView.as_view(), name="post_detail"),
    path("posts/create/", views.CreatePostView.as_view(), name="create_post"),
    path("category/<slug:category_slug>/", views.category_posts, name="category_posts"),
]
