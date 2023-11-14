from rest_framework.routers import DefaultRouter

from django.urls import include, path

from reviews.views import TitlesViewSet, GenresViewSet, CategoriesViewSet


v1_router = DefaultRouter()
v1_router.register('categories', CategoriesViewSet, basename='categories')
v1_router.register('genres', GenresViewSet, basename='genres')
v1_router.register('titles', TitlesViewSet, basename='titles')

urlpatterns = [
    path('', include(v1_router.urls)),
]
