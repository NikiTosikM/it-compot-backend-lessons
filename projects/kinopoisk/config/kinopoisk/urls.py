from django.urls import path

from .views import *

urlpatterns = [
    path('', main, name='main'),  # Главная страница.

    path('movies/', movie_list, name='movie_list'),  # Список всех фильмов.
    path('actors/', actor_list, name='actor_list'),  # Список всех актеров.
    path('directors/', director_list, name='director_list'),  # Список всех режиссеров.
    path('genres/', genre_list, name='genre_list'),  # Список всех жанров.

    path('movie/<int:movie_id>/', movie_detail, name='movie_detail'),  # Детали фильма.
    path('person/<int:person_id>/', person_detail, name='person_detail'),
    path('genre/<int:genre_id>/', genre_detail, name='genre_detail'),  # Фильмы по жанру.

    path('add_movie_review/', add_movie_review, name='add_movie_review'),
]
