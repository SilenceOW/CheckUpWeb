Обязательно надо распаковать архив в папку.


1) Открыть start.bat (либо открыть CMD в папке проекта)
2) Ввести "Scripts\activate.bat"
3) Ввести pip install Django
4.1) Ввести "python manage.py runserver"
4.2) ВАЖНО!!! При выгрузке на сервер, обязательно в файле TeachBook/setting.py: DEBUG = False (24 строка)
5) В браузере забить 127.0.0.1:8000

ВАЖНО!!!
6.1) Перед закрытием консоли нажать Ctrl+C
6.2) Если консоль уже закрыта то открыть start.bat, написать "Scripts\activate.bat" и потом "python manage.py clearsessions"
6.3) Можно закрывать консоль


Аккаунт администратора: Логин - admin, пароль - admin
Панель администратора находится по ссылке: your_website_name/admin


При выгрузке на сервер, обязательно поменять в TeachBook/settings.py: DEBUG = False (24 строчка), добавить хост сервера в список ALLOWED_HOSTS (26 строчка)
