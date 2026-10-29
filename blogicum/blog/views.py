"""Blog app views."""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import CommentForm, PostForm, ProfileForm
from .models import Category, Comment, Post, User

POSTS_PER_PAGE = 10


def get_posts(posts=Post.objects, published_only=True, with_comments=True):
    """Return posts with related objects, optionally filtered and annotated.

    ``published_only`` keeps only posts visible to everyone: published,
    in a published category and with a publication date in the past.
    ``with_comments`` adds a ``comment_count`` annotation.
    """
    posts = posts.select_related("author", "category", "location")
    if published_only:
        posts = posts.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
        )
    if with_comments:
        posts = posts.annotate(comment_count=Count("comments")).order_by(
            *Post._meta.ordering
        )
    return posts


def paginate(request, posts):
    """Return the requested page of ``posts``."""
    return Paginator(posts, POSTS_PER_PAGE).get_page(request.GET.get("page"))


def get_visible_post(request, post_id):
    """Return a post the current user is allowed to see, or raise 404.

    The author sees their post regardless of its publication status.
    """
    post = get_object_or_404(
        get_posts(published_only=False, with_comments=False), pk=post_id
    )
    if post.author != request.user:
        post = get_object_or_404(get_posts(with_comments=False), pk=post_id)
    return post


def index(request):
    """Render the feed of published posts."""
    return render(
        request,
        "blog/index.html",
        {"page_obj": paginate(request, get_posts())},
    )


def category_posts(request, category_slug):
    """Render published posts of a published category."""
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )
    return render(
        request,
        "blog/category.html",
        {
            "category": category,
            "page_obj": paginate(request, get_posts(category.post_set)),
        },
    )


def profile(request, username):
    """Render the user's page; the owner also sees unpublished posts."""
    author = get_object_or_404(User, username=username)
    posts = get_posts(
        author.post_set, published_only=request.user != author
    )
    return render(
        request,
        "blog/profile.html",
        {"profile": author, "page_obj": paginate(request, posts)},
    )


def post_detail(request, post_id):
    """Render a post with its comments and a comment form."""
    post = get_visible_post(request, post_id)
    return render(
        request,
        "blog/detail.html",
        {
            "post": post,
            "form": CommentForm(),
            "comments": post.comments.select_related("author"),
        },
    )


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Edit the current user's profile."""

    form_class = ProfileForm
    template_name = "blog/user.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse("blog:profile", args=(self.request.user.username,))


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a post on behalf of the current user."""

    form_class = PostForm
    template_name = "blog/create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:profile", args=(self.request.user.username,))


class AuthorRequiredMixin:
    """Let only the object's author proceed; redirect others to the post."""

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect("blog:post_detail", self.kwargs["post_id"])
        return super().dispatch(request, *args, **kwargs)


class PostMixin(AuthorRequiredMixin):
    """Common settings for post editing and deletion."""

    model = Post
    template_name = "blog/create.html"
    pk_url_kwarg = "post_id"


class PostUpdateView(PostMixin, UpdateView):
    """Edit a post."""

    form_class = PostForm

    def get_success_url(self):
        return reverse("blog:post_detail", args=(self.object.pk,))


class PostDeleteView(PostMixin, DeleteView):
    """Delete a post after confirmation."""

    def get_context_data(self, **kwargs):
        # create.html renders the post from ``form.instance``.
        return super().get_context_data(
            form=PostForm(instance=self.object), **kwargs
        )

    def get_success_url(self):
        return reverse("blog:profile", args=(self.request.user.username,))


@login_required
@require_POST
def add_comment(request, post_id):
    """Add a comment to a post visible to the current user."""
    post = get_visible_post(request, post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect("blog:post_detail", post_id)


class CommentMixin(AuthorRequiredMixin):
    """Common settings for comment editing and deletion."""

    model = Comment
    template_name = "blog/comment.html"
    pk_url_kwarg = "comment_id"

    def get_queryset(self):
        return super().get_queryset().filter(post_id=self.kwargs["post_id"])

    def get_success_url(self):
        return reverse("blog:post_detail", args=(self.kwargs["post_id"],))


class CommentUpdateView(CommentMixin, UpdateView):
    """Edit a comment."""

    form_class = CommentForm


class CommentDeleteView(CommentMixin, DeleteView):
    """Delete a comment after confirmation."""
