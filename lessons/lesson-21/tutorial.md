# Создаем свою модель пользователя.

У нас осталась незаполненная страница профиля.
Вспомните существующие поля модели `User`, а лучше покажите наглядно
класс `AbstructUser`.

1. ## Допишем `profile.html`
   ```html
   <!-- Core/auth/profile.html -->
   {% extends 'Core/base.html' %}
   {% load static %}
   {% block title %}Shop | Profile{% endblock %}
   
   {% block content %}
       <div class="d-flex flex-column mx-auto" style="width: min-content">
           <div class="d-flex align-items-center gap-3">
               <img src="{% static 'Core/img/user.png' %}"
                    style="filter: invert(.9)"
                    width="50" height="50"
                    alt="">
               <h1 class="text-body text-center fw-bold">
                   {{ request.user.username }}
               </h1>
           </div>
           <ul>
               <!-- Выводим только существующие поля -->
               {% if request.user.first_name %}
                   <li>{{ request.user.first_name }}</li>
               {% endif %}
               {% if request.user.last_name %}
                   <li>{{ request.user.last_name }}</li>
               {% endif %}
               {% if request.user.email %}
                   <li>{{ request.user.email }}</li>
               {% endif %}
           </ul>
           <a href="{% url 'orders' %}"
              class="btn border-secondary mx-auto">
               My orders
           </a>
       </div>
   {% endblock %}
   ```
   Сейчас аватар у всех пользователей будет одна и та же картинка. <br>
   Что нужно сделать, чтобы у каждого пользователя могла быть своя ава?<br>
   Нужно добавить в модель ещё одно поле которое будет хранить путь 
   до картинки пользователя.

2. ## Создадим свою модель пользователя.
    Мы не можем изменять исходный код библиотек(можем, но лучше не надо),
    поэтому мы не можем добавить новое поле в `AbstractUser` напрямую.
    Однако мы можем унаследоваться от `AbstractUser`, создав
    новую модель `User`. <br>
    Пусть ученики догадаются где мы будем создавать эту модель.
    ```python
    # Core/models.py
    from django.contrib.auth.models import AbstractUser
    from django.db import models
   
    class User(AbstractUser):
       pass  # объясните что это
    ```
    Так же нужно указать какую модель пользователя `django` будет использовать.
    ```python
    # settings.py
    ...
    AUTH_USER_MODEL = 'Core.User'
    ...
    ```
    Поменяем `import` модели пользователя для модели заказа.
    ```python
    # shop/models.py
    # from django.contrib.auth.models import User <---- Было
    from Core.models import User  #               <---- Стало
    ```
    Нужно создать файлы миграций и выполнить их, чтобы класс в `python` 
    смапился на бд.<br>
    `python manage.py makemigrations`<br>
    `python manage.py migrate`<br><br>

    Сейчас мы столкнемся с проблемой, когда миграции модели 
    пользователя из базового приложения django и наша начнут конфликтовать.
    В этом случае можно пытаться изменить файлы миграций руками,
    но для нас это будет пока что сложновато. Мы выполним сброс бд.
    * Удалям файлы миграций внутри каждого нашего приложени внутри папки
    `migrations`.<br>
      Осторожно, не удалите `__init__.py` файлы.
    * Удаляем `db.sqlite`
    * Повторно выполняем:<br>
    `python manage.py makemigrations`<br>
    `python manage.py migrate`<br><br>
   
    **Теперь миграция пройдет успешно.**<br>
    Важно понимать, что такие радикальные методы, как удаление базы данных,
    можно сказать, никогда не применяется, такие ситуации продумываются
    заранее, либо редактируются файлы миграций. <br><br>

    Желательно, чтобы ученики хотя бы примерно понимали,
    что при наследовании, функции и переменные содержащиеся в родителе, так же
    будут и у дочернего класса если мы их не переопределим, а значит сейчас у
    **нового User** есть все те же поля, что и у '**старого**'.

3. ## Добавим `avatar` в модель пользователя
    ```python
    class User(AbstractUser):
        avatar = models.ImageField(
            upload_to='avatars/', 
            null=True, blank=True
        )
    ```
    `python manage.py makemigrations`<br>
    `python manage.py migrate`

4. ## Исправим отображение картинки в профиле.
    Если аватарка есть, то отображаем ее, если нет, 
    то стандартную картинку.
    ```html
    <!-- Core/auth/profile.html -->
    {% if request.user.avatar %} 
        <img src="{{ request.user.avatar.url }}"
             width="50" height="50"
             class="rounded-5 object-fit-cover"
             alt="">
    {% else %}
        <img src="{% static 'Core/img/user.png' %}"
             style="filter: invert(.9)"
             width="50" height="50"
             alt="">
    {% endif %}
    ```
    ### Зайдем в админку
    ммм...

5. ## Создадим пользователя с правами администратора.
    `python manage.py createsuperuser`
    ### Зайдем в админку
    ммм... Где юзеры?

6. ## Настроим отображение модели `User` в админке.
    ```python
    class User(AbstractUser):
        avatar = models.ImageField(
            upload_to='avatars/', 
            null=True, blank=True
        )
    ```
    ### Установить аватарку через админку, проверьте, что все работает.


## Подведите итоги.
># git push...