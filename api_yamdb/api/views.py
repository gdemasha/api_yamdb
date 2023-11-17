from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Reviews, Title
from .serializers import ReviewsSerializer, CommentSerializer
from .permissions import AuthorOrModeratorOrAdminPermission


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = (AuthorOrModeratorOrAdminPermission,)

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        return serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrModeratorOrAdminPermission,)

    def get_queryset(self):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Reviews, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Reviews, pk=review_id)
        return serializer.save(author=self.request.user, review=review)
