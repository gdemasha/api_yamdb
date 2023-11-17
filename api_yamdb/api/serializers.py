from rest_framework import serializers

from django.db.models import Avg

from reviews.models import Reviews, Comments, Category, Genre, Title
import datetime as dt


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
        return 0

    def create(self, validated_data):
        print(validated_data.keys())
        return super().create(validated_data)

    def get_rating(self, obj):
        return 1
        # пока так
        return int(obj.reviews_score.aggregate(rating=Avg('score'))['rating'])
