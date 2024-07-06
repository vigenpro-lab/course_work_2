# Analyzer Banking Operations

## Описание

Это приложение предназначено для анализа банковских транзакций из Excel-файлов. Оно генерирует JSON-данные для веб-страниц, формирует Excel-отчеты и предоставляет другие полезные сервисы.

## Установка

### Требования

- Python 3.8+
- Poetry (для управления зависимостями)

### Установка зависимостей

1. Клонируйте репозиторий:
    ```sh
    git clone https://github.com/vigenpro-lab/course_work_2
    ```

2. Создайте и активируйте виртуальное окружение:
    ```sh
    poetry shell
    ```

3. Установите зависимости:
    ```sh
    poetry install
    ```

### Настройка окружения

1. Переименуйте файл `.env_template` в `.env`:
    ```sh
    mv .env_template .env
    ```

2. Откройте файл `.env` и добавьте необходимый API ключ:
    ```env
    API_KEY=your_api_key_here
    ```

## Структура проекта

```plaintext
.
├── src
│ ├── __init__.py
│ ├── utils.py
│ ├── main.py
│ ├── views.py
│ ├── reports.py
│ └── services.py
├── data
│ ├── operations.xlsx
├── tests
│ ├── __init__.py
│ ├── test_utils.py
│ ├── test_views.py
│ ├── test_reports.py
│ └── test_services.py
├── user_settings.json
├── .env_template
├── .flake8
├── .gitignore
├── pyproject.toml
├── poetry.lock
└── README.md
```
## Основные файлы и их описание

### `src/main.py`

Основной файл для запуска приложения. Здесь происходит инициализация и настройка основных компонентов приложения.

### `src/utils.py`

Содержит вспомогательные функции, используемые в других модулях приложения.

### `src/views.py`

Реализует основные функции для генерации JSON-ответов для веб-страниц. Включает функции для обработки данных о транзакциях и отображения их в нужном формате.

### `src/reports.py`

Отвечает за генерацию отчетов. Включает функции для формирования Excel-отчетов и декораторы для записи результатов в файлы.

### `src/services.py`

Содержит сервисы для получения данных о курсах валют и ценах на акции. Реализованы функции для анализа транзакций и получения необходимых данных из внешних API.

## Тестирование

Для запуска тестов используйте команду:

```sh
poetry run pytest
```
## Использование

Пример использования можно найти в файле `main.py`. Для запуска приложения выполните:

```sh
poetry run python src/main.py
```
## Конфигурация

Пользовательские настройки задаются в файле `user_settings.json`. Пример:

```json
{
  "user_currencies": ["USD", "EUR"],
  "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
}
```
