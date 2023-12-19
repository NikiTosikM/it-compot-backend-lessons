# Создание личного плейлиста

В данной методичке, мы создадим новое приложение, где пользователь сможет собрать свой личный плейлист видео.
>Можете если хотите показать, что примерно мы будем делать.<br><br>
![result.png](imgs/result.png)


1. ## Cоздадим новое приложение `playlist`.

   `python manage.py startapp playlist`
2. ## Показываем как можно встроить видео с YouTube.
   - ### Открываем видео, нажимаем поделиться.<br>
      ![result.png](imgs/resend.png) <br><br>

   - ### Нажимаем встроить.<br>
      ![result.png](imgs/insert.png)<br><br>

   - ### Объясняем, что такое `iframe`, и что нужно будет хранить в базе данных только `embed code`.<br><br>
      ![result.png](imgs/iframe.png) <br><br>

3. ## Создадим модель `Video`, где будут храниться название видео и ссылка для его встраивания в `iframe`.
   ```python
   # playlist/models.py
   from django.db import models
   
   class Video(models.Model):
       title = models.CharField(max_length=200)
       embed_code = models.TextField()
       created_at = models.DateTimeField(auto_now_add=True)
   
       def __str__(self):
           return self.title
   ```
   #### Мигрируем модель в db
   `python manage.py makemigrations`<br>
   `python manage.py migrate`

4. ## Зарегистрируем модель в `admin.py` для управления через административную панель.
   ```python
   # playlist/admin.py
   from django.contrib import admin
   from .models import Video
   
   admin.site.register(Video)
   ```
5. ## Создадим представление, которое будет отображать все видео из плейлиста.
   > Используем print при недопонимании.
   ```python
   # playlist/views.py
   from django.shortcuts import render
   from .models import Video
   
   def video_list(request):
       videos = Video.objects.all()
       # print(videos) если нужно...
       return render(request, 'playlist/video_list.html', {'videos': videos})
   ```
6. ## Свяжем `video_list()` с адресом `playlist/video_list/`.
   ```python
   # project_name/urls.py
   from django.urls import path
   from . import views
   
   urlpatterns = [
       path('playlist/video_list/', views.video_list),
   ]
   ```
   
7. ## Создадим несколько объектов Video в админке.
      > Обращаем внимание, что мы храним в бд только часть ссылки `embed_code`, 
        вместо всей ссылки или всего `iframe`.

8. ## Создадим шаблон для отображения видео используя `iframe` и шпаргалку [циклы](https://github.com/xlartas/it-compot-backend-methods/blob/main/django-base.md#%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-%D1%86%D0%B8%D0%BA%D0%BB%D0%BE%D0%B2-%D0%B8-%D1%83%D1%81%D0%BB%D0%BE%D0%B2%D0%B8%D0%B9-%D0%B2-%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD%D0%B5).  
   >Используем Bootstrap, header, footer берем с предыдущей страницы. 

   **`Когда сделаете`**, обратите внимание, что часть кода (*header, footer*) дублируется. 
   Применим `include` для `повторного использования` header и footer.<br>
   Подробно об `include` в [шпаргалке](https://github.com/xlartas/it-compot-backend-methods/blob/main/django-base.md#Include-%D0%B2-%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD%D0%B0%D1%85).
      > Создайте в папке с шаблонами новую папку `includes` 
      и поместите туда файлы `header.html` и `footer.html`. 
      В эти файлы поместим код header'а и footer'а соответственно.
      ### Результат
      ```html
      <!-- playlist/templates/playlist/video_list.html -->
      {% include 'playlist/includes/header.html' %}
      <main>
          {% for video in videos %}
              <div class="card" style="width: 275px;">
                  <!-- iframe руками полностью писать не надо. Копиаруем с youtube. Убираем attrs width и height -->
                  <iframe src="https://www.youtube.com/embed/{{ video.embed_code }}" 
                          frameborder="0" 
                          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                          allowfullscreen></iframe>
              </div>
          {% endfor %}
      </main>
      {% include 'playlist/includes/footer.html' %}
      ```
      ### Более красивый вариант, который можно задать как домашнее задание.
      > Добавляем отображение остальных полей, украшаем карточку.
      ```html
      <!-- playlist/templates/playlist/video_list.html -->
      {% for video in videos %}
          <div class="card rounded-top-3 border-5 border-secondary bg-dark" 
               style="width: 275px;">
              <iframe class="rounded-top-3"
                      src="https://www.youtube.com/embed/{{ video.embed_code }}" 
                      frameborder="0" 
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
              <div class="card-body">
                  <h5 class="card-title text-light">{{ video.title }}</h5>
                  <p class="card-text text-secondary">{{ video.created_at }}</p>
              </div>
          </div>
      {% endfor %}
      ```


Все готово!

## Подведите итоги.