from rest_framework import filters, status, viewsets, permissions
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import AccessToken

from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Genre, Category, Reviews, Title, CustomUser
from .serializers import (
    ReviewsSerializer, CommentSerializer, GenreSerializer,
    CategoriesSerializer, TitlesSerializer, UserSerializer,
    AdminSerializer, AuthSerializer, GetTokenSerializer
)
from .permissions import (
    AdminOnlyPermission
    # AuthorOrModeratorOrAdminPermission
)
from reviews.constants import SEND_CODE_EMAIL


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    # permission_classes = (AuthorOrModeratorOrAdminPermission,)

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all().order_by('id')

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        return serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = (AuthorOrModeratorOrAdminPermission,)

    def get_queryset(self):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Reviews, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Reviews, pk=review_id)
        return serializer.save(author=self.request.user, review=review)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().order_by('id')
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoriesViewSet(GenresViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategoriesSerializer


@api_view(['DELETE'])
def genre_delete(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    if request.method == "DELETE":
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
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


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup(request):
    serializer = AuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, create = CustomUser.objects.get_or_create(
            email=serializer.validated_data['email'],
            username=serializer.validated_data['username'],
        )
    except IntegrityError as error:
        raise ValidationError(f'{error}')
    if user.username == 'me':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код для входа',
            message=f'Код для входа {confirmation_code}',
            from_email=SEND_CODE_EMAIL,
            recipient_list=[user.email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        CustomUser,
        username=serializer.validated_data['username'],
    )
    if not default_token_generator.check_token(
            user,
            serializer.validated_data['confirmation_code'],
    ):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    token = AccessToken.for_user(user)
    data = {'token': str(token)}
    return Response(data)
