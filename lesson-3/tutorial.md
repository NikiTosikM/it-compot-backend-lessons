Кто-то точно спросит где должен храниться этот файл.<br>

Рассказываем про то, как устроено хранение статических файлов в django.<br>
 ┣- 📂app1 `Приложение app1`<br>
 ┃  ┣- 📂migrations `Файлы миграций`<br>
 ┃  ┣- 📂static `Статические файлы`<br>
 ┃  ┃  ┣- 📂app1 `Статические файлы app1 приложения`<br>
 ┃  ┃  ┃  ┣- 📂css<br>
 ┃  ┃  ┃  ┃  ┗- 📜bootstrap.min.css<br>
 ┃  ┃  ┃  ┣- 📂img<br>
 ┃  ┃  ┃  ┗- 📂js<br>

Подключаем .css файл в html.
```html
{% load static %}
...
<head>
    <link rel="stylesheet" href="{% static 'app1/css/bootstrap.min.css' %}"> 
</head>
```