from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from reviews.models import Category, CustomUser, Genre, Reviews, Title

from .permissions import (
    AdminOnlyPermission, AdminUserPermission,
    AuthorOrModeratorOrAdminPermission
)
from .serializers import (
    AdminSerializer, CategoriesSerializer,
    CommentSerializer, GenreSerializer,
    ReviewsSerializer, TitlesReadSerializer,
    TitlesWriteSerializer, UserSerializer
)


# class ContentViewSet(viewsets.ModelViewSet):
#     '''Вьюсетам CommentsViewSet, TitlesViewSet и UserViewSet'''
#     '''можно было бы наследоваться от такого вьюсета'''
#     def update(self, request, *args, **kwargs):
#         if request.method == 'PUT':
#             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         return super().update(request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (AdminUserPermission, permissions.IsAuthenticated)
    http_method_names = ['get', 'post', 'patch', 'delete']


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = (AuthorOrModeratorOrAdminPermission,)

    def get_title(self):
        title_id = self.kwargs['title_id']
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title.reviews.all().order_by('id')

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            title=self.get_title(),
        )


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrModeratorOrAdminPermission,)

    def get_queryset(self):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Reviews, pk=review_id)
        return review.title.comments.all()

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            review=self.get_review(),
        )

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().order_by('id')
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')
    permission_classes = (AdminUserPermission,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesReadSerializer
        return TitlesWriteSerializer

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AdminUserPermission,)


class CategoriesViewSet(GenresViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategoriesSerializer


@api_view(['DELETE'])
@permission_classes((AdminUserPermission,))
def genre_delete(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    if request.method == "DELETE":
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes((AdminUserPermission,))
def category_delete(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == "DELETE":
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = CustomUser.objects.all()
    serializer_class = AdminSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (AdminOnlyPermission,)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    @action(
        methods=['GET', 'PATCH', ],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
        url_path='me',
    )
    def get(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            request.user, data=request.data, partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
