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

from django.db.models import Q
from django.db.models.functions.datetime import Now
from django.shortcuts import get_object_or_404, render

from .models import Category, Post


def _get_published_posts_with_meta():
    return (
        Post.objects.select_related("category", "location")
        .filter(Q(category__is_published=True))
        .filter(Q(is_published=True) & Q(pub_date__lte=Now()))
    )


def index(request):
    """Render the blog index page.

    The view supplies a context containing the list of posts in
    reverse order (newest first) and renders the ``blog/index.html``
    template.
    """
    posts = _get_published_posts_with_meta()[:5]

    context = {"post_list": posts}

    return render(request, "blog/index.html", context)


def post_detail(request, post_id):
    """Render a detail page for a single post."""
    post_filtered = get_object_or_404(
        _get_published_posts_with_meta(),
        pk=post_id
    )
    context = {"post": post_filtered}
    return render(request, "blog/detail.html", context)


def category_posts(request, category_slug):
    """Render posts belonging to a particular category."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    posts_filtered = (
        _get_published_posts_with_meta().filter(category__pk=category.pk).all()
    )

    context = {"category": category_slug, "post_list": posts_filtered}
    return render(request, "blog/category.html", context)
