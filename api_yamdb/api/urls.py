from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoriesViewSet, CommentsViewSet, GenresViewSet,
    ReviewsViewSet, TitlesViewSet, UserViewSet,
    category_delete, genre_delete, signup, token,
)


router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('categories', CategoriesViewSet, basename='categories')
router.register('genres', GenresViewSet, basename='genres')
router.register('titles', TitlesViewSet, basename='titles')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='reviews'
)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments',
)
url_auth = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', token, name='token'),
]
urlpatterns = [
    path('v1/genres/<slug:slug>/', genre_delete),
    path('v1/categories/<slug:slug>/', category_delete),
    path('v1/', include(url_auth)),
    path('v1/', include(router.urls)),
]
