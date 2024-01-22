# Шаблонизация в зависимости от аутентифицированности и права доступа 

Вспомним, что в предыдущий раз мы сделали 4 кнопки в header
`signup`, `signin`, `profile`, `logout`.  <br>

Очевидно, что нам нужно видеть `profile` и `logout` только когда мы **_вошли_**.<br>
А `signup` и `signin` только когда **_не вошли_**.

Вспомним, что мы передаем объект `request` в функцию `render`.
```python
return render(request, 'example.html')
```
Объект `request` содержит информацию о текущей 
сессии и аутентифицированном пользователе(и не только). Это позволяет 
отображать пользовательские данные и изменять содержимое 
страницы в зависимости от состояния пользователя.
Мы можем использовать его в шаблоне как обычную переменную и выводить разные поля этого объекта.
```html
<!-- В вашем шаблоне (template.html) -->
<!-- Можете ради интереса все это вывести и посмотреть на настоящие данные -->
<p>{{ request.method }}</p>
<p>{{ request.GET }}</p>
<p>{{ request.POST }}</p>
<p>{{ request.COOKIES }}</p>
<p>{{ request.session }}</p>
<p>{{ request.user }}</p>
<p>{{ request.user.username }}</p>
<p>{{ request.user.first_name }}</p>
<p>{{ request.user.is_authenticated }}</p>
```
> Можете заскринить и кинуть ученикам почитать


1. ## Исправим отображение ссылок в `header`.
   Напомните ученикам об [использовании условий в шаблонах](https://github.com/xlartas/it-compot-backend-methods/blob/main/django-base.md#%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-%D1%86%D0%B8%D0%BA%D0%BB%D0%BE%D0%B2-%D0%B8-%D1%83%D1%81%D0%BB%D0%BE%D0%B2%D0%B8%D0%B9-%D0%B2-%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD%D0%B5)
   и скажите, что `request.user.is_authenticated` возвращает
   `True`/`False`, пусть попробуют сами условно отображать ссылки.
   ```html
   <!-- Вот так -->
   {% if request.user.is_authenticated %} 
   
   {% else %}
   
   {% endif %}
   ```
   `{% if request.user.is_authenticated == Ture %}` для ученика понятнее. 
   ```html
   <!-- header.html -->
   ...
   <ul class="navbar-nav mb-2 mb-lg-0 gap-2">
       <li class="nav-item">
           <a class="nav-link py-0"
              href="{% url 'catalog' %}">
               Catalog
           </a>
       </li>
       {% if request.user.is_authenticated %}
           <li class="nav-item">
               <a class="py-0"
                  href="{% url 'profile' %}">
                   <img width="20" height="20"
                        style="filter: invert(0.75)"
                        src="{% static 'Core/img/user.png' %}" alt="profile">
               </a>
           </li>
           <li class="nav-item my-auto">
               <a class="py-0"
                  href="{% url 'logout' %}">
                   <img width="24" height="24"
                        style="filter: invert(0.75)"
                        src="{% static 'Core/img/logout.png' %}" alt="logout">
               </a>
           </li>
       {% else %}
           <li class="nav-item my-auto">
               <a class="btn btn-secondary py-0"
                  href="{% url 'signin' %}">
                   Sign In
               </a>
           </li>
           <li class="nav-item my-auto">
               <a class="btn btn-secondary py-0"
                  href="{% url 'signup' %}">
                   Sing Up
               </a>
           </li>
       {% endif %}
   </ul>
   ```
   Проверьте, что все корректно отображается.

2. ## Управление доступом и правами пользователей
   Сейчас после входа в аккаунт мы можем перейти на адреса `signup` и `signin`, 
   а если разлогинимся, то сможем перейти в профиль, что неправильно.<br>
   Мы можем проверять есть ли в сессии аутентифицированный пользователь и опираясь на
   это рендерить страницу или перенаправлять или еще что-то.
   
   ```python
   def example(request):                        
       if not request.user.is_authenticated:
           return redirect('login')
       return render(request, 'example.html')
   ```
   ### Применяем эти знания
   > Ставьте `not` где нужно, и не ставьте, где не нужно
   ```python
   # Core/views.py
   ...
   def profile(request):
       if not request.user.is_authenticated:
           return redirect('signin')
       return render(request, 'Core/auth/profile.html')


   def signup(request):
       if request.user.is_authenticated:
           return redirect('profile')
       if request.method == 'POST':
           ...
       return render(request, 'Core/auth/signup.html')
   
   
   def signin(request):
       if request.user.is_authenticated:
           return redirect('profile')
   ...
       
   ```

> Немного свободного времени должно остаться, чтобы догнать, если опаздывали.

Можете пойти дальше или сделать страницу профиля, но это не обязательно.
Примерно так...
```html
{% extends 'Core/base.html' %}
{% load static %}
{% block title %}Shop | Profile{% endblock %}

{% block content %}
    <div class="d-flex flex-column mx-auto" style="width: min-content">
        <div class="d-flex align-items-center">
            <img src="{% static 'Core/img/user.png' %}"
                 style="filter: invert(.9)"
                 width="50" height="50"
                 alt="">
            <h1 class="text-body text-center fw-bold">
                {{ request.user.username }}
            </h1>
        </div>
        <ul>
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


Можно рассказать, что существует множество пакетов расширяющих возможности django.<br>
Например `django-allauth` – это мощная библиотека для Django, предназначенная для облегчения 
процессов аутентификации, регистрации и управления учетными записями пользователей. 
Она предоставляет интеграцию с социальными сетями и другими внешними провайдерами 
аутентификации, что позволяет пользователям регистрироваться и входить в систему с 
помощью своих учетных записей в этих сервисах 
(например, **Google**, **GitHub**, **Telegram**, **Vk**, **Twitter** и т.д.).
Расширенная обработка электронной почты, включая подтверждение электронной почты.

## Подведите итоги.
># git push...