# Отзывы к фильму

Повторение и закрепление знаний.

Для отправки отзыва нужно:
* Создать форму для отправки комментария.
* Создать контроллер принимающий запрос при отправке формы.
* Связать контроллер с маршрутом.


1. ## Сделаем форму для написания отзыва под плеером
    ```html
    <!-- kinopoisk/movie_detail.html -->
    <div class="mt-3 w-100">
        <form action="{% url 'add_movie_review' %}" method="POST" class="fr gap-1">
            {% csrf_token %}
            <textarea class="w-100 form-control" type="text" name="review_text"
                      placeholder="Напишите свой отзыв"></textarea>
            <button class="btn-send-review btn btn-secondary" type="submit">Отправить</button>
            <input type="hidden" value="{{ movie.id }}" name="movie_id">
        </form>
    </div>
    ```
2. ## Создадим контроллер `add_movie_review` и свяжем его с маршрутом
    ```python
    # kinopoisk/views.py
    def add_movie_review(request):
        if not request.user.is_authenticated:
            return redirect('signin')
        if request.method == 'POST':
            # Получаем movie id из запроса в отдельную переменную,
            # так как будем использовать его для создания отзыва и для редиректа.
            movie_id = request.POST.get('movie_id')
            MovieReview.objects.create(
                author=request.user,
                text=request.POST.get('review_text'),
                movie=Movie.objects.get(id=movie_id)
                # movie_id=movie_id
                # Что бы не делать доп. запрос на получение объекта фильма
                # достаточно передать его id, но это может запутать, так как
                # поля movie_id в модели нет, а movie есть.
            )
            return redirect('movie_detail', movie_id=movie_id)
    ```
    ```python
    # kinopoisk/urls.py
    urlpatterns = [
        ...
        path('add_movie_review/', add_movie_review, name='add_movie_review'),
    ]
    ```

3. ## Проверяем через админку, что комментарии появляются
4. ## Отобразим все отзывы к конкретному фильму
    Есть два варианта, выбирайте более **ПОНЯТНЫЙ** ученикам<br><br>
    * Можем передать `reviews` через контроллер в шаблон:
        ```python
        # kinopoisk/views.py
        def movie_detail(request, movie_id):
            return render(request, 'kinopoisk/movie_detail.html', {
                'movie': Movie.objects.get(id=movie_id),
                'reviews': MovieReview.objects.filter(movie_id=movie_id)
            })
        ```
    * А можем получить их прямо в шаблоне через `related_name`:
        ```python
        # kinopoisk/models.py
        class MovieReview(models.Model):
            ...
            movie = models.ForeignKey(
                Movie, on_delete=models.CASCADE,
                related_name='reviews') # <--- Напомните, что мы это делали
        ```
        ```html
        {% for review in movie.reviews.all %}
        ``` 
    <br>

    ```html
    <!-- kinopoisk/movie_detail.html -->
    <div class="mt-3 w-90">
        <form action="{% url 'add_movie_review' %}" method="POST" class="fr gap-1">
            ...
        </form>
        <div class="fc gap-2 mt-3">
            <!-- {% for review in reviews %} -->
            {% for review in movie.reviews.all %}
                <div class="border-secondary rounded-2 border-1 border p-2">
                    <h6 class="text-light fw-6">{{ review.author.username }}</h6>
                    <p>{{ review.text }}</p>
                    <div class="frsc mt-1 gap-2">
                        <span class="ms-auto text-secondary fs-6">{{ review.created_at }}</span>
                    </div>
                </div>
            {% endfor %}
        </div>
    </div>
    ```
5. ## Отобразим новые сверху
    Как видите, новые отзывы появляются снизу.<br>
    Изменить это можно так:
    ```python
    # kinopoisk/models.py
    class MovieReview(models.Model):
        ...
        class Meta:
            ordering = ('-created_at',)
    ```
    или
    ```python
    # kinopoisk/views.py
    def movie_detail(request, movie_id):
        return render(request, 'kinopoisk/movie_detail.html', {
            'movie': Movie.objects.get(id=movie_id),
            'reviews': MovieReview.objects.filter(
                movie_id=movie_id
            ).order_by('-created_at')
        })
    ```

## Подведите итоги.
># git push...