from django.db import models

from reviews.constants import MAX_LENGTH_NAME, MAX_LENGTH_SLUG


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
        )
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
        )
    )

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=MAX_LENGTH_NAME
    )
    description = models.TextField('Описание')
    year = models.IntegerField('Год релиза')
    category = models.ForeignKey(
        Category,
        verbose_name='Тип произведения',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр(ы) произведения',
        related_name='titles'
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
