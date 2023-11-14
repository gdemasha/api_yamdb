from rest_framework import viewsets

from reviews.models import Category, Genre, Title
from reviews.serializers import (
    CategoriesSerializer, GenreSerializer, TitlesSerializer
)


# пока заглушки, чтобы были эндпоинты
class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
