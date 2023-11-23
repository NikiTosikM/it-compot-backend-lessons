# Оформление заказа
Сегодня мы реализуем оформление заказа со страницы подробного просмотра товара.


1. ## Переопределим маршрут `order_create`
    Сделаем его динамическим. Передавать будем `id` `продукта` по которому хотим создать `заказ`.
    > Это повторение того, что делали на прошлом уроке, ученики должны вспомнить сами.
    ```python
    # shop/urls.py
    urlpatterns = [
        ...
        path('order_create/<int:product_id>/', order_create, name='order_create'),
        ...
    ]
    ```
2. ## Доделаем кнопку с оформлением заказа внутри `product_detail.html`
    Добавим `href` который будет вести на оформление заказа для конкретного продукта по его `id`
    > На странице `product_detail.html` доступна переменная `product`, которая содержит как раз нужный нам `id`
    ```html
    <!-- product_detail.html -->
    ...
    <a href="{% url 'order_create' product_id=product.id %}" 
       class="btn fs-4 btn-outline-secondary w-100 mt-3">Оформить заказ</a>
    ...
    ```
    Проверьте, что все работает и кнопка действительно<br>
    перенаправляет нас на адрес `order_create` с верно указанным `id` в адресной строке.
    > Что-то типа http://127.0.0.1:8000/shop/order_create/1/
3. ## Доделаем страницу для создания заказа
    Так как при оформлении заказа нам нужен предпросмотр того, что мы заказываем,
    скопируем код из `product_detail.html` изменив `заголовок h1` и тег `title`.<br><br>

    Так же необходимо создать форму для отправки данных для создания объекта `Order`.<br>
    Вспоминаем, какие поля нам нужны. **Откройте `models.py`(Order) и наглядно посмотрите.**<br>
    * Нужен сам продукт (поле _product_) по которому мы будем оформлять заказ,<br>
      но `input` для него не нужен, так как форма будет отправляться на адрес, который .<br>
      уже будет содержать `id` продукта, а значит мы сможем получить объект продукта по этому `id`.<br>
      > order_create/<int:product_id>/
    * Поле `created_at` заполняется датой автоматически за счет параметра `auto_now_add=True`.<br><br>
    * Таким образом, в форме будет лишь 1 `input` для `delivery_address`.<br><br>

    Проговариваем еще раз зачем нам `post` запрос, чем он отличается от `get`, 
    что существуют и другие, но пока мы их не изучаем, за что отвечает атрибут `action`, зачем атрибут `name` в `input`
    и так далее. <br>
    Это база которую _**нужно**_ понять и запомнить.
    
    ```html
    <!-- order_create.html -->
    {% extends 'shop/base.html' %}
    {% load static %}
    {% block title %}Shop | Order {{ product.name }} {% endblock %}
    
    {% block content %}
        <div class="d-flex gap-3 flex-wrap justify-content-center mx-auto"
             style="max-width: 300px;">
            <div class="d-flex flex-column align-items-start text-center border-0 rounded-4 text-nowrap px-4 py-4"
                 style="width: min-content; box-shadow: 0 0 5px #00000022;">
                <h1 class="text-wrap">Заказ {{ product.name }}</h1>
                <!-- Остальной код из дательного просмотра товара -->
                <span class="fs-5">{{ product.desc }}</span>
                <!-- Формируем динамический адрес до тойже страницы на
                     которой мы сейчас, но отправлять будем уже post запрос.
                     Адрес должен содержать id текущего продукта, не забываем. -->
                <form action="{% url 'order_create' product_id=product.id %}"
                      class="d-flex flex-column justify-content-center mx-auto mt-3"
                      method="post">{% csrf_token %}
                    <!-- required атрибут не позволит отправить форму пока данный input не будет заполнен. -->
                    <input name="delivery_address" type="text"
                           class="form-control"
                           required 
                           placeholder="Адрес доставки">
                    <button type="submit"
                            class="btn fs-4 btn-outline-secondary w-100 mt-3">
                        Заказать</button>
                </form>
            </div>
        </div>
    {% endblock %}
    ```
    Если попробуем нажать на кнопку оформить заказ на странице детального просмотра, то увидим ошибку.<br>
    Пусть ученики подумают, почему так происходит.<br>
    Внутри `order_create.html` мы используем переменную `product`, но разве мы её передали при рендере в шаблон? Нет.<br>
    Даём ученикам самим передать переменную в шаблон как мы делали в `def product_detail`.
    ```python
    # shop/views.py
    def order_create(request, product_id):
        product = Product.objects.get(id=product_id)
        return render(request, 'shop/order_create.html', {
            'product': product
        })
    ```
