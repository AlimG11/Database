# Описание
Проект представляет собой систему для управления товарными запасами, покупка товаров и учёта клиентов. 

## Наименование
Название проекта: «MarketBase»

## Предметная область
Предметная область: Торговля и логистика.
Проект ориентирован на предприятия, занимающиеся розничной или оптовой торговлей.

# Данные

### users

| Name        | Type          | Settings                      | References                    |
|-------------|---------------|-------------------------------|-------------------------------|
| **user_id** | SERIAL | 🔑 PK, not null  |  | 
| **username** | VARCHAR(32) | not null , unique |  | 
| **password** | VARCHAR(32) | not null  |  | 
| **user_role** | VARCHAR(6) | not null  |  | 
| **created_at** | DATE | not null  |  | 


### product_categories

| Name        | Type          | Settings                      | References                    | 
|-------------|---------------|-------------------------------|-------------------------------|
| **category_id** | SERIAL | 🔑 PK, not null  |  | 
| **category_name** | VARCHAR(64) | not null , unique |  | 
| **seller_id** | INTEGER | not null  | seller->users | 


### products

| Name        | Type          | Settings                      | References                    |
|-------------|---------------|-------------------------------|-------------------------------|
| **product_id** | SERIAL | 🔑 PK, not null  |  | 
| **seller_id** | INTEGER | not null  | products->seller | 
| **category_id** | INTEGER | not null  | products->categories | 
| **product_name** | VARCHAR(64) | not null  |  | 
| **description** | VARCHAR(256) | not null  |  | 
| **price** | NUMERIC(10,2) | not null  |  | 
| **total_quantity** | INTEGER | not null , default: 0 |  | 
| **date_od_update** | DATE | not null  |  | 


### purchase_history

| Name        | Type          | Settings                      | References                    |
|-------------|---------------|-------------------------------|-------------------------------|
| **purchase_id** | SERIAL | 🔑 PK, not null  |  | 
| **client_id** | INTEGER | not null  | purchase_history->client | 
| **product_id** | INTEGER | not null  | purchase_history->products | 
| **quantity** | INTEGER | not null  |  | |
| **purchase_date** | DATE | not null  |  | |
| **total_price** | NUMERIC(10,2) | not null  |  | 
| **price** | NUMERIC((10,2)) | not null  |  |  


### supply_history

| Name        | Type          | Settings                      | References                    |
|-------------|---------------|-------------------------------|-------------------------------|
| **supply_id** | SERIAL | 🔑 PK, not null  |  | 
| **seller_id** | INTEGER | not null  | supply_history->seller | 
| **product_id** | INTEGER | not null  | supply_history->products | 
| **quantity** | INTEGER | not null  |  | 
| **supply_date** | DATE | not null  |  | 


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
