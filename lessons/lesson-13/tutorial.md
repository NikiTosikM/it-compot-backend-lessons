# Рендер внутренних URL и создание динамических ссылок в Django

Сегодня мы научимся рендерить внутренние URL в шаблонах Django и создавать 
динамические URL на примере страницы с отображением конкретного заказа и товара. 
Сначала сделаем вместе один пример, затем вы сделаете то же самое на другом примере сами.

**Можете показать раздел в 
[шпаргалке](https://github.com/Artasov/itcompot-methods/blob/main/django-base.md#%D0%B4%D0%B8%D0%BD%D0%B0%D0%BC%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5-%D0%BC%D0%B0%D1%80%D1%88%D1%80%D1%83%D1%82%D1%8B),
если хотите.**

1.  ## Создание URL для отображения конкретного товара
    Для начала, необходимо определить URL-путь для страницы товара в urls.py:
    
    ```python
    # shop/urls.py
    from django.urls import path
    from . import views
    
    urlpatterns = [
        path('product/<int:id>/', views.product_detail, name='product_detail'),
    ]
    ```
    Здесь `<int:id>` – это динамическая часть URL, 
    которая передает id товара в виде целого числа в 
    функцию указанное представление `product_detail`.

2.  ## Создадим представление `product_detail`
    ```python
    # shop/views.py
    from django.shortcuts import get_object_or_404, render
    from .models import Product
    
    def product_detail(request, id):  # В переменную id попадет <int:id>.
        # http://127.0.0.1:8000/shop/product/1/
        # Тогда id будет равный 1.
        product = Product.objects.get(id=id)
        return render(request, 'shop/product_detail.html', {'product': product})
    ```

3.  ## Создадим шаблон `product_detail`

    ```html
    <!-- shop/product_detail.html  -->
    {% extends 'shop/base.html' %}
    {% load static %}
    {% block title %}Shop | {{ product.name }} {% endblock %}
    
    {% block content %}
        <h1 class="text-dark text-center fw-bold mb-4">
            {{ product.name }}
        </h1>
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

Рендер URL в шаблоне
Для того чтобы создать ссылку на страницу товара в другом шаблоне, используем тег {% url %}:

html
Copy code
<!-- shop/templates/shop/catalog.html -->
{% for product in products %}
    <a href="{% url 'product_detail' id=product.id %}">{{ product.name }}</a>
{% endfor %}
Здесь 'product_detail' – это имя URL-пути, который мы определили в urls.py, и id=product.id передает id каждого товара в этот URL-путь.

Самостоятельная работа: Страница заказа
Теперь попробуйте сделать то же самое для страницы заказа:

Определите URL-путь в urls.py.

Создайте представление order_detail в views.py.

Создайте шаблон order_detail.html.

Рендерите ссылки на страницу заказа в другом шаблоне, используя тег {% url %}.

Если у вас возникли трудности, обратитесь к примеру с товаром выше.

Дополнительное задание: Ссылка на связанный товар на странице заказа
Если у вас еще осталось время, попробуйте добавить на страницу заказа ссылку на связанный с этим заказом товар.

В order_detail.html:

html
Copy code
<!-- shop/templates/shop/order_detail.html -->
<a href="{% url 'product_detail' id=order.product.id %}">Подробнее о товаре</a>
Это позволяет пользователю переходить от заказа к связанному с ним товару, улучшая навигацию по сайту.