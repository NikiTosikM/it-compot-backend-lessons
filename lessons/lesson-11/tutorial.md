# Карточка товара.

Сегодня мы подключим админку и сделаем карточку товара для магазина.
Но перед этим доделаем если что-то не успели с предыдущего занятия.


1. ## Подключим административную панель
    > Одну показываем, вторую пусть сами, или обе сами ...
    ```python
    from .models import Product, Order
    
    
    @admin.register(Product)
    class ProductAdmin(admin.ModelAdmin):
        list_display = (
            'name',
            'price',
            'rating',
            ...  # и другие поля которые хотите.
        )
        list_editable = (
            'price',
        )
    
    
    @admin.register(Order)
    class OrderAdmin(admin.ModelAdmin):
        list_display = (
            'id',
            'product',
            'rating',
        )
    ```

2. ## Создаём карточку товара
    Как обычно, используем Bootstrap.<br>
    Берём [шаблон карточки](https://getbootstrap.com/docs/5.3/components/card/) 
    и добавляем на него все необходимое:<br>
    * Изображение, название, цену, скидку, рейтинг, описание, кнопку
    >Отображайте меньше полей если понимаете, что ученики не успеют.
    ```html
    <!-- shop/catalog.html  -->
    <div class="card border-0 rounded-4" 
         style="width: 250px; box-shadow: 0 0 5px #00000022;">
        <img src="{{ product.image.url }}" 
             class="card-img-top rounded-4" alt="{{ product.name }}">
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
                <!-- Используйте рейтинг товара для отображения звезд
                     Делаем цикл в ковычках пишем ЛЮБУЮ строку из 5 символов.  
                     Таким образом мы просто делаем цикл из 5 итераций 
                     т.к. максимальный рейтинг - 5, соответственно звезд 
                     будет тоже не больше 5. -->
                <!-- Если номер итерации меньше чем число рейтинга в 
                     данном обьекте продукта добавляем картинку звездочки,
                     иначе добавляем такую же картинку но делаем её серой. -->
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
                {{ product.desc|linebreaks }}<br>
            </small>
        </div>
    </div>
    ```