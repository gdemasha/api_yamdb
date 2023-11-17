from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Reviews
from .serializers import ReviewsSerializer, CommentSerializer
from .permissions import AuthorOrModeratorOrAdminPermission


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = (AuthorOrModeratorOrAdminPermission,)

    def get_queryset(self):
        #  title_id = self.kwargs['title_id']
        #  title = get_object_or_404(Titles, pk=title_id)
        #  return title.reviews.all()
        pass

    def perform_create(self, serializer):
        #  title_id = self.kwargs['title_id']
        #  title = get_object_or_404(Titles, pk=title_id)
        #  return serializer.save(author=self.request.user, title=title)
        pass


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
