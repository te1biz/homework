# Проект homework

## Описание:

это моя домашка 

## Установка:

1. Клонируйте репозиторий:
```
git clone https://github.com/te1biz/homework.git
```
2. Установите зависимости:
```
poetry install
```
## Использование:

1. filter by state -
Фильтрует список словарей по значению ключа
2. sort by date - 
сортирует список по дате

### Включения и генераторы:
1. добавил функции filter_by_currency, transaction_descriptions, card_number_generator для работы с массивами транзакций
2. Так же добаавил тесты для них

## Генераторы и включение:
модуль src.generators получил генераторы для отбора транзакций по коду валют и выдачи номеров карт в диапазоне.


## Тесты 
1. запустить все тесты для проверки можно командой 
```bash
pytest
```
2. чтоб запустить тесты и создать html отчет используйте
```bash
pytest --cov=src --cov-report=term-missing --cov-report=html
```

# Пример использования функций
### импортируйте нужные функции из src

### filter by curency:
```bash
print("--- Фильтрация по валюте (RUB) ---")

rub_transactions = filter_by_currency(sample_transactions, "RUB")
for tx in rub_transactions:
    print(f"ID: {tx['id']}, Описание: {tx['description']}")
```

### transaction_descriptions
```bash
descriptions_gen = transaction_descriptions(sample_transactions)
all_descriptions = list(descriptions_gen)

print(all_descriptions)
```

### card_number_generator
```bash
cards = card_number_generator(1, 3)

print(next(cards))
print(next(cards))
print(next(cards))
```

