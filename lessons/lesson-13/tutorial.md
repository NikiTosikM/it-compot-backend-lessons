# Рендер внутренних URL и создание динамических ссылок в Django

Сегодня мы научимся рендерить внутренние URL в шаблонах Django и создавать 
динамические URL на примере страницы с отображением конкретного заказа и товара. 
Сначала сделаем вместе один пример, затем вы сделаете то же самое на другом примере сами.

**Можете показать раздел в 
[шпаргалке](https://github.com/xlartas/it-compot-backend-methods/blob/main/django-base.md#%D0%B4%D0%B8%D0%BD%D0%B0%D0%BC%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5-%D0%BC%D0%B0%D1%80%D1%88%D1%80%D1%83%D1%82%D1%8B),
если хотите.**

1.  ## Создание URL для отображения конкретного товара
    Мы хотим добиться поведения при котором по запросу<br>
    `GET http://127.0.0.1:8000/shop/product/1/` выводилась<br> 
    бы информация о товаре с `id = 1`. То есть цифра в конце адреса<br>
    в данном случае обозначает `id` того товара, который мы хотим получить.<br><br>

    Для начала, необходимо определить URL-путь для страницы товара в `urls.py`:
    
    ```python
    # shop/urls.py
    urlpatterns = [
        ...
        path('shop/product/<int:id>/', views.product_detail),
    ]
    ```
    Здесь `<int:id>` – это динамическая часть URL, 
    которая передает id товара в виде целого числа в 
    функцию указанного представления `product_detail`.

2.  ## Создадим представление `product_detail`
    ```python
    # shop/views.py
    def product_detail(request, id):  # В переменную id попадет <int:id>.
        # Если GET http://127.0.0.1:8000/shop/product/1/
        # Тогда id будет равен 1.
        product = Product.objects.get(id=id)
        # Взяли продукт с id=1 и передаем его в шаблон
        return render(request, 'shop/product_detail.html', {'product': product})
    ```

3.  ## Создадим шаблон `product_detail`
    Можем частично скопировать с каталога и немного изменить.
    Обратите внимание, что в примере ниже название 
    вкладки содержит название товара.
    ```html
    <!-- shop/product_detail.html  -->
    {% extends 'shop/base.html' %}
    {% load static %}
    {% block title %}Shop | {{ product.name }} {% endblock %}
    
    {% block content %}
        <div class="d-flex gap-3 flex-wrap justify-content-center mx-auto"
             style="max-width: 300px;">
            <div class="d-flex flex-column align-items-start text-center border-0 rounded-4 text-nowrap px-4 py-4"
                 style="width: min-content; box-shadow: 0 0 5px #00000022;">
                <h1 class="text-wrap">{{ product.name }}</h1>
                <img src="{{ product.image.url }}" alt="">
                <span class="d-flex mt-auto">
                    <span class="fs-2 fw-bold">{{ product.price }} ₽</span>
                    {% if product.discount %}
                        <span class="text-danger fs-6">-{{ product.discount }}%</span>
                    {% endif %}
                </span>
                <div class="d-flex gap-1 mb-2">
                    {% for star in "*****" %}
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
                <span class="fs-5">В наличии: {{ product.stock }}</span>
                <span class="fs-5">{{ product.desc }}</span>
                <button class="btn fs-4 btn-outline-secondary w-100 mt-3">Оформить заказ</button>
            </div>
        </div>
    {% endblock %}
    ```
    **Проверьте, что все работает**


4.  ## Рендер URL в шаблоне
    Нам бы хотелось переходить на страницу товара из 
    каталога, это более удобно.<br>
    Используем тег `{% url 'pattern_name' %}`.<br>
    Данный тэг после рендера шаблона (выполнении функции `render()` во views) 
    заменится на маршрут соответствующий `name=pattern_name`.<br>
    Вспоминаем, что такое 
    **[имена маршрутов](https://github.com/xlartas/it-compot-backend-methods/blob/main/django-base.md#%D0%A4%D0%BE%D1%80%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-%D0%B2%D0%BD%D1%83%D1%82%D1%80%D0%B5%D0%BD%D0%BD%D0%B8%D1%85-%D0%BC%D0%B0%D1%80%D1%88%D1%80%D1%83%D1%82%D0%BE%D0%B2-%D0%B2-%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD%D0%B5)**
    делаем каждый товар в каталоге ссылкой на просмотр 
    подробной информации о товаре.
    
    ```html
    <!-- shop/catalog.html -->
    ...
    {% for product in products %}
        <!-- Генерируем ссылку с указанием id данного товара.-->
        <a href="{% url 'product_detail' id=product.id %}"
           class="card border-0 rounded-4"
           style="width: 250px; box-shadow: 0 0 5px #00000022;">
            ...
        </a>
    {% endfor %}
    ...
    ```
    Здесь `product_detail` – это имя URL-паттерна, 
    который мы определили в urls.py, и `id=product.id`
    передает `id` каждого товара в этот URL-путь. 
    Теперь при нажатии на товар в каталоге, пользователя 
    будет перенаправлять на страницу подробного просмотра товара.<br><br>
    
    Текст на товаре станет подчеркнутым. Я думаю стоит ученикам самим
    попробовать загуглить и найти нужный класс.
    По первой ссылке stackover по запросу `Как убрать подчеркивание bootstrap`  
    правильный вариант. Добавляем найденный класс к ссылке.
    ```html
    <!-- shop/catalog.html -->
    ...
    <a href="{% url 'product_detail' id=product.id %}"
       class="card border-0 rounded-4 text-decoration-none"
       style="width: 250px; box-shadow: 0 0 5px #00000022;">
        ...
    </a>
    ```

5.  ## Добавляем ссылку на товар в заказы.
    Сейчас в заказе отображается только имя товара.<br>
    Пусть ученики сделают сами, чтобы <br>
    при нажатии на имя товара на странице заказов, <br>
    пользователя перенаправляло на страницу товара.
    
    ```html
    {% for order in orders %}
        <div class="d-flex flex-column text-center border-0 rounded-4 text-nowrap px-4 py-2"
             style="width: min-content; box-shadow: 0 0 5px #00000022;">
            <span class="align-self-start fw-bold fs-5">{{ order.id }}</span>
    
            <a href="{% url 'product_detail' id=order.product.id %}">
                {{ order.product.name }}
            </a>
    
            <span>{{ order.delivery_address|truncatewords:6 }}</span>
            <span>{{ order.created_at }}</span>
        </div>
    {% endfor %}
    ```

Если осталось время, переделайте шапку чтобы в навигации 
были ссылки на заказы и каталог.
># git push...