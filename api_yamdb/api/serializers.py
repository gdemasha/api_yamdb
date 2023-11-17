from rest_framework import serializers
from django.db.models import Avg

from reviews.models import Reviews, Comments, Title


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('rating')

    def get_rating(self, obj):
        return int(obj.reviews_score.aggregate(rating=Avg('score'))['rating'])


class ReviewsSerializer(serializers.ModelSerializer):
    #  author = serializers.SlugRelatedField(
    #  read_only=True,
    #  slug_field='username',
    #  default=serializers.CurrentUserDefault(),
    #  )
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Reviews
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')


class CommentSerializer(serializers.ModelSerializer):
    #  author = serializers.SlugRelatedField(
    #  read_only=True,
    #  slug_field='username',
    #  default=serializers.CurrentUserDefault(),
    #  )
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date', 'review')
