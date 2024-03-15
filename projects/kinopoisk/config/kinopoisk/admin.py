from django.contrib import admin

from .models import MoviePerson, Genre, Movie, MovieReview


@admin.register(MoviePerson)
class MoviePersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo', 'birth_date', 'role')
    list_editable = ('photo', 'birth_date', 'role')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'poster', 'release_date', 'rating', 'duration')


@admin.register(MovieReview)
class MovieReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'author', 'created_at', 'likes')
