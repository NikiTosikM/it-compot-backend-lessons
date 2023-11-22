# Дополнительные материалы
Можно использовать если осталось время после основного материала урока.

1. ## Смена темы bootstrap
    В bootstrap можно сменить тему одним атрибутом. <br>
    Добавим в `body` атрибут `data-bs-theme="dark"` или `white`.
    ```html
    <body data-bs-theme="dark">...</body>
    <!--или-->
    <body data-bs-theme="white">...</body>
    ```
    > В случае если тема работает не корректно, обратите внимание, что у дочерних элементов цвета 
    не должны сливаться с фоном в той или иной теме, классы 
    черно-белых цветов стоит удалить либо проследить, что они правильно заданы, 
    иначе текст может начать сливаться с фоном.

2. ## Улучшение читабельности названия модели и её объектов в ui(user interface)
    ```python
    class Post(models.Model):
        title = models.CharField(max_length=70)
        image = models.ImageField(upload_to='images/')
        text = models.TextField()
        likes = models.IntegerField(blank=True)
        rating = models.FloatField(blank=True)
        is_published = models.BooleanField(default=True)
        created_at = models.DateTimeField(auto_now_add=True)
        
        class Meta:
            # Название объекта модели для django ui.
            # Например, используется в админке, 
            # чтобы английские слова стали кирилическими.
            # Стоит отметить, что это работает не только для админки. 
            verbose_name = 'Пост' 
            # Тоже самое во множественном числе.
            verbose_name_plural = 'Посты'
        
        # Интерпритация класса как str
        def __str__(self):
            return self.title + ' ' + self.is_published  
            # Например, при выводе через print(объект поста),
            # Будет выводится более читабельная надпись.
    ```