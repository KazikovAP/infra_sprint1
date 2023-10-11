[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/-Node.js-464646?style=flat-square&logo=Node.js)](https://nodejs.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![SQLite](https://img.shields.io/badge/-SQLite-464646?style=flat-square&logo=SQLite)](https://www.sqlite.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)

# Kittygram
Kittygram - социальная сеть для обмена фотографиями любимых питомцев.

---
# Как пользоваться:
- Перейдите на сайт https://kazikovkittygram.viewdns.net/
- Зарегестрируйтесь
- Войдите
- Увидитие список доступных питомцев для просмотра
- После того, как налюбовались всеми питомцами, добавьте своего

Приятного использования

---
## Технологии
* Python 3.9
* Django 3.2.3
* Django Rest Framework 3.12.4
* gunicorn 20.1.0
* Node.js

---
## Установка проекта на локальный компьютер или виртуальный сервер из репозитория GitHub:
- Клонируйте проект с репозитория `https://github.com/KazikovAP/infra_sprint1.git`
- Перейдите в директорию клонированного репозитория `cd infra_sprint1`
- Создайте виртуальное окружение `python3 -m venv venv`
- Активируйте виртуальное окружение `source venv/bin/activate`
- Установите необходимые зависимости `pip install -r requirements.txt`

---
## Настройка бэкенд-приложения
- Примените миграции `python3 manage.py migrate`
- Создайте суперпользователя, чтобы пользоваться всем функционалом приложения `python3 manage.py createsuperuser`
- В настройках проекта `settings.py` в список `ALLOWED_HOSTS = ['xxx.xxx.xxx.xxx', '127.0.0.1', 'localhost', 'ваш_домен']` укажите ваш IP и домен
- Также в `settings.py` отключите режим дебага для бэкенд-приложения `DEBUG = False`
- Подготовьте бэкенд-приложение для сбора статики. В файле `settings.py` укажите директорию, куда эту статику нужно сложить `STATIC_URL = 'static_backend'`, также добавьте константу `STATIC_ROOT = BASE_DIR / 'static_backend'`
- Соберите статику бэкенд-приложения `python3 manage.py collectstatic`
- Скопируйте директорию static_backend/ в директорию /var/www/название_проекта/ `sudo cp -r путь_к_директории_с_бэкендом/static_backend /var/www/название_проекта`

---
## Настройка фронтенд-приложения
- Находясь в директории с фронтенд-приложением, установите зависимости для него `npm i`
- Из директории с фронтенд-приложением выполните команду `npm run build`
-  Скопируйте статику фронтенд-приложения в директорию по умолчанию `sudo cp -r путь_к_директории_с_фронтенд-приложением/build/. /var/www/имя_проекта/`

---
## Установка и настройка WSGI-сервера Gunicorn
- При подключённом удалённом сервере и активированном виртуальном окружении, установите пакет gunicorn `pip install gunicorn==20.1.0`
- Запустите Gunicorn, из директории с файлом manage.py `gunicorn --bind 0.0.0.0:8000 backend.wsgi`
- Создайте файл конфигурации юнита systemd для Gunicorn в директории /etc/systemd/system/ `sudo nano /etc/systemd/system/gunicorn_название_проекта.service`
- Подставьте в код из листинга свои данные:
`[Unit]
Description=gunicorn daemon
After=network.target
[Service]
User=yc-user
WorkingDirectory=/home/yc-user/infra_sprint1/backend/
ExecStart=/home/yc-user/infra_sprint1/backend/venv/bin/gunicorn --bind 0.0.0.0:>
[Install]
WantedBy=multi-user.target`
- Запустите Gunicorn `sudo systemctl start gunicorn_название_проекта`
- Чтобы systemd следил за работой демона Gunicorn, запускал его при старте системы и при необходимости перезапускал, используйте команду: `sudo systemctl enable gunicorn_название_проекта`

---
## Установка и настройка веб- и прокси-сервера Nginx
- Установите Nginx `sudo apt install nginx -y`
- Запустите Nginx `sudo systemctl start nginx`
- Обновите настройки Nginx. Для этого откройте файл конфигурации веб-сервера `sudo nano /etc/nginx/sites-enabled/default`
- очистите содержимое файла и запишите новые настройки
`server {
 listen 80;
 server_name ваш_домен;
 location /api/ {
 proxy_pass http://127.0.0.1:8000;
 }
 location /admin/ {
 proxy_pass http://127.0.0.1:8000;
 }
 location / {
 root /var/www/имя_проекта;
 index index.html index.htm;
 try_files $uri /index.html;
 }
}`
- Сохраните изменения в файле, закройте его и проверьте на корректность: `sudo nano /etc/nginx/sites-enabled/default`
- Перезагрузите конфигурацию Nginx: `sudo systemctl reload nginx`

---
## Настройка файрвола ufw
Файрвол установит правило, по которому будут закрыты все порты, кроме тех, которые
вы явно укажете.
- Активируйте разрешение принимать запросы только на порты 80, 443 и 22
80, 443: с ними будут работать пользователи, делая запросы к приложению.
`sudo ufw allow 'Nginx Full'`
22: нужен, чтобы вы могли подключаться к серверу по SSH.
`sudo ufw allow OpenSSH`
- Включите файрвол `sudo ufw enable`
- Проверьте работу файрвола `sudo ufw status`

---
## Получение и настройка SSL-сертификата
- Установите пакетный менеджер snap `sudo apt install snapd`
- Установите и обновите зависимости для пакетного менеджера snap `sudo snap install core; sudo snap refresh core`
- Установите пакет cerbot `sudo snap install --classic certbot`
-  Обеспечети доступ к пакету для пользователя с правами администратора `sudo ln -s /snap/bin/certbot /usr/bin/certbot`
-  Запустите certbot и получите SSL-сертификат `sudo certbot --nginx`
-  сертификат автоматически сохранится на вашем сервере в системной директории /etc/ssl/ Также будет автоматически изменена конфигурация Nginx: в файл /etc/nginx/sites-enabled/default добавятся новые настройки и будут прописаны пути к сертификату
- ерезагрузить конфигурацию Nginx `sudo systemctl reload nginx`

---
## Разработал:
[Aleksey Kazikov](https://github.com/KazikovAP)

---
## Лицензия
[MIT](https://opensource.org/licenses/MIT)
