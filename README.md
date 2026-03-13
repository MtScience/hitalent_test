# hitalent_test

Тестовое задание для Hitalent. Моделирует систему управления некоторой организацией. Включает в себя базу данных и REST API для взаимодействия с ней. Реализовано на базе FastAPI и SQLAlchemy (+ Alembic для миграций).

## Запуск

1. Склонировать репозиторий
  
   ```console
   $ git clone https://github.com/MtScience/hitalent_test.git
   ```

2. В каталоге проекта создать файл `.env` следующего вида:

   ```
   POSTGRES_PORT=5432
   POSTGRES_DB=<имя базы>
   POSTGRES_HOST='localhost'
   POSTGRES_USER=<имя пользователя Postgres>
   POSTGRES_PASSWORD=<пароль пользователя Postgres>
   ```

3. Собрать Docker-образ проекта:

   ```console
   $ docker build -t server .
   ```

4. Запустить вместе с образом Postgres:

   ```console
   $ docker compose up
   ```

После указанных манипуляций Swagger проекта (предоставляемый FastAPI) будет доступен по адресу `127.0.0.1:8000/docs`.
