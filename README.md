# Обработка банковских операций (Homework)

Учебный проект на Python для обработки, фильтрации и анализа банковских транзакций. Проект поддерживает фильтрацию и сортировку операций, генераторы для работы с транзакциями, маскировку номеров карт и счетов, а также чтение финансовых операций из JSON-, CSV- и XLSX-файлов.

## Функционал проекта

### Обработка и сортировка данных

- **`filter_by_state`** — фильтрует список транзакций по значению ключа `state`. По умолчанию используется статус `EXECUTED`.
- **`sort_by_date`** — сортирует транзакции по дате. По умолчанию — по убыванию, от новых к старым.

### Маскировка данных

Функции для маскировки номеров банковских карт и счетов, а также форматирования даты операции.

### Генераторы (`src.generators`)

Модуль для последовательной обработки транзакций:

- **`filter_by_currency`** — возвращает транзакции с указанным кодом валюты, например `RUB` или `USD`.
- **`transaction_descriptions`** — последовательно возвращает описания транзакций.
- **`card_number_generator`** — генерирует номера карт в формате `XXXX XXXX XXXX XXXX` в заданном диапазоне.

### Декораторы (`src.decorators`)

- **`log`** — декоратор для логирования начала и завершения работы функции. При возникновении ошибки записывает её тип и входные аргументы. Поддерживает вывод в консоль или в файл.

### Чтение финансовых операций из файлов (`src.file_readers`)

Для чтения данных используются библиотеки `pandas` и `openpyxl`.

- **`read_csv_transactions(path)`** — считывает финансовые операции из CSV-файла.
- **`read_excel_transactions(path)`** — считывает финансовые операции из Excel-файла формата XLSX.

Обе функции принимают путь к файлу и возвращают список словарей, в которых ключи соответствуют названиям столбцов, а значения — данным транзакций.

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/te1biz/homework.git
   cd homework
   ```

2. Установите зависимости:

   ```bash
   poetry install
   ```

## Примеры использования

### 1. Фильтрация транзакций по валюте

```python
from src.generators import filter_by_currency

rub_transactions = filter_by_currency(sample_transactions, "RUB")

for transaction in rub_transactions:
    print(transaction["description"])
```

### 2. Генерация номеров карт

```python
from src.generators import card_number_generator

cards = card_number_generator(1, 3)

for card in cards:
    print(card)
```

### 3. Чтение транзакций из CSV

```python
from src.file_readers import read_csv_transactions

transactions = read_csv_transactions("data/transactions.csv")
print(transactions)
```

### 4. Чтение транзакций из Excel

```python
from src.file_readers import read_excel_transactions

transactions = read_excel_transactions("data/transactions_excel.xlsx")
print(transactions)
```

## Тестирование

Проект использует `pytest` для модульного тестирования. Тесты новых функций чтения CSV и Excel проверяют вызовы pandas с помощью `Mock` и `patch`.

Запуск всех тестов:

```bash
poetry run pytest
```

Проверка покрытия кода:

```bash
poetry run pytest --cov=src --cov-report=term-missing --cov-report=html
```

После выполнения HTML-отчёт будет доступен в `htmlcov/index.html`.

Проверка типизации:

```bash
poetry run mypy src tests
```

Проверка стиля кода:

```bash
poetry run flake8 src tests
```

Проверка сортировки импортов:

```bash
poetry run isort --check-only src tests
```
