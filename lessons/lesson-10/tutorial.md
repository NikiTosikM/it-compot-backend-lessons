# Магазин
Сегодня мы начнем создавать свой личный магазин. <br>
Подумайте на какую тематику он будет.

1. ## Создание нового приложения
   Для начала создадим новое приложение с названием shop, выполнив следующую команду в терминале:

   `python manage.py startapp shop`

2. ## Создание моделей
   Перейдем к созданию моделей в файле models.py вашего нового приложения.<br>
   Пусть ученики продумают, какие поля будут в их моделях.<br><br>

   Заказ должен относится к определенному товару, поэтому мы будем использовать <br>
   специальное поле (`ForeignKey / Внешний ключ`) которое будет `ссылаться` на определенный объект модели `Product`.<br>
   В действительности в базе данных в этом поле будет лежать `primary_key`(в нашем случае `id`) связанного объекта.
   ```python
   # shop/models.py
   class Product(models.Model):
       name = models.CharField(max_length=100)
       desc = models.TextField()
       price = models.FloatField()
       rating = models.PositiveIntegerField()
       stock = models.PositiveIntegerField()  # в наличии кол-во
       is_available = models.BooleanField(default=True)
   
   class Order(models.Model):
       product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
       delivery_address = models.CharField(max_length=255)
       created_at = models.DateTimeField(auto_now_add=True)
   ```
3. ## Создание представлений, шаблонов и маршрутов.
   Продумайте какие адреса и страницы у вас будут.
   * ### Создание шаблонов
      Cоздадим пока что пустые шаблоны HTML для каждой страницы. 
      ```sh
      shop/templates/shop/catalog.html
      shop/templates/shop/orders.html
      shop/templates/shop/order_create.html
      ```
     
   * ### Создание представлений (views)
     ```python
     # shop/views.py
     def catalog(request):
         # <h1>Каталог товаров</h1>
         return render(request, 'shop/catalog.html')
     
     def orders(request):
         # <h1>Заказы</h1>
         return render(request, 'shop/orders.html')
     
     def order_create(request):
         # <h1>Заказать</h1>
         return render(request, 'shop/order_create.html')
     ```
    
   * ### Создание маршрутов
       Обратите внимание, что `project_name/urls.py` собраны все маршруты до разных приложений.<br>
       Было бы гораздо лучше если бы у каждого приложения был свой urls.py, и это возможно.<br>
       Создайте файл urls.py в папке приложения shop и добавьте в него маршруты `catalog` `orders` `order_create`.
    
       ```python
       # shop/urls.py
       from .views import * # импортируем все из файла
       
       urlpatterns = [
           path('catalog/', catalog, name='catalog'),
           path('orders/', orders, name='orders'),
           path('order_create/', order_create, name='order_create'),
       ]
       ```
       ####  Теперь, когда у нас есть свой файл shop/urls.py для приложения,<br>мы можем включить его в корневой файл urls.py проекта с помощью функции `include`.
       ```python
       # project_name/urls.py
       from django.urls import path, include
       urlpatterns = [
           ...
           path('shop/', include('shop.urls')),  # включаем URL-адреса приложения shop
       ]
       # По итогу мы получим следующие адреса:
       # http://127.0.0.1:8000/shop/catalog/
       # http://127.0.0.1:8000/shop/orders/
       # http://127.0.0.1:8000/shop/order_create/
       ```
       >Здесь мы используем include для включения URL-адресов приложения shop в общие URL-адреса проекта, что позволяет нам организовывать URL-адреса более структурированно и читаемо.

### Если осталось время пусть ученики создадут свои urls.py для каждого приложения и верно распределят адреса.

># git push...