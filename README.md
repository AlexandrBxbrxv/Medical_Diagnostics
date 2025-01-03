# Сайт компании медицинской диагностики

### Запуск
##### Для запуска локально без докера:
* Заполните файл ".env.sample" и переименуйте его в ".env"
* Установить зависимости: `pip install -r requirements.txt`
* Поднять сайт: `python manage.py runserver`

##### Для запуска через докер:
* Заполните файл ".env.sample" и переименуйте его в ".env"
* Пропишите из папки проекта Medical_Diagnostics>`docker-compose up -d --build`

##### Для запуска на сервере:
* Заполните файл ".env.sample" и переименуйте его в ".env"
* Загрузите проект на GitLab
* Клонируйте проект на сервер
* Проект запуститься сам

<hr>

###### DevLog

_v0.8_
1. Настройка Docker и docker-compose.yaml
2. Настройка env проекта на работу с контейнерами
3. Настройка для работы с GitLab deploy pipline
4. Правки PEP8

_v0.7_
1. Тесты для контроллеров Cart
2. Тесты для контроллеров History
3. Добавлена карта проезда
4. Настройка скриптов и внешнего вида страниц

_v0.6_
1. Добавлена страница Корзина
2. Добавлены механики добавления/удаления услуг в корзину
3. Изменена модель History
4. Добавлена страница История

_v0.5_
1. Обновлена главная страница
2. Добавлена страница "О компании"
3. Добавлена страница "Контакты"
4. Добавлена модель Feedback
5. Настроена кастомная форма для обратной связи

_v0.4_
1. Добавлена модель Service
2. CRUD для Appointment
3. Тесты на CRUD для Appointment
4. CRUD для Analysis
5. Тесты на CRUD для Analysis
6. CRUD для Result
7. Тесты на CRUD для Result

_v0.3_
1. Установлена библиотека coverage
2. Добавлены модели Cart, History
3. CRUD для Doctor
4. Тесты на CRUD для Doctor

_v0.2_
1. Добавлена главная страница
2. Добавлен вход/выход пользователя
3. Регистрация с отправкой подтверждающего письма на почту
4. Просмотр/изменение своего профиля

_v0.1_
1. Добавлены приложения main, services
2. Добавлены модели Doctor, Appointment, Analysis, Result
3. Добавлено отображение моделей в админке

_v0_
1. Установлены библиотеки Django, python-dotenv, psycopg2, Pillow, flake8
2. Все чувствительные данные засекречены
3. Добавлена модель User
