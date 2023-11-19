from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from reviews.constants import MAX_LENGTH_NAME, MAX_LENGTH_SLUG, ROLE_CHOICE


class CustomUser(AbstractUser):
    email = models.EmailField('Почта', max_length=254, unique=True,)
    bio = models.CharField('Био', max_length=254, null=True, blank=True,)
    role = models.CharField(
        'Роль',
        max_length=9,
        choices=ROLE_CHOICE,
        default='user',
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField('Название категории', max_length=MAX_LENGTH_NAME)
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
    name = models.CharField('Название жанра', max_length=MAX_LENGTH_NAME)
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
    name = models.CharField(
        'Название произведения',
        max_length=MAX_LENGTH_NAME,
    )
    description = models.TextField('Описание')
    year = models.IntegerField('Год релиза')
    category = models.ForeignKey(
        Category,
        verbose_name='Тип произведения',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр(ы) произведения',
        related_name='titles',
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Reviews(models.Model):

    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
    )
    score = models.PositiveIntegerField(
        default=1,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1),
        ],
        blank=True,
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review',
            )
        ]


class Comments(models.Model):

    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True,
    )
    review = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
