# Кинопоиск. Доделываем контроллеры.

На этом уроке мы должны доделать контроллеры, так чтобы они передавали внутрь
шаблонов нужные нам данные.

Похожих контроллеров много, а значит у учеников будет много личной практики. 

1. ## Контроллеры.
    Я прокомментировал, что в теории можно `подсказать`, а что ученики должны сделать `сами`.
    Просто обсуждайте с учениками, что должно передаваться в тот или иной шаблон,
    и поглядывайте в раздел **[ORM](https://github.com/xlartas/it-compot-backend-methods/blob/main/django-base.md#orm)**
    в шпаргалке.
    ```python
    from django.shortcuts import render, get_object_or_404
    from .models import Movie, MoviePerson, Genre
    
    def main(request):  # Сами
        return render(request, 'kinopoisk/main.html')
    
    def movie_list(request):  # Сами
        movies = Movie.objects.all()
        return render(request, 'kinopoisk/movie_list.html', {
            'movies': movies
        })
    
    
    def actor_list(request):  # Подсказываем
        actors = MoviePerson.objects.filter(role=MoviePerson.RoleType.ACTOR)
        return render(request, 'kinopoisk/person_list.html', {
            'people': actors, 'title': 'Actors'
        })
    
    
    def director_list(request):  # Сами
        directors = MoviePerson.objects.filter(role=MoviePerson.RoleType.DIRECTOR)
        return render(request, 'kinopoisk/person_list.html', {
            'people': directors, 'title': 'Directors'
        })
    
    
    def genre_list(request):  # Сами
        genres = Genre.objects.all()
        return render(request, 'kinopoisk/genre_list.html', {
            'genres': genres
        })
    
    
    def movie_detail(request, movie_id):  # Сами
        movie = Movie.objects.get(id=movie_id)
        return render(request, 'kinopoisk/movie_detail.html', {
            'movie': movie
        })
    
    def actor_detail(request, actor_id):  # Напомнить, про раздел Related Name в шпаргалке.
        actor = MoviePerson.objects.get(id=actor_id, role=MoviePerson.RoleType.ACTOR)
        movies = actor.acted_in_movies.all()
        return render(request, 'kinopoisk/person_detail.html', {
            'person': actor, 'movies': movies, 'title': 'Actor'
        })
    
    
    def director_detail(request, director_id):  # Сами
        director = MoviePerson.objects.get(id=director_id, role=MoviePerson.RoleType.DIRECTOR)
        movies = director.directed_movies.all()
        return render(request, 'kinopoisk/person_detail.html', {
            'person': director, 'movies': movies, 'title': 'Director'
        })
    
    
    def genre_detail(request, genre_id):  # Сами
        genre = Genre.objects.get(id=genre_id)
        movies = genre.movies.all()
        return render(request, 'kinopoisk/genre_detail.html', {
            'genre': genre, 'movies': movies
        })
    ```

## Место для загрузки на гит или для доделать что-либо.

## Подведите итоги.
># git push...