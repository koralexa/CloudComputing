# Система управления книжным магазином

- _mysql_ - база данных для хранения информации о наличии книг
- _api_ - веб-сервер для управления информацией о наличии книг

Dockerfile для mysql состоит по сути из одной команды FROM, поскольку другие манипуляции с образом mysql не требуются (таблицы создает api с помощью slqalchemy).

## Сборка и запуск

```bash
cd task1
docker compose build
docker compose up -d # для mysql написан healthcheck, поэтому может занять больше времени, чем ожидалось
```

По адресу <http://127.0.0.1:7950/docs> можно найти интерактивную документацию api, позволяющую удобно выполнять запросы

## Сценарии использования

- **Получение списка книг в наличии**
  - GET /books
  - C помощью query-параметра search можно выполнять поиск по названию и автору
- **Добавление книги**
  - POST /books
  - name - название книги (строка длиной не более 100 символов)
  - author - автор книги (строка длиной не более 50 символов)
  - Если книга ранее не продавалась в магазине, она будет добавлена в базу в количестве 1 и получит уникальный идентификатор
  - Если книга есть в наличии или ранее продавалась в магазине, ее количество в наличии будет увеличено на 1
- **Получение информации о книге по идентификатору**
  - GET /books/{bookId}
  - bookId - идентификатор книги (целое число)
  - Если книга с таким идентификатором отсутствует в базе, будет возвращен статус 404
- **Продажа книги**
  - POST /books/{bookId}
  - bookId - идентификатор книги (целое число)
  - Если книга с таким идентификатором отсутствует в базе, будет возвращен статус 404
  - Если книги с таким идентификатором нет в наличии, будет возвращен статус 400
  - Иначе, количество таких книг в наличии будет уменьшено на 1
