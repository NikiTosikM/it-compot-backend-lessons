# Вспомнаем про модели и продолжаем работать с пользователями


1. ## Доделаем систему заказов
   * Очевидно, что заказ должен быть связан не только с продуктом, но и с пользователем.<br>
     Вспомните, как вы привязывали продукт(через `ForeignKey`) к заказу и как импортировали 
     модель пользователя в `Core/views.py`<br>
     Напомните ученикам основную информацию про модели и таблицы в бд.
     В теории ученики должны сами написать это.
     ```python
     # shop/models.py
     from django.contrib.auth.models import User
     ...
     class Order(models.Model):
         user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
         product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
         delivery_address = models.CharField(max_length=255)
         created_at = models.DateTimeField(auto_now_add=True)
     ```
     Напомните зачем и что такое миграционные файлы. Сделайте и примените их.<br>
     ```python manage.py makemigrations```<br>
     ```python manage.py migrate```<br><br>
   
   * Отмечаем, что заказ теперь будет создаваться неправильно.<br>
     Исправляем. Заодно сделаем, чтобы оформлять заказ и просматривать 
     страницу с заказами мог только авторизированный пользователь.
     ```python
     # shop/views.py
     ...
     def orders(request):
         if not request.user.is_authenticated: <-------------
             return redirect('signin')         <-------------
     
         orders_ = Order.objects.all()
         return render(request, 'shop/orders.html', {'orders': orders_})

     def order_create(request, product_id):
         if not request.user.is_authenticated: <-------------
             return redirect('signin')         <-------------
         
         if request.method == 'POST':
             Order.objects.create(
                 user=request.user,            <------------- 
                 # user=request.user.id,       <------------- 
                 # user_id=request.user,       <-------------
                 # user_id=request.user.id,    <-------------
                 # Разное написание одного и того же
                 product_id=product_id,
                 delivery_address=request.POST.get('delivery_address')
             )
             return redirect('orders')
         return render(request, 'shop/order_create.html', {
             'product': Product.objects.get(id=product_id)
         })
     ```
     Стоит напомнить, что в `ForeignKey` поле хранятся первичные ключи 
     связанной таблицы, в нашем случае цифры, и когда мы пишем `user=request.user` 
     django понимает, что в поле user нужно положить не весь объект, а его первичный ключ(id).
     Можете скинуть скриншоты разных вариаций написания и сказать, что мы очень 
     поверхностно касаемся использования ORM системы.
     
    
3. ## Используем `filter`
    Создайте заказы от имени разных пользователей. <br>
    На странице с заказами пользователь видит все заказы. <br>
    А должен только свои.<br>
    Используя раздел [ORM](https://github.com/xlartas/it-compot-backend-methods/blob/main/django-base.md#orm)
    в шпаргалке пусть ученики сами попытаются добиться верного поведения.
    ```python
    # shop/views.py
    ...
    def orders(request):
        if not request.user.is_authenticated: 
            return redirect('signin')        
        
        # orders_ = Order.objects.all() было
        orders_ = Order.objects.filter(user=request.user) # стало
        return render(request, 'shop/orders.html', {'orders': orders_})
    ```