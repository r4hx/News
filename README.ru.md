# Самаризатор RSS каналов

## Описание

Этот проект представляет собой сервис для суммаризации статей RSS каналов. Если вы используете RSS для получения новостей, вы можете добавить свои источники в проект и получить новый RSS канал с кратким содержанием статей.

Даже если исходные каналы предоставляют краткую сводку статей, сервис проанализирует страницы и выделит основные идеи из них.

## Установка

Для запуска проекта вам понадобится Docker и docker-compose. Следуйте следующим шагам:

Клонируйте репозиторий:

```
git clone <url_репозитория>
```

Запустите сборку контейнеров:
 
```
make build
```

## Настройка

Скопируйте файл `.env.example` в `.env` и заполните обязательные параметры:

- YANDEX_TOKEN = токен от сервиса https://300.ya.ru (внизу страницы нажмите API и появится кнопка "получить токен")

## Использование

Для запуска проекта используйте команду:

```
make 
```

и откройте ссылку в браузере `http://127.0.0.1`

Для остановки проекта и очистки кэша используйте:

```
make stop
```

