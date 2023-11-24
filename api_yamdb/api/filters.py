from django_filters import rest_framework

from reviews.models import Title


class TitleFilter(rest_framework.FilterSet):
    """
    Кастомный фильтр, позволяющий фильтровать произведения'
    с использованием параметра 'slug' жанра и категории.
    """
    category = rest_framework.CharFilter(field_name='category__slug')
    genre = rest_framework.CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category')
