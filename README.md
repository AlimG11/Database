# Описание
Проект представляет собой систему для управления товарными запасами, покупка товаров и учёта клиентов. 

## Наименование
Название проекта: «MarketBase»

## Предметная область
Предметная область: Торговля и логистика.
Проект ориентирован на предприятия, занимающиеся розничной или оптовой торговлей.

# Данные

### users (Пользователи)

| Name        | Type          | Settings                      | References                    |
|-------------|---------------|-------------------------------|-------------------------------|
| **user_id** | SERIAL | 🔑 PK, not null  |  | |
| **username** | VARCHAR(32) | not null , unique |  | |
| **password** | VARCHAR(32) | not null  |  | |
| **role** | VARCHAR(6) | not null  |  | |
| **created_at** | DATE | not null  |  | | 


### product_categories (Категории товаров)

| Name        | Type          | Settings                      | References                    |
|-------------|---------------|-------------------------------|-------------------------------|
| **category_id** | SERIAL | 🔑 PK, not null  |  | |
| **category_name** | VARCHAR(64) | not null , unique |  | | 


### products (Товары)

| Name        | Type          | Settings                      | References                    |
|-------------|---------------|-------------------------------|-------------------------------|
| **product_id** | SERIAL | 🔑 PK, not null  |  | |
| **seller_id** | INTEGER | not null  | products->seller | |
| **category_id** | INTEGER | not null  | products->categories | |
| **product_name** | VARCHAR(64) | not null  |  | |
| **description** | VARCHAR(256) | not null  |  | |
| **price** | NUMERIC(10,2) | not null  |  | |
| **total_quantity** | INTEGER | not null , default: 0 |  | |
| **date_od_update** | DATE | not null  |  | | 


### purchase_history (История покупок)

| Name        | Type          | Settings                      | References                    |
|-------------|---------------|-------------------------------|-------------------------------|
| **purchase_id** | SERIAL | 🔑 PK, not null  |  | |
| **client_id** | INTEGER | not null  | purchase_history->client | |
| **product_id** | INTEGER | not null  | purchase_history->products | |
| **quantity** | INTEGER | not null  |  | |
| **purchase_date** | DATE | not null  |  | |
| **total_price** | NUMERIC(10,2) | not null  |  | | 


### supply_history (История поставок)

| Name        | Type          | Settings                      | References                    |
|-------------|---------------|-------------------------------|-------------------------------|
| **supply_id** | SERIAL | 🔑 PK, not null  |  | |
| **seller_id** | INTEGER | not null  | supply_history->seller | |
| **product_id** | INTEGER | not null  | supply_history->products | |
| **quantity** | INTEGER | not null  |  | |
| **date_of_update** | DATE | not null  |  | | 


## Отношения

- **products to users**: many_to_one
- **products to product_categories**: many_to_one
- **purchase_history to users**: many_to_one
- **purchase_history to products**: many_to_one
- **supply_history to users**: many_to_one
- **supply_history to products**: many_to_one


![ER Diagram](https://github.com/user-attachments/assets/f58bc621-26b2-4b49-997d-e1c8e8be9e57)


# Пользовательские роли

Роли и их описание:

- Продавец:

  Ответственность:
    Выставляет новые товары на продажу
    
- Клиент:

  Ответственность:
    Может покупать товары


# UI / API 

Консольный интерфейс

## Язык программирования

Python

## СУБД

PostgreSQL
