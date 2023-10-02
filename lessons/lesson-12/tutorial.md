# Шаблонизация вывода товаров и заказов

Сегодня мы седлаем вывод всех товаров и заказов на отдельных страницах.
Перед началом создайте несколько товаров и заказов через админку.
> По 3 штуки достаточно.

1. ## Отображение одного товара
   Вспоминаем как можно 
   [передавать переменные в шаблон](https://github.com/Artasov/itcompot-methods/blob/main/django-base.md#%D0%BF%D0%B5%D1%80%D0%B5%D0%B4%D0%B0%D1%87%D0%B0-%D0%BF%D0%B5%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D1%8B%D1%85-%D0%B2%D0%BD%D1%83%D1%82%D1%80%D1%8C-%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD%D0%B0)
   и брать 
   [объекты](https://github.com/Artasov/itcompot-methods/blob/main/django-base.md#orm)
   из базы данных.<br>
   Получаем 1 товар и отображаем его на странице.
   ```python
   # shop/views.py
   from .models import Product
   
   
   def catalog(request):
       product = Product.objects.get(id=0)
       # или 
       product = Product.objects.first()
       # или 
       product = Product.objects.last()
       return render(request, 'shop/catalog.html', {'product': product})
   ```
   
   Используем переданную переменную в шаблоне.
    > Отображайте меньше полей если понимаете, что ученики не успеют.
    ```html
    <!-- shop/catalog.html  -->
   ...
    <div class="card border-0 rounded-4" 
         style="width: 250px; box-shadow: 0 0 5px #00000022;">
        <img src="{{ product.image.url }}" 
             class="card-img-top rounded-4 mt-3" alt="{{ product.name }}">
        <div class="card-body d-flex flex-column justify-content-center">
            <span class="card-text align-items-start d-flex">
                <span class="fs-2 fw-bold">{{ product.price }} ₽</span>
                <!-- Можно добавить условие для отображения скидки -->
                {% if product.discount %}
                    <span class="text-danger fs-6">-{{ product.discount }}%</span>
                {% endif %}
            </span>
            <h3 class="card-title fs-6">{{ product.name }}</h3>
            <div class="d-flex gap-1 mb-3">
                <!-- Используйте рейтинг товара для отображения звезд.
                     Делаем цикл в кавычках пишем ЛЮБУЮ строку из 5 символов.  
                     Таким образом мы просто делаем цикл из 5 итераций 
                     т.к. максимальный рейтинг - 5, соответственно звезд 
                     будет тоже не больше 5. -->
                <!-- Если номер итерации меньше чем число рейтинга в 
                     данном объекте продукта, добавляем картинку звездочки,
                     иначе добавляем такую же картинку, но делаем её серой. -->
                
                {% for star in "Пять." %} 
                    Картинку нужно скачать
                    {% if forloop.counter <= product.rating %}
                        <img width="20" height="20" 
                             src="{% static 'shop/img/rating_star.png' %}" 
                             alt="star">
                    {% else %}
                        <img width="20" height="20" 
                             src="{% static 'shop/img/rating_star.png' %}"
                             style="filter: grayscale(1);" 
                             alt="star">
                    {% endif %}
                {% endfor %}
            </div>
            <!-- Условие для отображения кнопки -->
            {% if product.is_available %}
            <button class="btn btn-outline-secondary text-dark">В корзину</button>
            {% else %}
            <button class="btn btn-outline-secondary text-dark" disabled>Нет в наличии</button>
            {% endif %}
            <small class="text-black-50 mt-2">
                <!-- Описание товара -->
                {{ product.desc }}<br>
            </small>
        </div>
    </div>
    ```
2. ## Самостоятельно делаем то же самое с отображением заказа.
   ```python
   from .models import Product, Order
   
   
   def orders(request):
         order = Order.objects.first()
         return render(request, 'shop/orders.html', {'order': order})
   ```
   > Выводим любые поля, можно даже картинку из продукта хардам задать вывести.
   ```html
    <!-- shop/orders.html  -->
    {% extends 'shop/base.html' %}
    {% load static %}
    {% block title %}Shop | ORDERS{% endblock %}
    
    {% block content %}
        <h1 class="text-dark text-center fw-bold mb-4">Заказы</h1>
        <div class="d-flex gap-3 flex-wrap justify-content-center mx-auto"
             style="max-width: 800px;">
            <div class="d-flex flex-column text-center border-0 rounded-4 text-nowrap px-4 py-2"
                 style="width: min-content; box-shadow: 0 0 5px #00000022;">
                <span class="align-self-start fw-bold fs-5">{{ order.id }}</span>
                <span>{{ order.product.name }}</span>
                {# обрезаем 10 слов #}
                <span>{{ order.delivery_address|truncatewords:6 }}</span>
                <span>{{ order.created_at }}</span>
            </div>
        </div>
    {% endblock %}
    ```
3. ## Отобразим сразу несколько заказов используя [циклы в шаблонах](https://github.com/Artasov/itcompot-methods/blob/main/django-base.md#%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-%D1%86%D0%B8%D0%BA%D0%BB%D0%BE%D0%B2-%D0%B8-%D1%83%D1%81%D0%BB%D0%BE%D0%B2%D0%B8%D0%B9-%D0%B2-%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD%D0%B5).
    Для начала нужно передавать в шаблон не 1 заказ, а несколько. Будем брать все.<br>
    Возвращаемся к [ORM](https://github.com/Artasov/itcompot-methods/blob/main/django-base.md#orm).
    ```python
    # shop/views.py
    def orders(request):
        # _ чтобы не совпадало с именем функции.
        orders_ = Order.objects.all()
        return render(request, 'shop/orders.html', {'orders': orders_})
    ```
    ```html
    <!-- shop/orders.html  -->
    ...
    {% for order in orders %}
        <div class="d-flex flex-column text-center border-0 rounded-4 text-nowrap px-4 py-2"
             style="width: min-content; box-shadow: 0 0 5px #00000022;">
            <span class="align-self-start fw-bold fs-5">{{ order.id }}</span>
            <span>{{ order.product.name }}</span>
            <span>{{ order.delivery_address|truncatewords:6 }}</span>
            <span>{{ order.created_at }}</span>
        </div>
    {% endfor %}
    ...
    ```
4. ## Просим учеников самим сделать то же самое с товарами.
   ```python
    # shop/views.py
    def catalog(request):
        all_products = Product.objects.all()
        return render(request, 'shop/catalog.html', {'products': all_products})
    ```
   
    ```html
    <!-- shop/catalog.html  -->
    {% extends 'shop/base.html' %}
    {% load static %}
    {% block title %}Shop | CATALOG{% endblock %}
    
    {% block content %}
        <h1 class="text-dark text-center fw-bold mb-4">Каталог</h1>
        <div class="d-flex gap-3 flex-wrap justify-content-center mx-auto" 
             style="max-width: 800px;">
            {% for product in products %}
                <div class="card border-0 rounded-4"
                 ...
                </div>
            {% endfor %}
        </div>
    {% endblock %}
    ```
   
#### Если все успели, добавьте в шапку удобную навигацию к товарам и заказам

># git push...