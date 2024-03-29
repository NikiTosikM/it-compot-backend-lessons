from django.shortcuts import render

from .models import Movie, MoviePerson, Genre


def main(request):
    return render(request, 'kinopoisk/main.html')


def movie_list(request):
    movies = Movie.objects.all().order_by('-id')
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


def person_detail(request, person_id):
    person = MoviePerson.objects.get(id=person_id)
    if person.role == MoviePerson.RoleType.ACTOR:
        movies = person.acted_in_movies.all()
    else:
        movies = person.directed_movies.all()
    return render(request, 'kinopoisk/person_detail.html', {
        'person': person,
        'movies': movies
    })


def genre_detail(request, genre_id):
    genre = Genre.objects.get(id=genre_id)
    movies = genre.movies.all()
    return render(request, 'kinopoisk/genre_detail.html', {
        'genre': genre, 'movies': movies
    })
