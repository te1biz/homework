Обработка банковских операций (Homework)

Учебный проект на Python для обработки, фильтрации и анализа массивов банковских транзакций. Реализованы инструменты для сортировки данных, выборки по статусам и валютам, а также генераторы для оптимизированной работы с большими объемами операций.
Функционал проекта
Обработка и сортировка данных

    filter_by_state — фильтрует список словарей с транзакциями по значению ключа state (по умолчанию 'EXECUTED').
    sort_by_date — сортирует список транзакций по дате (по умолчанию — по убыванию, от самых новых к старым).

Генераторы (src.generators)

Модуль для эффективной потоковой обработки транзакций:

    filter_by_currency — поочередно выдает транзакции, где валюта операции соответствует заданному коду (например, "RUB" или "USD").
    transaction_descriptions — генератор, который принимает список транзакций и поочередно возвращает описание (description) каждой операции.
    card_number_generator — генерирует номера банковских карт в формате XXXX XXXX XXXX XXXX в заданном диапазоне (от 0000 0000 0000 0001 до 9999 9999 9999 9999).

Установка

    Клонируйте репозиторий: git clone https://github.com/te1biz/homework.git cd homework
    Установите зависимости с помощью Poetry: poetry install

Примеры использования

Импортируйте необходимые функции из пакета src:
1. Фильтрация по валюте (filter_by_currency)

from src.generators import filter_by_currency

print("--- Фильтрация по валюте (RUB) ---")
rub_transactions = filter_by_currency(sample_transactions, "RUB")

for tx in rub_transactions:
    print(f"ID: {tx['id']}, Описание: {tx['description']}")

2. Получение описаний транзакций (transaction_descriptions)

from src.generators import transaction_descriptions

descriptions_gen = transaction_descriptions(sample_transactions)
all_descriptions = list(descriptions_gen)

print(all_descriptions)

3. Генерация номеров карт (card_number_generator)

from src.generators import card_number_generator

cards = card_number_generator(1, 3)

print(next(cards))  # 0000 0000 0000 0001
print(next(cards))  # 0000 0000 0000 0002
print(next(cards))  # 0000 0000 0000 0003

Тестирование

Проект покрыт модульными тестами с использованием библиотеки pytest.

Для запуска всех тестов выполните команду: pytest Для запуска тестов с оценкой покрытия кода (Coverage) и генерацией HTML-отчета используйте: pytest --cov=src --cov-report=term-missing --cov-report=html (После выполнения команды отчет о покрытии будет доступен в папке htmlcov/index.html).
About
No description, website, or topics provided.
Resources
Readme
Activity
Stars
1 star
Watchers
1 watching
Forks
1 fork
Releases
1tag
Create a new release
Packages
No packages published
Publish your first package
Contributors
2 (2)

    @te1biz
    te1biztelbiz
    @antigravity-gemini-lab
    antigravity-gemini-labGoogle Antigravity

Languages

    Python100%
