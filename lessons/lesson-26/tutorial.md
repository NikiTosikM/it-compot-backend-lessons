# Кинопоиск. Карточка для `MoviePerson`

Не используем готовую карточку `bootstrap`, напишите её самостоятельно. 

С Frontend курса, у довольно сильных учеников на мой взгляд,
**очень** слабые знания об элементарном размещении элементов.

Достаточно объяснить 4 свойства:
* `display: flex` - включает использование `flex-direction` `justify-content-center` `gap` `align-items`


```html
<!-- kinopoisk/movie_list.html -->
{% extends 'Core/base.html' %}
{% block title %}Кинопоиск | Фильмы{% endblock %}
{% block content %}
    <h2>Фильмы</h2>
    {% for movie in movies %}
        <p>{{ movie.title }}</p>
    {% endfor %}
{% endblock %}
```

1. ## Пишем карточку
    