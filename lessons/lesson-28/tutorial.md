# Понятие `Code refactoring`, страница персоны и жанра.

Рефакторинг кода — это процесс улучшения существующего кода 
без изменения его внешнего поведения. Цель рефакторинга — сделать 
код более понятным, читаемым и эффективным, а также упростить 
дальнейшую разработку и обслуживание программы.
> Однако мы все же перепишем некоторую логику

1. ## Исправляем код
    Заметим, что зная `id` объекта `MoviePerson` мы можем его получить.
    Нам не нужно знать его роль (актер или режиссер).
    Исходя из этого, можно сделать вывод, что нам не нужно 2 контроллера
    для отображения `actor_detail` и `director_detail`.
    
    * ### Urls
        #### Поменяем это:
        ```python
        # kinopoisk/urls.py
        urlpatterns = [
            ...
            path('actor/<int:actor_id>/', actor_detail, name='actor_detail'),
            path('director/<int:director_id>/', director_detail, name='director_detail')
        ]
        ```
        #### На это:
        ```python
        urlpatterns = [
            ...
            path('person/<int:person_id>/', person_detail, name='person_detail')
        ]
        ```
   
    * ### Controllers
        #### Поменяем это:
        ```python
        # kinopoisk/views.py
        ...
        def actor_detail(request, actor_id):
            actor = MoviePerson.objects.get(id=actor_id)
            movies = actor.acted_in_movies.all()
            return render(request, 'kinopoisk/person_detail.html', {
                'person': actor, 'movies': movies,
            })
        
        
        def director_detail(request, director_id):
            director = MoviePerson.objects.get(id=director_id)
            movies = director.directed_movies.all()
            return render(request, 'kinopoisk/person_detail.html', {
                'person': director, 'movies': movies,
            })
        ```
        #### На это:
        ```python
        # kinopoisk/views.py
        ...
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
        ```
    Логичный вопрос: `А разве не нужно сделать также со списками актеров и режиссеров?`<br>
    Ответ: `Нужно! Но я не буду заострять на этом внимание, если останется время можете сделать.`

2. ## Напишем `person_detail.html`
    > Для Easy и Medium учеников шаблон сложный. Делайте проще.
    ```html
    <!-- kinopoisk/person_detail.html -->
    {% extends "Core/base.html" %}
    {% load static %}
    {% block title %}Кинопоиск | {{ person.name|title }}{% endblock %}
    {% block main %}
        <div class="fccs justify-content-md-center flex-md-row m-sm-0 gap-5 w-90 mx-auto ">
            <img class="h-min mx-md-0 mx-auto" src="{{ person.photo.url }}" alt="">
            <div class="fc mx-auto mx-md-0">
                <h1 class="mb-4 text-center me-md-auto d-inline">{{ person.name|title }}</h1>
                <span class="text-center me-md-auto d-inline">Дата рождения: {{ person.birth_date }}</span>
                <div class="mt-3 frc gap-3 mw-550px flex-wrap bg-black-30 p-4 rounded-4">
                    {% for movie in movies %}
                       {% include 'kinopoisk/includes/movie_card.html' with movie=movie %}
                    {% endfor %}
                </div>
            </div>
        </div>
    {% endblock %}
    ```

3. ## Напишем `genre_detail.html`
    ```html
    {% extends "Core/base.html" %}
    {% load static %}
    {% block title %}Кинопоиск | {{ genre.name|title }}{% endblock %}
    {% block main %}
        <h1 class="mb-4">{{ genre.name|title }}</h1>
        <div class="fr gap-3 mw-1000px flex-wrap">
            {% for movie in movies %}
                {% include 'kinopoisk/includes/movie_card.html' with movie=movie %}
            {% endfor %}
        </div>
    {% endblock %}
    ```

4. ## Если осталось время
    Заметим, что карточки фильмов на странице с актерами и режиссерами большеваты.<br>
    > Может показаться, что высосано из пальца, однако часто нужно уметь контролировать
      вид `include` элементов.

    ### Я вижу 2 решения:
    * ### 1
      Использовать общий класс у родителя, например `person_container`, и через него 
      модифицировать максимальную ширину карточки.
      ```css
      /* kinopoisk/static/kinopoisk/css/person_detail.css */
      .person_container .movie_card{
          max-width: 150px !important;
      }
      ```
      Нужно создать блок для подключения кастомных стилей для разных страниц в `base.html`.
      > Если мы просто добавим `person_detail.css` в `base.html`, 
        тогда на всех страницах будет этот файл, а это излишне. 
     
      Добавим новый блок `head`, который мы сможем заполнять в дочерних страницах.
      ```html
      <!-- Core\templates\Core\base.html -->
      ...
      <head>
          ...
          {% block head %}{% endblock %}
          ...
      </head>
      ...
      ```
      Тогда в `person_detail.html`
      ```html
      <!-- kinopoisk/person_detail.html -->
      {% extends "Core/base.html" %}
      ...
      {% block head %}
          <link rel="stylesheet" href="{% static 'kinopoisk/css/person_detail.css' %}">
      {% endblock %}
      ...
      ```
    * ### 2
      Передавать классы через переменную сквозь `include`.
      ```html
      <!-- kinopoisk/templates/kinopoisk/person_detail.html -->                                           
      ...
      {% include 'kinopoisk/includes/movie_card.html' with movie=movie movie_card_classes='mw-150px' %}
      ...
      ```
      ```html
      <!-- kinopoisk/templates/kinopoisk/includes/movie_card.html -->
      <a href="{% url 'movie_detail' movie_id=movie.id %}" 
         class="{{ movie_card_classes }} fc mw-300px w-100 text-light text-decoration-none hover-scale-2">
          <img src="{{ movie.poster.url }}" alt="">
          ...
      </a>
      ```

## Подведите итоги.
># git push...