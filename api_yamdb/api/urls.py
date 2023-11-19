from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoriesViewSet, CommentsViewSet, GenresViewSet,
    ReviewsViewSet, TitlesViewSet, UserViewSet,
    category_delete, genre_delete
)

router = DefaultRouter()
router.register(
    r'^titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='reviews'
)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/$',
    ReviewsViewSet,
    basename='review',
)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments',
)
router.register(
    (r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
     r'/comments/(?P<comment_id>\d+)/$'),
    CommentsViewSet,
    basename='comment',
)
router.register('users', UserViewSet, basename='users')
router.register('categories', CategoriesViewSet, basename='categories')
router.register('genres', GenresViewSet, basename='genres')
router.register('titles', TitlesViewSet, basename='titles')


urlpatterns = [
    path('v1/genres/<slug:slug>/', genre_delete),
    path('v1/categories/<slug:slug>/', category_delete),
    path('v1/', include(router.urls)),
]
