"""Blog models."""

from django.contrib.auth import get_user_model
from django.db.models import Model
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import (
    BooleanField,
    CharField,
    DateTimeField,
    SlugField,
    TextField,
)
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey

User = get_user_model()


class PublishedModel(Model):
    """BaseModel for all models in this app."""

    class Meta:
        """Meta."""

        abstract = True

    is_published = BooleanField(
        verbose_name="Опубликовано",
        default=True,
        help_text="Снимите галочку, чтобы скрыть публикацию.",
    )
    created_at = DateTimeField(verbose_name="Добавлено", auto_now_add=True)


class Category(PublishedModel):
    """Category model."""

    title = CharField(verbose_name="Заголовок", max_length=256)
    description = TextField(verbose_name="Описание")
    slug = SlugField(
        verbose_name="Идентификатор",
        unique=True,
        help_text=(
            "Идентификатор страницы для URL; разрешены "
            "символы латиницы, цифры, дефис и подчёркивание."
        ),
    )
    def __str__(self):
        return self.title

    class Meta:
        """Meta."""

        verbose_name = "категория"
        verbose_name_plural = "Категории"


class Location(PublishedModel):
    """Location model."""

    name = CharField(verbose_name="Название места", max_length=256)
    def __str__(self):
        return self.name

    class Meta:
        """Meta."""

        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"


class Post(PublishedModel):
    """Post model."""

    title = CharField(verbose_name="Заголовок", max_length=256)
    text = TextField(verbose_name="Текст")
    pub_date = DateTimeField(
        verbose_name="Дата и время публикации",
        help_text=(
            "Если установить дату и время в будущем — "
            "можно делать отложенные публикации."
        ),
    )
    author = ForeignKey(
        verbose_name="Автор публикации",
        to=User, on_delete=CASCADE
    )
    location = ForeignKey(
        verbose_name="Местоположение",
        to=Location,
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )
    category = ForeignKey(
        verbose_name="Категория",
        to=Category,
        on_delete=SET_NULL,
        null=True,
        blank=False,
    )
    image = ImageField(
        verbose_name="Изображение"
    )

    def __str__(self):
        return f"{self.author.username}-{self.title}"

    class Meta:
        """Meta."""

        verbose_name = "публикация"
        verbose_name_plural = "Публикации"

class Comment(PublishedModel):
    """Comment model"""
    text = TextField(verbose_name="Текст")

    author = ForeignKey(
        verbose_name="Автор комментария",
        to=User, on_delete=CASCADE
    )
    post = ForeignKey(
        verbose_name="Пост к которому относится комментарий",
        to=Post, on_delete=CASCADE
    )
    def __str__(self):
        return f"{self.post.title}-{self.author}"

    class Meta:
        """Meta."""

        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"
