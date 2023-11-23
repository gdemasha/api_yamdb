from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .permissions import (
    AdminOnlyPermission, AdminUserPermission,
    AuthorOrModeratorOrAdminPermission,
)
from .serializers import (
    AdminSerializer, AuthSerializer,
    CategoriesSerializer, CommentSerializer,
    GenreSerializer, GetTokenSerializer,
    ReviewsSerializer, TitlesReadSerializer,
    TitlesWriteSerializer, UserSerializer,
)
from api_yamdb.settings import EMAIL_HOST_USER
from reviews.models import Category, Genre, Review, Title, User


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для пользователя."""

    queryset = User.objects.all()
    serializer_class = AdminSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (AdminOnlyPermission,)
    http_method_names = ['get', 'post', 'delete', 'patch']

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
    """Вью-функция для регистрации."""

    serializer = AuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, created = User.objects.get_or_create(
            email=serializer.validated_data['email'],
            username=serializer.validated_data['username'],
        )
    except IntegrityError:
        raise ValidationError('Указанный email или username уже существует!')

    if user.username == 'me':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Код для входа',
        message=f'Код для входа {confirmation_code}',
        from_email=EMAIL_HOST_USER,
        recipient_list=[user.email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def token(request):
    """Вью-функция для работы с токеном."""

    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username'],
    )
    if not default_token_generator.check_token(
            user,
            serializer.validated_data['confirmation_code'],
    ):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    data = {'token': str(AccessToken.for_user(user))}
    return Response(data)


class GenresViewSet(viewsets.ModelViewSet):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AdminUserPermission,)


class CategoriesViewSet(GenresViewSet):
    """Вьюсет для категорий."""

    queryset = Category.objects.all().order_by('id')
    serializer_class = CategoriesSerializer


@api_view(['DELETE'])
@permission_classes((AdminUserPermission,))
def genre_delete(request, slug):
    """Вью-функция для запроса на удаление жанра."""

    get_object_or_404(Genre, slug=slug).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes((AdminUserPermission,))
def category_delete(request, slug):
    """Вью-функция для запроса на удаление категории."""

    get_object_or_404(Category, slug=slug).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class TitlesViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""

    queryset = (Title.objects
                .annotate(
                    rating=Avg('reviews__score'),
                ).prefetch_related(
                    'reviews', 'genre',
                ).select_related(
                    'category',
                ).order_by('id')
                )
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)
    filterset_class = TitleFilter
    search_fields = ('name',)
    permission_classes = (AdminUserPermission,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesReadSerializer
        return TitlesWriteSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""

    serializer_class = ReviewsSerializer
    permission_classes = (AuthorOrModeratorOrAdminPermission,)
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all().order_by('id')

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        try:
            serializer.save(author=self.request.user, title=title)
        except IntegrityError:
            raise ValidationError(
                'Вы уже оставляли отзыв на это произведение.'
            )


class CommentsViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (AuthorOrModeratorOrAdminPermission,)
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_queryset(self):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all().order_by('pub_date')

    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, pk=review_id)
        return serializer.save(author=self.request.user, review=review)
