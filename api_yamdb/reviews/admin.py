from django.contrib import admin

from reviews.models import Category, User, Genre, Review, Title


@admin.register(Title)
class TitlesAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('year', 'category', 'genre')


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = list_display = ('name', 'slug')


@admin.register(Genre)
class GenreAdmin(CategoriesAdmin):
    pass


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    search_fields = list_display = ('author', 'title', 'pub_date')
    list_filter = ('author', 'title')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
    )
    search_fields = ('username', 'role')
    list_filter = ('username',)
