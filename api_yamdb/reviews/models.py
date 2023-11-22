from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.constants import (
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_NAME,
    MAX_LENGTH_ROLE,
    MAX_LENGTH_SLUG,
    MAX_LENGTH_TEXT,
    ROLE_CHOICE,
    USER,
)


class User(AbstractUser):
    """Кастомная модель пользователя."""

    email = models.EmailField(
        'Почта',
        max_length=MAX_LENGTH_EMAIL,
        unique=True,
    )
    bio = models.CharField(
        'Био',
        max_length=MAX_LENGTH_TEXT,
        null=True,
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=MAX_LENGTH_ROLE,
        choices=ROLE_CHOICE,
        default=USER,
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Category(models.Model):
    """Модель категории."""

    name = models.CharField(
        'Название категории',
        max_length=MAX_LENGTH_NAME,
    )
    slug = models.SlugField(
        'URL категории',
        max_length=MAX_LENGTH_SLUG,
        unique=True,
        help_text=(
            'Идентификатор категории произведения. '
            f'Не более {MAX_LENGTH_SLUG} символов. '
            'Разрешены символы латиницы и символы: ^[-a-zA-Z0-9_]+$'
        ),
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра."""

    name = models.CharField(
        'Название жанра',
        max_length=MAX_LENGTH_NAME,
    )
    slug = models.SlugField(
        'URL жанра',
        max_length=MAX_LENGTH_SLUG,
        unique=True,
        help_text=(
            f'Идентификатор жанра. Не более {MAX_LENGTH_SLUG} символов. '
            'Разрешены символы латиницы и символы: ^[-a-zA-Z0-9_]+$'
        ),
    )

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        'Название произведения',
        max_length=MAX_LENGTH_NAME,
    )
    description = models.TextField(
        'Описание',
        max_length=MAX_LENGTH_TEXT,
    )
    year = models.IntegerField('Год релиза')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Тип произведения',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр(ы) произведения',
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзыва."""

    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
    )
    score = models.PositiveIntegerField(
        'Оценка',
        default=1,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1),
        ],
        blank=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('author', 'title')

    def __str__(self):
        return f'{self.author} про {self.title}'


class Comments(models.Model):
    """Модель комментария."""

    text = models.TextField(
        'Комментарий',
        max_length=MAX_LENGTH_TEXT,
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True,
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий {self.author} к {self.review}'
