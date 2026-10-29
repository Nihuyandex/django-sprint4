"""Blog forms."""

from django.forms import DateTimeInput, ModelForm

from .models import Comment, Post, User


class PostForm(ModelForm):
    """Form for creating and editing posts."""

    class Meta:
        """Meta."""

        model = Post
        fields = ("title", "text", "pub_date", "location", "category", "image")
        widgets = {
            "pub_date": DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
        }


class CommentForm(ModelForm):
    """Form for creating and editing comments."""

    class Meta:
        """Meta."""

        model = Comment
        fields = ("text",)


class ProfileForm(ModelForm):
    """Form for editing the current user's profile."""

    class Meta:
        """Meta."""

        model = User
        fields = ("first_name", "last_name", "username", "email")
