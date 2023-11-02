# Введение в БД и административную панель Django
### Будем начинать мини-проект **Блог**

## Начало
1. Создайте новое приложение `blog`

    `python manage.py startapp blog`
2. Объясните еще раз разницу между проектом и приложением в Django.
3. Объясните, что такое база данных и какие задачи она решает в веб-разработке.
4. Расскажите, как Django взаимодействует с базой данных `SQLite3` (она по умолчанию).
5. Показываем и подробно объясняем [этот раздел](https://github.com/xlartas/it-compot-backend-methods/blob/main/django-base.md#%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5-%D0%BF%D1%80%D0%BE%D1%81%D1%82%D0%B5%D0%B9%D1%88%D0%B5%D0%B9-%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D0%B8-%D0%B4%D0%BB%D1%8F-%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D0%B0) на нашей вспомогательной страничке.
## Модели

1. Создайте модель для постов, начиная с простейших полей, таких как заголовок и текст.
    ```python
    # blog/models.py
    class Post(models.Model):
        title = models.CharField(max_length=70)
        text = models.TextField()
    ```
2. Создайте миграции для вашей модели с помощью команды <br>

    `python manage.py makemigrations`

3. Исполнение файлов миграций с помощью команды 

   `python manage.py migrate.`

4. Установим расширение `SQLite Viewer` в VS Code.
5. Показываем, что произошло внутри базы данных.
6. Объясните, зачем нужна административная панель, и как она облегчает управление данными.
7. Зарегистрируем модель в `admin.py` для управления через административную панель.
   ```python
   # blog/admin.py
   from django.contrib import admin
   from .models import Post
   
   @admin.register(Post)
   class PostAdmin(admin.ModelAdmin):
       # Тут указываем в кортеже те поля которые будут видны при групповом отображении.
       list_display = ('title', 'text')
   ```
8. Создайте staff пользователя и откройте административную панель.
   
   `python manage.py createsuperuser`

9. Создайте объекты постов через административную панель, чтобы убедиться, что ваша <br>
   модель функционирует.

10. Доделываем до такого вида, постепенно обновляя уже созданные объекты. <br>
    **Если easy уровень то 2-3 поля на первый раз более чем достаточно. class Meta и __str_\_ можно им тоже не показывать.**

    ```python
    class Post(models.Model):
        title = models.CharField(max_length=70)
        image = models.ImageField(upload_to='images/')
        text = models.TextField()
        likes = models.IntegerField(blank=True)
        rating = models.FloatField(blank=True)
        is_published = models.BooleanField(default=True)
        created_at = models.DateTimeField(auto_now_add=True)
    ```
    > Не забываем создать и выполнить миграции

    Скорее всего при миграциях будет ошибка о нехватке библиотеки Pillow для использования ImageField<br>
    Установите эту библиотеку `pip install Pillow`<br><br>

11. Рассказываем, что для корректного использования медиафайлов(картинок через imagefield),<br>
    нужно определить адреса для этих медиафайлов. То есть сделать так, чтобы каждая картинка <br>
    или любой другой медиафайл были доступны по своему маршруту.<br><br>

12. Отредактируем `settings.py` и `корневые urlpatterns`
    ```python
    # project_name/settings.py
    ...
    # Адрес по которому будут доступные media.
    # Вы можете проверить доступ после добавления первого поста перейдя по ссылке.
    # http://127.0.0.1:8000/MEDIA_URL/images/IMAGE_NAME/
    MEDIA_URL = '/media/'
    # Локальный адрес хранения media.
    # Корневая папка проекта с manage.py файлом + 'media'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    ...
    ```
    ```python
    # project_name/urls.py
    urlpatterns = [
        ...,
        ...,
        ...,
    ]
    #  На сервере media обслуживает серверная служба, 
    #  а не django, поэтому только при debug мы включаем 
    #  обслуживание на стороне django, добавляя адреса для media.
    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    ```
#### Если осталось время доделывайте git с прошлого занятия.

># git push...