import datetime as dt

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import Avg
from rest_framework import serializers

from reviews.constants import MAX_LENGTH_EMAIL, MAX_LENGTH_USERNAME
from reviews.models import Category, Comments, CustomUser, Genre, Review, Title


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя 'user'."""

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        read_only_fields = ('role',)


class AdminSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя 'admin'."""

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


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
        model = CustomUser
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
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category',
        )

    def validate_year(self, value):
        year = dt.date.today().year
        if not (value <= year):
            raise serializers.ValidationError('Проверьте год произведения!')
        return value

    def get_rating(self, obj):
        score_title = Review.objects.filter(title_id=obj.id)
        if score_title.count() != 0:
            return int(score_title.aggregate(Avg('score'))['score__avg'])
        return None


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


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comments
        exclude = ('review',)
