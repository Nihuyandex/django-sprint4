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
    path("category/<slug:category_slug>/", views.category_posts, name="category_posts"),
    path("posts/create/", views.CreatePostView.as_view(), name="create_post"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("posts/<int:pk>/edit/", views.EditPostView.as_view(), name="edit_post"),
    path("posts/<int:pk>/delete/", views.DeletePostView.as_view(), name="delete_post"),
    path(
        "comments/<int:pk>/", views.CommentDetailView.as_view(), name="comment_detail"
    ),
    path(
        "comments/<int:post>/create/",
        views.CreateCommentView.as_view(),
        name="add_comment",
    ),
    path(
        "comments/<int:pk>/edit/", views.EditCommentView.as_view(), name="edit_comment"
    ),
    path(
        "comments/<int:pk>/delete/",
        views.DeleteCommentView.as_view(),
        name="delete_comment",
    ),
]
