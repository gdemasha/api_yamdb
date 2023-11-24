import datetime as dt

from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from reviews.constants import MAX_LENGTH_EMAIL, MAX_LENGTH_USERNAME
from reviews.models import Category, Comments, User, Genre, Review, Title


class AdminSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя 'admin'."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


class UserSerializer(AdminSerializer):
    """Сериализатор для пользователя 'user'."""

    role = serializers.StringRelatedField()


class AuthSerializer(serializers.Serializer):
    """Сериализатор для регистрации."""

    email = serializers.EmailField(max_length=MAX_LENGTH_EMAIL, required=True)
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME,
        validators=[UnicodeUsernameValidator()],
        required=True,
    )


class GetTokenSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с токеном."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesReadSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений - только на чтение."""

    genre = GenreSerializer(read_only=False, many=True)
    category = CategoriesSerializer(read_only=False)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category',
        )

    def validate_year(self, value):
        if dt.date.today().year < value:
            raise serializers.ValidationError('Проверьте год произведения!')
        return value


class TitlesWriteSerializer(TitlesReadSerializer):
    """Сериализатор для произведений - только на запись."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )


class ReviewsSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(ReviewsSerializer):
    """Сериализатор для комментариев."""

    class Meta:
        model = Comments
        exclude = ('review',)
