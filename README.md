# Сайт компании медицинской диагностики

### Запуск
Установить зависимости: pip install -r requirements.txt\
Заполните файл ".env.sample" и переименуйте его в ".env"\
Поднять сайт: python manage.py runserver

###### DevBlog

`v.0.1`
1. Добавлены приложения main, services
2. Добавлены модели Doctor, Appointment, Analysis, Result
3. Добавлено отображение моделей в админке

`v.0`
1. Установлены библиотеки Django, python-dotenv, psycopg2, Pillow, flake8
2. Все чувствительные данные засекречены
3. Добавлена модель User
