# Вспоминаем JS и меняем тему на сайте
## ❗️Если ученики слабые или вы отстаёте сильно, можете не делать сохранение темы в локальное хранилище.

## [Скидываем ученикам и пробегаемся вместе с ними по строчкам этого файла](https://github.com/xlartas/it-compot-backend-methods/blob/main/js_lesson_change_theme_cheat_sheet.md).

Если вы уже меняли тему через `bootstrap`, то вспомните как, 
если нет, то...
```html
<body data-bs-theme="dark"></body>
или
<body data-bs-theme="light"></body>
```
Этого файла про js должно хватить, чтобы ученики сами:
сделали кнопку-картинку луну-солнце которая будет
при клике менять изображение и аттрибут `data-bs-theme`,
а после перезагрузки страницы подгружалась последняя 
выбранная тема.

1. ## Добавим кнопку в `header`
    Кнопкой будет обычная картинка.<br>
    Скачайте и поместите в папку для статических файлов иконки 
    для кнопок темной и светлой тем.
    ```html
    <!-- Core/includes/header.html -->
    {% load static %}
    <header>
        <nav class="navbar navbar-expand-lg">
            ....
                ....
                    <ul class="navbar-nav mb-2 mb-lg-0 gap-2">
                        ....
                        <li class="nav-item">
                            <img width="20" height="20"
                                 id="btn-change-theme"
                                 src="{% static 'Core/img/moon.png' %}" alt="theme">
                            <!-- src мы потом удалим, но пока пусть
                                 будет для наглядности. -->
                        </li>
                    </ul>
                ....
            ....
        </nav>
    </header>
    ```
2. ## Создадим js файл для смены темы и подключим его
    ```html
    <!-- Core/base.html -->
    {% load static %}
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        ....
        <!-- Вспомните, что такое defer -->
        <script defer src="{% static 'Core/js/theme.js' %}"></script>
        ....
    </head>
    <body class="d-flex flex-column" data-bs-theme="dark" style="min-height: 100vh;">
        ....
    </body>
    </html>
    ```
3. ## Напишем обработку смены картинки при клике.
    * Получим кнопку и сделаем функцию `setTheme` которая по задумке будем 
      принимать `false` или `true` и пока что просто менять картинку кнопки.<br><br>
      
      Повторите как устроены **[статические и медиа файлы](https://github.com/xlartas/it-compot-backend-methods/blob/main/django-base.md#static--media-files)**
      и как правильно подобрать верный `url` до нужной картинки.<br><br>
      * `http`://`127.0.0.1:8000`/`STATIC_URL`/`path_like_in_static_folder`/
      ```js
      // Core/js/theme.js
      const btnChangeTheme = document.querySelector('#btn-change-theme');
      function setTheme(value) {
          if (value === true) {
              // Меняем изображение на кнопке
              btnChangeTheme.src = '/static/Core/img/sun.png';
          } else {
              // Меняем изображение на кнопке
              btnChangeTheme.src = '/static/Core/img/moon.png';
          }
      }
      ```
      ```js  
      // Проверьте, что работает
      setTheme(false) // темная тема
      setTheme(true) // светлая тема
      ```
    
    * Добавим изменение атрибута `data-bs-theme` у `body`
      ```js
      // Core/js/theme.js
      const btnChangeTheme = document.querySelector('#btn-change-theme');
      const body = document.querySelector('body');
      
      function setTheme(value) {
          if (value === true) {
              btnChangeTheme.src = '/static/Core/img/sun.png';
              document.body.setAttribute('data-bs-theme', 'light');
          } else {
              btnChangeTheme.src = '/static/Core/img/moon.png';
              document.body.setAttribute('data-bs-theme', 'dark');
          }
      }
      // Проверьте, что работает
      ```
    * Чтобы отслеживать текущее состояние темы нужно завести переменную,
      она будет хранить `false` или `true`. Сделаем функцию переключатель темы 
      и свяжем её с событием клика у кнопки.
      ```js
      const body = document.querySelector('body');
      
      const btnChangeTheme = document.querySelector('#btn-change-theme');
      // При каждом клике переключаем тему
      btnChangeTheme.addEventListener('click', toggleTheme);
      
      let currentTheme = true;
      
      function setTheme(value) {
          if (value === true) {
              // Меняем изображение на кнопке
              btnChangeTheme.src = '/static/Core/img/sun.png';
              document.body.setAttribute('data-bs-theme', 'light');
          } else {
              // Меняем изображение на кнопке
              btnChangeTheme.src = '/static/Core/img/moon.png';
              document.body.setAttribute('data-bs-theme', 'dark');
          }
      }
      
      function toggleTheme() {
          // Устанавливаем тему в противоположную
          currentTheme = !currentTheme
          setTheme(currentTheme);
      }
      // Проверьте, что работает
      ```
    * Добавим сохранение темы в локальное хранилище и загрузку из него.
      ```js
      const body = document.querySelector('body');
      const btnChangeTheme = document.querySelector('#btn-change-theme');
      btnChangeTheme.addEventListener('click', toggleTheme);
      let currentTheme = true;
      loadTheme();
      
      function setTheme(value) {
          if (value === true) {
              // Меняем изображение на кнопке
              btnChangeTheme.src = '/static/Core/img/sun.png';
              document.body.setAttribute('data-bs-theme', 'light');
          } else {
              // Меняем изображение на кнопке
              btnChangeTheme.src = '/static/Core/img/moon.png';
              document.body.setAttribute('data-bs-theme', 'dark');
          }
          localStorage.setItem('theme', value);
      }
      
      function loadTheme() {
          const loaded_theme = localStorage.getItem('theme');
          if (loaded_theme !== null) { // Если функция вернула null, то сохраненного значения не существует.
              if (loaded_theme === 'true') {  // Помним, что локальное хранилище сохраняет только строки.
                  setTheme(true);
                  currentTheme = true;
              } else {
                  setTheme(false);
                  currentTheme = false;
              }
          }
      }
      
      function toggleTheme() {
          setTheme(!currentTheme);
          currentTheme = !currentTheme
      }
      ```
    ### Проверьте, что все работает

# Удалите атрибут `src` у кнопки.

4. ## Для сильных учеников можно попробовать объяснить оптимизированный код:
   ```javascript
   const btnChangeTheme = document.querySelector('#btn-change-theme');
   btnChangeTheme.addEventListener('click', () => setTheme(!isLightTheme()));
   
   function isLightTheme() {
       return localStorage.getItem('theme') === 'true';
   }
   
   function setTheme(isLight) {
       const theme = isLight ? 'light' : 'dark';
       btnChangeTheme.src = isLight ? '/static/Core/img/sun.png' : '/static/Core/img/moon.png';
       document.body.setAttribute('data-bs-theme', theme);
       localStorage.setItem('theme', isLight);
   }
   
   setTheme(isLightTheme());
   ```

## Подведите итоги.
># git push...