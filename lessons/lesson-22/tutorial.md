# Кинопоиск. Проектирование сущностей.

Теперь, когда мы знаем так много
всего, нужно это закрепить на финальном проекте и
узнать немного нового.

В этом проекте я буду гораздо меньше акцентировать внимание
на уже известных и сделанных не раз деталях.
Но вы как преподаватель, не забывайте делать это за меня.

1. ## Создадим новый проект `kinopoisk`
   Создайте новую папку, а в ней сделайте виртуальную среду,
   установите `django` и запустите новый проект.
   > Не забывайте, что проект мы называем всегда `config`.
   Или как-то иначе, чтобы папка с настройками проекта
   имела лаконичное название.

2. ## Продумаем наш проект
   Я в методичке буду придерживаться следующей идеи:
   сначала придумать логику, потом делать красиво.<br><br>

   Лучше брать с чего-то пример: [Шрек? https://www.kinopoisk.ru/film/430/](https://www.kinopoisk.ru/film/430/)<br>
   Заметим, что в ссылке, как и у нас было, передается `id` фильма.
   Так мы можем понять, что до Шрека было загружено примерно 429 фильмов.

   #### В проекте будет:
    1. ### Core
       Страницы: `signin` `signup` `signout` `profile`<br>
       Модели: `User`
    2. ### kinopoisk
       Страницы: `signin` `signup` `signout` `profile`<br>
       Модели: `Movie` `Actor` `Review` `Genre`

3. ## Продумаем модели
   Можете пользоваться любым конструктором баз данных.<br>
   Например: https://sql.toad.cz/ <br>
   Можете писать сразу в `models.py` файлы, как сочтете нужным.<br><br>

   В дальнейшем я приложу файл который можно будет загрузить
   и база данных заполнится(фильмами, актерами, отзывами), однако, этот файл
   будет иметь структуру ровно такую же как в моделях ниже.
   Вы можете сами заполнять бд либо воспользоваться этим файлом.<br><br>

   Стоит отметить, что переопределять базовую модель
   не совсем корректно в целом. Лучше создать отдельную
   модель `UserProfile`, которая будет привязана `OneToOne`
   к базовому пользователю. И в эту модель уже можно
   добавлять `avatar` и что угодно еще. <br>
   Но для упрощения мы просто скопируем приложение `Core`
   с проекта `магазин`. Заодно ученики поймут, что приложения
   можно переиспользовать и нам не придется заново делать базовый шаблон,
   шапку и т.д. Не забудьте добавить `Core`
   в `INSTALLED_APPS` и изменить переменную
   `AUTH_USER_MODEL = 'Core.User'`. Так же внесем небольшие
   изменения в модель.<br><br>

   Создайте приложение `kinopoisk` и подключите к проекту.

   > Мигрировать будем после создания всех моделей.
    ```python
    # Core/models.py
    class User(AbstractUser):
        # Обьясните, что такое ManyToManyField.
        # Это поле будет содержать 0 или несколько идентификторов фильмов.
        # Можно для упрощения сказать, что это просто массив из id'шников 
        # понравившихся пользователю фильмов.
        favorite_movies = models.ManyToManyField('Movie')
        avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    ```
    ```python
    # kinopoisk/models.py
    from django.db import models
    from Core.models import User
    
    class MoviePerson(models.Model):
        class RoleType(models.TextChoices):
            ACTOR = 'actor', 'Actor'
            DIRECTOR = 'director', 'Director'
    
        name = models.CharField(max_length=255)
        birth_date = models.DateField()
        biography = models.TextField()
        photo = models.ImageField(
            upload_to="kinopoisk/images/person/photos/",
            blank=True, null=True
        )
        role = models.CharField(
            max_length=20, choices=RoleType.choices,
            blank=True, null=True
        )
    
    
    class Genre(models.Model):
        name = models.CharField(max_length=255)
        description = models.TextField(blank=True, null=True)
    
    
    class Movie(models.Model):
        title = models.CharField(max_length=255)
        description = models.TextField()
        release_date = models.DateField(null=True, blank=True)
        rating = models.FloatField(null=True, blank=True)
        # Продолжительность в минутах
        duration = models.PositiveSmallIntegerField()  
        genres = models.ManyToManyField(Genre, related_name='movies')
        director = models.ForeignKey(
            MoviePerson, on_delete=models.SET_NULL,
            null=True, related_name='directed_movies'
        )
        actors = models.ManyToManyField(
            MoviePerson, related_name='acted_in_movies'
        )
        poster = models.ImageField(
            upload_to="kinopoisk/images/movies/posters/",
            blank=True, null=True
        )
    
    
    class MovieReview(models.Model):
        author = models.ForeignKey(
            User, on_delete=models.SET_NULL,
            null=True, related_name='reviews'
        )
        movie = models.ForeignKey(
            Movie, on_delete=models.CASCADE,
            related_name='reviews'
        )
        text = models.TextField()
        likes = models.PositiveIntegerField(default=0)
        created_at = models.DateTimeField(auto_now_add=True)
    ``` 
   ** В `Django`, когда вы используете класс `models.TextChoices`
   (или любой другой вариант `Choices`), вы создаете перечисление для
   удобного использования определенных констант. При этом каждая константа в
   `TextChoices` может быть представлена парой значений: первое значение (ключ)
   используется в коде и базе данных, а второе значение (метка) используется
   для отображения в пользовательском интерфейсе, например, в формах или
   административной панели `Django`.<br>

   В данном случае, для `RoleType`:<br>
   'actor', 'Actor':<br>
    * Первое значение `actor` — это значение, которое будет храниться в базе данных. Оно используется в коде для
      проверки условий, выполнения запросов и т.д.
    * Второе значение `Actor` — это человекочитаемая строка, которая отображается в пользовательском интерфейсе. Это
      может быть полезно, когда вы хотите, чтобы в формах выбора или на страницах административной панели отображалось
      понятное человеку описание варианта.

4. ## Проведите миграции
   > Не забудьте почистить старые миграции приложения Core.

5. ## Добавьте таблицы в админку
   ```python
   # kinopoisk/admin.py
   from django.contrib import admin
   from .models import MoviePerson, Genre, Movie, MovieReview
   
   @admin.register(MoviePerson)
   class MoviePersonAdmin(admin.ModelAdmin):
       list_display = ('name', 'birth_date', 'role')
   
   @admin.register(Genre)
   class GenreAdmin(admin.ModelAdmin):
       list_display = ('name',)
   
   @admin.register(Movie)
   class MovieAdmin(admin.ModelAdmin):
       list_display = ('title', 'release_date', 'rating', 'duration')
   
   @admin.register(MovieReview)
   class MovieReviewAdmin(admin.ModelAdmin):
       list_display = ('movie', 'author', 'created_at', 'likes')
   ```

6. ## Создайте суперюзера и проверьте, что таблицы появились в админке.


## Подведите итоги.
>### Гит на следующем уроке. Если успеваете, загрузите на этом.