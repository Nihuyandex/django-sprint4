"""
Blog app view functions.

The module provides three primary views used by the blog
application:

* :func:`index` – renders a list of posts in reverse order.
* :func:`post_detail` – renders a single post identified by its
  integer ``id``.
* :func:`category_posts` – renders posts belonging to a particular
  category.  The actual filtering logic is omitted for brevity; the
  function simply passes the slug to the template.

The sample data defined below is intentionally minimal and
serves only for demonstration purposes.

"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.functions.datetime import Now
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.detail import DetailView

from .models import Category, Comment, Post, User


def _get_published_posts_with_meta():
    return (
        Post.objects.select_related("category", "location")
        .filter(Q(category__is_published=True))
        .filter(Q(is_published=True) & Q(pub_date__lte=Now()))
    )


class IndexListView(ListView):
    model = Post
    ordering = "pub_date"
    paginate_by = 10
    template_name = "blog/index.html"


class CreatePostView(CreateView, LoginRequiredMixin):
    model = Post
    fields = "__all__"
    template_name = "blog/create.html"
    success_url = reverse_lazy("blog:my_profile")


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"


class EditPostView(UpdateView):
    model = Post


class DeletePostView(DeleteView):
    model = Post


class CreateCommentView(CreateView, LoginRequiredMixin):
    model = Post
    fields = "__all__"
    # template_name = "blog/create.html"
    success_url = reverse_lazy("blog:my_profile")


class CommentDetailView(DetailView):
    model = Comment
    template_name = "blog/comment.html"


class EditCommentView(UpdateView):
    model = Comment


class DeleteCommentView(DeleteView):
    model = Comment


def category_posts(request, category_slug):
    """Render posts belonging to a particular category."""
    category = get_object_or_404(Category, slug=category_slug, is_published=True)

    posts_filtered = (
        _get_published_posts_with_meta().filter(category__pk=category.pk).all()
    )

    context = {"category": category_slug, "post_list": posts_filtered}
    return render(request, "blog/category.html", context)


@login_required
def redirect_to_my_profile(request):
    return redirect(f"/profile/{request.user.username}/")


def profile(request, profile_slug):
    profile = get_object_or_404(User, username=profile_slug)
    context = {"profile": profile}
    return render(request, "blog/profile.html", context)


@login_required
def edit_profile(request):
    context = {"profile": request.user}
    return render(request, "blog/user.html", context)
