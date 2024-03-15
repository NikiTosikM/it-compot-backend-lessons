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

2. ## Улучшение читабельности названия модели и её объектов в `ui` _(user interface)_
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
            # или return f'{self.title} {self.is_published}' 
    
            # Например, при выводе через print(объект поста),
            # Будет выводится более читабельная надпись.
    ```
3. ## У всех разная TimeZone, а по умолчанию UTC+0.
   Изменять Timezone в django можно изменяя переменную `TIME_ZONE` в `settings.py`.<br>
   Тогда даты будут отображаться учитывая timezone, а не по UTC+0
   > Убедитесь, что `USE_TZ = True`

   ### Значения для разных timezone
   * `UTC` - Coordinated Universal Time (UTC+0)
   * `Europe/Moscow` - Московское время (UTC+3)
   * `Europe/Kaliningrad` - Восточноевропейское время (UTC+2)
   * `Europe/Samara` - Самарское время (UTC+4)
   * `Asia/Yekaterinburg` - Екатеринбургское время (UTC+5)
   * `Asia/Omsk` - Омское время (UTC+6)
   * `Asia/Krasnoyarsk` - Красноярское время (UTC+7)
   * `Asia/Irkutsk` - Иркутское время (UTC+8)
   * `Asia/Yakutsk` - Якутское время (UTC+9)
   * `Asia/Vladivostok` - Владивостокское время (UTC+10)
   * `Asia/Magadan` - Магаданское время (UTC+11)
   * `Asia/Kamchatka` - Камчатское время (UTC+12)
   * `Europe/London` - Великобритания (UTC+0, летом UTC+1)
   * `Europe/Paris` - Центральноевропейское время (UTC+1, летом UTC+2)
   * `Europe/Berlin` - Центральноевропейское время (UTC+1, летом UTC+2)
   * `Asia/Tokyo` - Японское время (UTC+9)
   * `Asia/Shanghai` - Китайское стандартное время (UTC+8)
   * `Asia/Dubai` - Стандартное время ОАЭ (UTC+4)
   * `America/New_York` - Восточное стандартное время (UTC-5, летом UTC-4)
   * `America/Chicago` - Центральное стандартное время (UTC-6, летом UTC-5)
   * `America/Denver` - Горное стандартное время (UTC-7, летом UTC-6)
   * `America/Los_Angeles` - Тихоокеанское стандартное время (UTC-8, летом UTC-7)
   * `America/Sao_Paulo` - Бразильское время (UTC-3, летом UTC-2)
   * `Australia/Sydney` - Восточное стандартное время Австралии (UTC+10, летом UTC+11)
   * `Pacific/Auckland` - Новозеландское время (UTC+12, летом UTC+13)
   * `Asia/Kolkata` - Индийское стандартное время (UTC+5:30)
   * `Asia/Bangkok` - Индокитайское время (UTC+7)
   * `Asia/Seoul` - Корейское стандартное время (UTC+9)
   * `Asia/Singapore` - Сингапурское стандартное время (UTC+8)
   * `Africa/Johannesburg` - Южноафриканское стандартное время (UTC+2)
   
4. ## Управление доступом и правами пользователей
   Мы можем проверять есть ли в сессии аутентифицированный пользователь и опираясь на
   это рендерить страницу или перенаправлять или еще что-то.
   
   ```python
   def example(request):                        
       if not request.user.is_authenticated:
           return redirect('login')
       return render(request, 'example.html')
   ```
   
   Однако в django есть встроенный декоратор, делающий то же самое за нас.<br>
   Объясните вкратце, что такое декоратор и как он работает.
   ```python
   from django.contrib.auth.decorators import login_required
   
   # Указываем имя патерна на который нас перенаправит если мы не аутентифицированы.
   @login_required(login_url='pattern_name')
   def example(request):
       return render(request, 'example.html')
   ```