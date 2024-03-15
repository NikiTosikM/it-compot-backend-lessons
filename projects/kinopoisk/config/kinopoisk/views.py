from django.shortcuts import render

from .models import Movie, MoviePerson, Genre


def main(request):
    return render(request, 'kinopoisk/main.html')


def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'kinopoisk/movie_list.html', {
        'movies': movies
    })


def actor_list(request):
    actors = MoviePerson.objects.filter(
        role=MoviePerson.RoleType.ACTOR
    ).order_by('-id')
    return render(request, 'kinopoisk/person_list.html', {
        'persons': actors, 'title': 'Актеры'
    })


def director_list(request):
    directors = MoviePerson.objects.filter(role=MoviePerson.RoleType.DIRECTOR)
    return render(request, 'kinopoisk/person_list.html', {
        'persons': directors, 'title': 'Режиссеры'
    })


def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'kinopoisk/genre_list.html', {
        'genres': genres
    })


def movie_detail(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    return render(request, 'kinopoisk/movie_detail.html', {
        'movie': movie
    })


def actor_detail(request, actor_id):
    actor = MoviePerson.objects.get(id=actor_id, role=MoviePerson.RoleType.ACTOR)
    movies = actor.acted_in_movies.all()
    return render(request, 'kinopoisk/person_detail.html', {
        'person': actor, 'movies': movies,
    })


def director_detail(request, director_id):
    director = MoviePerson.objects.get(id=director_id, role=MoviePerson.RoleType.DIRECTOR)
    movies = director.directed_movies.all()
    return render(request, 'kinopoisk/person_detail.html', {
        'person': director, 'movies': movies,
    })


def genre_detail(request, genre_id):
    genre = Genre.objects.get(id=genre_id)
    movies = genre.movies.all()
    return render(request, 'kinopoisk/genre_detail.html', {
        'genre': genre, 'movies': movies
    })
