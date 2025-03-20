# Описание
Проект представляет собой систему для управления товарными запасами, покупка товаров и учёта клиентов. 

## Наименование
Название проекта: «MarketBase»

## Предметная область
Предметная область: Торговля и логистика.
Проект ориентирован на предприятия, занимающиеся розничной или оптовой торговлей.

# Данные

- **Database system:** PostgreSQL
## Table structure

### users

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **user_id** | SERIAL | 🔑 PK, not null  |  | |
| **username** | VARCHAR(32) | not null , unique |  |Имя пользователя |
| **password** | VARCHAR(32) | not null  |  |Пароль пользаветеля |
| **user_role** | VARCHAR(6) | not null  |  |Роль пользователя (клиент, продавец) |
| **created_at** | DATE | not null  |  |Дата создания аккаунта пользователя | 


### product_categories

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **category_id** | SERIAL | 🔑 PK, not null  |  | |
| **category_name** | VARCHAR(64) | not null , unique |  |Название категории товаров |
| **seller_id** | INTEGER | not null  | seller->users |ID пользователя(продавца), который ввел эту категорию | 


### products

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **product_id** | SERIAL | 🔑 PK, not null  |  | |
| **seller_id** | INTEGER | not null  | products->seller |ID пользователя(продавца), у которого продается данный товар |
| **category_id** | INTEGER | not null  | products->categories |ID категории товара |
| **product_name** | VARCHAR(64) | not null  |  |Название товара |
| **description** | VARCHAR(256) | not null  |  |Описание продукта |
| **price** | NUMERIC(10,2) | not null  |  |Стоимость 1 единцы товара |
| **total_quantity** | INTEGER | not null , default: 0 |  |Количество товара на складе |
| **date_od_update** | DATE | not null  |  |Дата обновления товара | 


### purchase_history

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **purchase_id** | SERIAL | 🔑 PK, not null  |  | |
| **client_id** | INTEGER | not null  | purchase_history->client |ID пользователя(клиента) который произвел эту покупку |
| **product_id** | INTEGER | not null  | purchase_history->products |ID товара, которого купили |
| **quantity** | INTEGER | not null  |  |Количество товара за покупку |
| **price** | NUMERIC | not null  |  |Цена 1 единицы товара |
| **total_price** | NUMERIC(10,2) | not null  |  |Общая сумма покупки |
| **purchase_date** | DATE | not null  |  |Дата покупки | 


### supply_history

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **supply_id** | SERIAL | 🔑 PK, not null  |  | |
| **seller_id** | INTEGER | not null  | supply_history->seller |ID пользователя(продавца), который произвел поставку |
| **product_id** | INTEGER | not null  | supply_history->products |ID товара |
| **quantity** | INTEGER | not null  |  |Количество товара за поставку |
| **supply_date** | DATE | not null  |  |Дата поставки | 


## Зависимости

- **products to users**: many_to_one
- **products to product_categories**: many_to_one
- **purchase_history to users**: many_to_one
- **purchase_history to products**: many_to_one
- **supply_history to users**: many_to_one
- **supply_history to products**: many_to_one
- **product_categories to users**: many_to_one

![New diagram](https://github.com/user-attachments/assets/65854055-6e3c-40cf-9aec-088c0cb49b24)


# Пользовательские роли

Роли и их описание:

- Продавец:

  Ответственность:
    Выставляет новые товары на продажу и добовляет новые категории
    
- Клиент:

  Ответственность:
    Может покупать товары


# UI / API 

Консольный интерфейс

## Язык программирования

Python

## СУБД

PostgreSQL


## Инструкция по запуску

Для работы программы необходимо установить PostgreSQL (ссылка для скачивания - https://www.postgresql.org/download/) и DBeaver (ссылка для скачивания -https://dbeaver.io/download/)
На PostgreSQL необходимо запустить сервер и подключиться к нему через DBeaver. Далее создать базу данных и назвать его 'postgres' 
В эту базу данных импортировать дамп файл из репозитория.
Для работы программы также необходим Python и также библиотеки flask и psycopg2.
Далее загружаем серверный и клиентский файлы из репозитория. Желательно в одну директорию, для удобства.
Запуск производиться через консоль cmd. Запускаем в директории с установленными файлами, либо перейти к нужной диреткории с помощью команды `cd "путь к директории"`
Открываем два окна консоли, на одной запускаем сервер `python server.py`, а на другом клиента `python client.py`
