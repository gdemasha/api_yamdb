from django.contrib import admin

from reviews.models import Category, Genre, Title


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
