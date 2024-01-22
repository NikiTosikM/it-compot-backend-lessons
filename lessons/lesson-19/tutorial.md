# 



## 

3. ## Вспомним про модели
   * Очевидно, что заказ должен быть связан не только с продуктом, но и с пользователем.<br>
     Вспомните, как вы привязывали продукт(через ForeignKey) к заказу и как импортировали 
     модель пользователя в `Core/views.py`<br>
     Напомните ученикам основную информацию про модели и таблицы в бд.
     В теории ученики должны сами написать это.
     ```python
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
     Исправляем, используя полученные знания. Заодно сделаем, чтобы 
     оформлять заказ и просматривать страницу с заказами мог только 
     авторизированный пользователь.
     ```python
     def orders(request):
         if not request.user.is_authenticated:
             return redirect('signin')
         orders_ = Order.objects.all()
         return render(request, 'shop/orders.html', {'orders': orders_})

     def order_create(request, product_id):
         if not request.user.is_authenticated:
             return redirect('signin')
         
         if request.method == 'POST':
             Order.objects.create(
                 user=request.user,
                 product_id=product_id,
                 delivery_address=request.POST.get('delivery_address')
             )
             return redirect('orders')
         return render(request, 'shop/order_create.html', {
             'product': Product.objects.get(id=product_id)
         })
     ```