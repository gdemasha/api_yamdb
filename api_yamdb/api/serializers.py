from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import serializers
from django.db.models import Avg

from reviews.models import (
    Reviews, Comments, Category, Genre, Title, CustomUser
)
import datetime as dt


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Reviews
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date', 'review')


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=False)
    category = CategoriesSerializer(read_only=False, many=False)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )

    def validate_year(self, value):
        year = dt.date.today().year
        if not (value <= year):
            raise serializers.ValidationError('Проверьте год произведения!')
        return value

    def get_rating(self, obj):
        return int(obj.reviews_score.aggregate(rating=Avg('score'))['rating'])

    def create(self, validated_data):
        title = Title.objects.create(
            **validated_data,
            category=get_object_or_404(
                Category,
                slug=self.initial_data['category'],
            ),
        )
        title.genre.set(get_list_or_404(
            Genre,
            slug__in=self.initial_data['genre'],
        ))
        return title


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