4. ## Принимаем и сохраняем данные
    Теперь при отправке формы страница просто перезагружается. Почему?<br>
    Какой тип запроса мы сейчас обрабатываем в функции `def order_create`?<br>
    `GET`, а форму мы отправляем через `POST`. <br>
    А так как мы загружаем страницу и отправляем данные по одному и тому же адресу,<br>
    значит обработка данных `POST` запроса должна быть в той же функции, что и рендер страницы.<br>
    Мы это уже делали с магическим числом и созданием нового видео в предыдущем проекте.<br>
    Вспоминаем разделы шпаргалки 
    [Обмен данными клиент - сервер](https://github.com/xlartas/it-compot-backend-methods/blob/main/django-base.md#%D0%BE%D0%B1%D0%BC%D0%B5%D0%BD-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8-%D0%BA%D0%BB%D0%B8%D0%B5%D0%BD%D1%82----%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80)
    и 
    [Сохранение объектов в бд](https://github.com/xlartas/it-compot-backend-methods/blob/main/django-base.md#orm)
    ```python
    # shop/views.py
    def order_create(request, product_id):
        product = Product.objects.get(id=product_id)
        # Проверяем тип запроса и если пост то сохраняем продукт,
        # заполняя нужные поля.
        # created_at заполняется автоматически
        if request.method == 'POST':
            Order.objects.create(
                product=product,
                delivery_address=request.POST.get('delivery_address')
            )
        return render(request, 'shop/order_create.html', {
            'product': product
        })
    ```
    Теперь заказ создаётся и мы попадаем на туже саму страницу с оформлением заказа,<br>
    но хотелось бы, чтобы нас перенаправляло на страницу с заказами.
5. ## Делаем редирект с аргументами
    Вспоминаем как делаются [редиректы]()
    ```python
    # shop/views.py
    def order_create(request, product_id):
        product = Product.objects.get(id=product_id)
        # Проверяем тип запроса и если пост то сохраняем продукт,
        # заполняя нужные поля.
        # created_at заполняется автоматически
        if request.method == 'POST':
            Order.objects.create(
                product=product,
                delivery_address=request.POST.get('delivery_address')
            )
            # Редирект выполняем при POST запросе, когда создан новый заказ
            return redirect('orders')
        # А при GET просто рендерим страницу с созданием заказа
        return render(request, 'shop/order_create.html', {
            'product': product
        })
    ```
## Все готово.
Если осталось время можно улучшить код украсив сайт или дополнив шапку рабочими ссылками.<br><br>
И _**только**_ для хардов объясняем, чтобы не путать лишний раз более слабых учеников, <br>
что в поле `product` модели `Order` хранится `цифра` - `id` связанного продукта,<br>
а значит поле `product` можно заполнить `product_id` переданным через `URL`,<br>
а значит поле продукт нужно получать только при рендере страницы с заказом.<br>
```python
# shop/views.py
def order_create(request, product_id):
    if request.method == 'POST':
        Order.objects.create(
            product=product_id, # или product_id=product_id
            delivery_address=request.POST.get('delivery_address')
        )
        return redirect('orders')
    product = Product.objects.get(id=product_id)
    return render(request, 'shop/order_create.html', {
        'product': product
    })
```    
># git push...