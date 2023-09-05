# Введение в БД и административную панель Django
Будем начинать мини-проект 'Личный блог'

## Начало
1. Создание нового приложения blog
2. Объясните еще раз разницу между проектом и приложением в Django.
3. Объясните, что такое база данных и какие задачи она решает в веб-разработке.
4. Расскажите, как Django устраивает взаимодействие с базой данных SQLite3.
5. Показываем и подробно объясняем [этот раздел](https://github.com/Artasov/itcompot-methods/blob/main/django-base.md#%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5-%D0%BF%D1%80%D0%BE%D1%81%D1%82%D0%B5%D0%B9%D1%88%D0%B5%D0%B9-%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D0%B8-%D0%B4%D0%BB%D1%8F-%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D0%B0) на нашей вспомогательной страничке.
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
7. Подключите административную панель Django.
   ```python
   # blog/admin.py
   from django.contrib import admin
   from .models import Post
   
   @admin.register(Post)
   class PostAdmin(admin.ModelAdmin):
       list_display = ('title', 'text')
   ```
8. Создайте staff пользователя и откройте административную панель.
9. Создайте объекты постов через административную панель, чтобы убедиться, что ваша <br>
   модель функционирует.
10. Постепенно добавляйте новые поля и связи между моделями, повторяя процесс миграции, <br>
    чтобы продемонстрировать изменения в базе данных.
11. Доделываем до такого вида, постепенно обновляя уже созданные объекты.
    ```python
    class Post(models.Model):
    title = models.CharField(max_length=70)
    text = models.TextField()
    likes = models.IntegerField(blank=True)
    rating = models.FloatField(blank=True)
    image = models.ImageField(upload_to='images/')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title
    ```

># git push...