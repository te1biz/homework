Обработка банковских операций (Homework)

 Учебный проект на Python для загрузки, фильтрации и анализа банковских транзакций. Программа поддерживает JSON, CSV и XLSX, а также реализует главную страницу, сервис «Инвесткопилка» и отчёт по тратам в выбранной категории.

## _Функционал проекта_

### _Обработка и сортировка данных_

* **`src.main`** — консольное приложение для работы с банковскими операциями.
* **`filter_by_state`** — фильтрует транзакции по статусу.
* **`sort_by_date`** — сортирует транзакции по дате.
* Поддерживается фильтрация рублёвых операций, поиск по описанию и маскировка номеров карт и счетов.

### _Главная страница (`src.views`)_

Функция **`main_page()`** принимает дату и время в формате `YYYY-MM-DD HH:MM:SS` и список транзакций. Она формирует JSON с приветствием, расходами и кешбэком по картам, топ‑5 транзакций, курсами валют и ценами акций.

Настройки находятся в `user_settings.json` в корне проекта:

```json
{
  "user_currencies": ["USD", "EUR"],
  "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
}
```

Курсы валют загружаются через Exchange Rates Data API. Для этого укажите ключ в `.env`:

```env
EXCHANGE_RATES_API_KEY=ваш_ключ
```

Цены акций загружаются через Yahoo Finance Chart API. Если API недоступен, в JSON сохраняются валюта или тикер, значение `0.0` и описание ошибки в поле `error`.

Пример:

```python
import json

from src.utils import load_transactions
from src.views import main_page

transactions = load_transactions("data/operations.json")
response = main_page("2024-03-31 12:00:00", transactions)

print(json.dumps(json.loads(response), ensure_ascii=False, indent=2))
```

### _Сервис «Инвесткопилка» (`src.services`)_

**`investment_bank(month, transactions, limit)`** рассчитывает сумму, которую можно было накопить за счёт округления трат за указанный месяц. Допустимые шаги округления: 10, 50 и 100 рублей.

```python
from src.services import investment_bank

transactions = [
    {"Дата операции": "2024-03-01", "Сумма операции": 1712},
    {"Дата операции": "2024-03-15", "Сумма операции": 1750},
]

saved_amount = investment_bank("2024-03", transactions, 50)
print(saved_amount)  # 38.0
```

### _Отчёт по тратам в категории (`src.reports`)_

**`spending_by_category(dataframe, category, date_to=None)`** возвращает операции выбранной категории за три календарных месяца до даты включительно. Если дата не указана, используется текущая дата.

Результат автоматически сохраняется в `reports.json` в текущей рабочей папке. Декоратор **`report_saver`** позволяет указать другой путь к файлу.

```python
import pandas as pd

from src.reports import spending_by_category

transactions = pd.read_excel("data/transactions.xlsx")
report = spending_by_category(
    transactions,
    category="Продукты",
    date_to="2024-03-31",
)

print(report)
```

---

## _Установка_

Для работы проекта нужны Python 3.13 или новее и Poetry.

```bash
poetry install
```

Отчёты используют библиотеку `pandas`. Если она ещё не указана в зависимостях проекта, добавьте её один раз:

```bash
poetry add pandas
poetry install
```

Для запросов курсов валют создайте `.env` на основе `.env.example` и укажите действующий `EXCHANGE_RATES_API_KEY`. Не добавляйте `.env` в Git: в нём хранится секретный ключ.

---

## _Запуск_

Запустите консольное приложение из корневой папки проекта:

```bash
poetry run python -m src.main
```

По умолчанию доступны файлы:

* `data/operations.json`
* `data/transactions.csv`
* `data/transactions.xlsx`

Если файла нет по стандартному пути, программа предложит указать свой путь.

---

## _Тестирование_

Запустить все тесты:

```bash
poetry run pytest -q
```

Запустить тесты главной страницы, сервиса и отчёта:

```bash
poetry run pytest -q tests/test_views.py tests/test_services.py tests/test_reports.py
```

Сформировать отчёт о покрытии кода, если установлен `pytest-cov`:

```bash
poetry run pytest --cov=src --cov-report=term-missing --cov-report=html
```

---

## _Структура проекта_

```text
homework/
├── data/
│   └── operations.json
├── src/
│   ├── main.py
│   ├── operations.py
│   ├── processing.py
│   ├── search.py
│   ├── services.py
│   ├── reports.py
│   ├── views.py
│   ├── generators.py
│   ├── masks.py
│   ├── widget.py
│   ├── external_api.py
│   └── utils.py
├── tests/
├── user_settings.json
├── .env.example
├── pyproject.toml
├── poetry.lock
└── README.md
```
