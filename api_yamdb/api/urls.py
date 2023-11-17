from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ReviewsViewSet

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
    ReviewsViewSet,
    basename='comments',
)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/(?P<comment_id>\d+)/$',
    ReviewsViewSet,
    basename='comment',
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
