# Описание
Проект представляет собой систему для управления товарными запасами, покупка товаров и учёта клиентов. 

## Наименование
Название проекта: «MarketBase»

## Предметная область
Предметная область: Торговля и логистика.
Проект ориентирован на предприятия, занимающиеся розничной или оптовой торговлей.

# Данные
# Untitled Diagram documentation
## Summary

- [Introduction](#introduction)
- [Database Type](#database-type)
- [Table Structure](#table-structure)
	- [users](#users)
	- [product_categories](#product_categories)
	- [products](#products)
	- [purchase_history](#purchase_history)
	- [supply_history](#supply_history)
- [Relationships](#relationships)
- [Database Diagram](#database-Diagram)

## Introduction

## Database type

- **Database system:** PostgreSQL
## Table structure

### users

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **user_id** | SERIAL | 🔑 PK, not null  |  | |
| **username** | VARCHAR(32) | not null , unique |  | |
| **password** | VARCHAR(32) | not null  |  | |
| **role** | VARCHAR(6) | not null  |  | |
| **created_at** | DATE | not null  |  | | 


### product_categories

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **category_id** | SERIAL | 🔑 PK, not null  |  | |
| **category_name** | VARCHAR(64) | not null , unique |  | | 


### products

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **product_id** | SERIAL | 🔑 PK, not null  |  | |
| **seller_id** | INTEGER | not null  | products->seller | |
| **category_id** | INTEGER | not null  | products->categories | |
| **product_name** | VARCHAR(64) | not null  |  | |
| **description** | VARCHAR(256) | not null  |  | |
| **price** | NUMERIC(10,2) | not null  |  | |
| **total_quantity** | INTEGER | not null , default: 0 |  | |
| **date_od_update** | DATE | not null  |  | | 


### purchase_history

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **purchase_id** | SERIAL | 🔑 PK, not null  |  | |
| **client_id** | INTEGER | not null  | purchase_history->client | |
| **product_id** | INTEGER | not null  | purchase_history->products | |
| **quantity** | INTEGER | not null  |  | |
| **purchase_date** | DATE | not null  |  | |
| **total_price** | NUMERIC(10,2) | not null  |  | | 


### supply_history

| Name        | Type          | Settings                      | References                    | Note                           |
|-------------|---------------|-------------------------------|-------------------------------|--------------------------------|
| **supply_id** | SERIAL | 🔑 PK, not null  |  | |
| **seller_id** | INTEGER | not null  | supply_history->seller | |
| **product_id** | INTEGER | not null  | supply_history->products | |
| **quantity** | INTEGER | not null  |  | |
| **date_of_update** | DATE | not null  |  | | 


## Relationships

- **products to users**: many_to_one
- **products to product_categories**: many_to_one
- **purchase_history to users**: many_to_one
- **purchase_history to products**: many_to_one
- **supply_history to users**: many_to_one
- **supply_history to products**: many_to_one

## Database Diagram

```mermaid
erDiagram
	products }o--|| users : references
	products }o--|| product_categories : references
	purchase_history }o--|| users : references
	purchase_history }o--|| products : references
	supply_history }o--|| users : references
	supply_history }o--|| products : references

	users {
		SERIAL user_id
		VARCHAR(32) username
		VARCHAR(32) password
		VARCHAR(6) role
		DATE created_at
	}

	product_categories {
		SERIAL category_id
		VARCHAR(64) category_name
	}

	products {
		SERIAL product_id
		INTEGER seller_id
		INTEGER category_id
		VARCHAR(64) product_name
		VARCHAR(256) description
		NUMERIC(10,2) price
		INTEGER total_quantity
		DATE date_od_update
	}

	purchase_history {
		SERIAL purchase_id
		INTEGER client_id
		INTEGER product_id
		INTEGER quantity
		DATE purchase_date
		NUMERIC(10,2) total_price
	}

	supply_history {
		SERIAL supply_id
		INTEGER seller_id
		INTEGER product_id
		INTEGER quantity
		DATE date_of_update
	}
```
# Пользовательские роли

Роли и их описание:

- Продавец:

  Ответственность:
    Выставляет новые товары на продажу, может менят их данные (цену, название, описание, количество на складе)
    
- Клиент:

  Ответственность:
    Может покупать товары и ставить им оценки за качество


# UI / API 

Консольный интерфейс

## Язык программирования

Python

## СУБД

PostgreSQL
