# Pay2u - сервис подключения подписок

- [Описание](#desc)
- [Описание Backend](#desc-backend)
    - [Стек технологий](#stack-backend)
    - [Запуск всего проекта в контейнерах(локально)](#all-local)
    - [Запуск всего проекта в контейнерах на сервере](#all-server)
    - [Запуск только бакенда для разработки](#backend-local)
        - [Установка Poetry](#install-poetry)
        - [Запуск Postgres](#start-postgres)
        - [Запуск Django](#start-django)
    - [Команда](#team-backend)
- [Описание Frontend](#desc-frontend)
    - [Стек технологий](#stack-frontend)
    - [Команда](#team-frontend)

## Описание <a id="desc"></a>
Сервис позволяет пользователям следить за своими подписками на развлекательные сервисы. Подписки разбиты на категории для простоты навигации. Пользователь может подключать новые и продлять старые подписки, добавлять понравившееся в избранное. Есть опция учёта расходов и начисленного кэшбека.

url-адрес: https://pay2u.zapto.org/

swagger: https://pay2u.zapto.org/swagger/
для выполнения запросов необходимо авторизоваться под пользователем для разработки из файла `.env`. По умолчанию - `dev_user` `dev_user_password`

redoc: https://pay2u.zapto.org/redoc/

## Описание Backend <a id="desc-backend"></a>
Приложение можно запустить разными способами - [раз](#all-local), [два](#all-server), [три](#backend-local).
Во всех случаях автоматически применяются миграции и загружаются тестовые данные из каталога `backend/test_data/`.

### Стек технологий <a id="stack-backend"></a>
 - Python 3.10
 - Poetry 1.8
 - Django 4.2
 - Django REST Framework 3.15
 - Pillow 10.2
 - Postgres 13.3
 - Nginx
 - Docker

### Запуск всего проекта в контейнерах(локально) <a id="all-local"></a>
1. Клонируйте репозиторий
```
git clone git@github.com:KiryhaUdmurt/pay2u.git
```
2. Перейдите в каталог с проектом
```
cd pay2u/
```
3. Заполните `.env` в корне проекта по примеру `.env.example`
4. Установите Docker
```
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt-get install docker-compose-plugin
```
5. Запустите проект
```
sudo docker compose -f infra/docker-compose-local-all.yaml up -d --build
```
Приложение доступно по адресу http://localhost/

### Запуск всего проекта в контейнерах на сервере  <a id="all-server"></a>
Выполните шаги 1-4 из [Запуск всего проекта в контейнерах(локально)](#all-local)

1. В файле `.env` удалите параметр `DEBUG` или задайте для него значение `False`
2. Установите nginx `sudo apt install nginx -y`
3. Скорректируйте конфиг файл `sudo nano /etc/nginx/sites-available/default`
```
server {
        server_name pay2u.zapto.org;
        location / {
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
                proxy_set_header Host $http_host;
                proxy_pass http://127.0.0.1:8000/;
        }
}
```
4. Установите certbot `sudo snap install --classic certbot`
5. Запустите генерацию сертификата `sudo certbot --nginx `
6. Запустите проект
```
sudo docker compose -f infra/docker-compose-all.yaml up -d --build
```
Приложение доступно по адресу https://ваш-домен.ру/

### Запуск только бакенда для разработки <a id="backend-local"></a>
Выполните шаги 1-4 из [Запуск всего проекта в контейнерах(локально)](#all-local)

#### Установка Poetry <a id="install-poetry"></a>
- установите poetry
    ```
    pip install poetry
    ```
- установите зависимости
    ```
    poetry install
    ```
- для удобства можно задать параметр(.venv будет создаваться в каталоге с проектом)
    ```
    poetry config virtualenvs.in-project true

    ```
- активируйте окружение
    ```
    poetry shell
    ```

#### Запуск Postgres <a id="start-postgres"></a>
Для запуска контейнера с Postgres выполните команду
```
poetry run task onlydb
```
 

#### Запуск Django <a id="start-django"></a>
Для запуска сервера разработки Django  выполните команду
```
poetry run task start
```
API будет доступно по адресу http://localhost:8000/api/v1/
Для работы через Postman в заголовки запросов необходимо добавить параметр `Authorization` с токеном из `.env` файла.


### Команда <a id="team-backend"></a>
[Денис Третьяков](https://github.com/dentretyakoff)\
[Иван Павлов](https://github.com/ivnpvl)

## Описание Frontend <a id="desc-frontend"></a>


### Стек технологий <a id="stack-frontend"></a>


### Команда <a id="team-frontend"></a>



[MIT License](https://opensource.org/licenses/MIT)