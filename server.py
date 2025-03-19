from flask import Flask, request, jsonify
import psycopg2
import datetime

app = Flask(__name__)

# Параметры подключения к PostgreSQL
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'admin'
DB_HOST = 'localhost'
DB_PORT = 5432

def get_db_connection():
    """ Устанавливает соединение с базой данных """
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        return None

@app.route('/register', methods=['POST'])
def register():
    """ Регистрация нового пользователя """
    data = request.json
    username = data.get("username")
    password = data.get("password")
    user_role = data.get("user_role")

    if not username or not password or user_role not in ['client', 'seller']:
        return jsonify({"error": "Некорректные данные"}), 400
    
    created_at = datetime.date.today()
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Ошибка подключения к БД"}), 500

    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (username, password, user_role, created_at)
                VALUES (%s, %s, %s, %s)
            """, (username, password, user_role, created_at))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": f"Ошибка регистрации: {e}"}), 500
    finally:
        conn.close()
    
    return jsonify({"message": "Регистрация прошла успешно."})

@app.route('/categories', methods=['GET'])
def get_categories():
    """ Получить список категорий товаров """
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Ошибка подключения к БД"}), 500
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT category_id, category_name FROM product_categories")
            categories = cur.fetchall()
            category_list = [{"id": row[0], "name": row[1]} for row in categories]
    except psycopg2.Error as e:
        return jsonify({"error": f"Ошибка получения категорий: {e}"}), 500
    finally:
        conn.close()
    return jsonify({"categories": category_list})


@app.route('/add_category', methods=['POST'])
def add_category():
    """ Добавление новой категории товаров """
    data = request.json
    category_name = data.get("category_name")
    
    if not category_name:
        return jsonify({"error": "Не указано название категории"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Ошибка подключения к БД"}), 500

    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO product_categories (category_name)
                VALUES (%s) RETURNING category_id
            """, (category_name,))
            new_category_id = cur.fetchone()[0]
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": f"Ошибка добавления категории: {e}"}), 500
    finally:
        conn.close()

    return jsonify({"message": "Категория успешно добавлена.", "category_id": new_category_id})


@app.route('/supply', methods=['POST'])
def supply():
    """ Поставка товара от продавца """
    data = request.json
    # Флаг, определяющий новый товар или существующий
    is_new = data.get("is_new", False)
    seller_id = data.get("seller_id")
    supply_date = datetime.date.today()

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Ошибка подключения к БД"}), 500

    try:
        with conn.cursor() as cur:
            if not is_new:
                # Поставка существующего товара:
                product_id = data.get("product_id")
                quantity = data.get("quantity")
                if not product_id or not quantity:
                    return jsonify({"error": "Для поставки существующего товара необходимо указать product_id и quantity"}), 400

                # Обновляем количество товара (увеличиваем общее количество)
                cur.execute("UPDATE products SET total_quantity = total_quantity + %s WHERE product_id = %s", (quantity, product_id))
                # Записываем поставку в историю
                cur.execute("""
                    INSERT INTO supply_history (seller_id, product_id, quantity, supply_date)
                    VALUES (%s, %s, %s, %s)
                """, (seller_id, product_id, quantity, supply_date))
            else:
                # Поставка нового товара:
                name = data.get("product_name")
                seller_id = data.get("seller_id")
                category_id = data.get("category_id")
                description = data.get("description")
                price = data.get("price")
                quantity = data.get("quantity")
                if not name or not category_id or price is None or not quantity:
                    return jsonify({"error": "Для нового товара обязательно укажите product_name, category_id, price и quantity (description - опционально)"}), 400

                # Вставляем новый товар и возвращаем его product_id
                cur.execute("""
                    INSERT INTO products (product_name, seller_id, category_id, description, price, total_quantity)
                    VALUES (%s, %s, %s, %s, %s, %s) RETURNING product_id
                """, (name, seller_id, category_id, description, price, quantity))
                new_product_id = cur.fetchone()[0]
                # Записываем поставку в историю
                cur.execute("""
                    INSERT INTO supply_history (seller_id, product_id, quantity, supply_date)
                    VALUES (%s, %s, %s, %s)
                """, (seller_id, new_product_id, quantity, supply_date))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": f"Ошибка поставки товара: {e}"}), 500
    finally:
        conn.close()

    return jsonify({"message": "Поставка товара успешно выполнена."})


@app.route('/products', methods=['GET'])
def get_products():
    """ Получить список доступных товаров """
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Ошибка подключения к БД"}), 500
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT product_id, product_name, description, price, total_quantity FROM products WHERE total_quantity > 0")
            products = cur.fetchall()

        product_list = [
            {"id": row[0], "name": row[1],"description": row[2], "price": row[3], "quantity": row[4]}
            for row in products
        ]
    except psycopg2.Error as e:
        return jsonify({"error": f"Ошибка получения списка товаров: {e}"}), 500
    finally:
        conn.close()

    return jsonify({"products": product_list})

@app.route('/purchase_history', methods=['GET'])
def purchase_history():
    """ Получить историю покупок для клиента """
    client_id = request.args.get("client_id", type=int)
    if not client_id:
        return jsonify({"error": "Не указан client_id"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Ошибка подключения к БД"}), 500

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT purchase_id, product_id, quantity, price, total_price, purchase_date 
                FROM purchase_history 
                WHERE client_id = %s
            """, (client_id,))
            purchases = cur.fetchall()
            purchase_list = [
                {
                    "purchase_id": row[0],
                    "product_id": row[1],
                    "quantity": row[2],
                    "price": row[3],
                    "total_price": row[4],
                    "purchase_date": row[5].isoformat() if isinstance(row[5], datetime.date) else str(row[5])
                }
                for row in purchases
            ]
    except psycopg2.Error as e:
        return jsonify({"error": f"Ошибка получения истории покупок: {e}"}), 500
    finally:
        conn.close()

    return jsonify({"purchase_history": purchase_list} or [])


@app.route('/supply_history', methods=['GET'])
def supply_history():
    """ Получить список поставок товаров """
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Ошибка подключения к БД"}), 500

    seller_id = request.args.get("seller_id", type=int)
    if not seller_id:
        return jsonify({"error": "Не указан seller_id"}), 400
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT supply_id, product_id, quantity, supply_date FROM supply_history WHERE seller_id = %s", ((seller_id,)))
            
            supplies = cur.fetchall()
            supply_list = [
                {
                    "supply_id": row[0],
                    "product_id": row[1],
                    "quantity": row[2],
                    "supply_date": row[3].isoformat() if isinstance(row[3], datetime.date) else str(row[3])
                }
                for row in supplies
            ]
    except psycopg2.Error as e:
        return jsonify({"error": f"Ошибка получения истории поставок: {e}"}), 500
    finally:
        conn.close()

    return jsonify({"supply_history": supply_list} or [])

@app.route('/update_product', methods=['PUT'])
def update_product():
    """ Обновление информации о товаре для продавцов """
    data = request.json
    product_id = data.get("product_id")
    if not product_id:
        return jsonify({"error": "Не указан ID товара"}), 400

    # Подготовка списка обновляемых полей и значений
    fields = []
    values = []
    if "product_name" in data:
        fields.append("product_name = %s")
        values.append(data["product_name"])
    if "price" in data:
        fields.append("price = %s")
        values.append(data["price"])
    if "description" in data:
        fields.append("description = %s")
        values.append(data["description"])

    if not fields:
        return jsonify({"error": "Нет данных для обновления"}), 400

    # Добавляем product_id в конец списка значений для условия WHERE
    values.append(product_id)

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Ошибка подключения к БД"}), 500

    try:
        with conn.cursor() as cur:
            query = f"UPDATE products SET {', '.join(fields)} WHERE product_id = %s"
            cur.execute(query, tuple(values))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": f"Ошибка обновления товара: {e}"}), 500
    finally:
        conn.close()

    return jsonify({"message": "Товар успешно обновлен."})


@app.route('/buy', methods=['POST'])
def buy_product():
    """ Клиент покупает товар """
    data = request.json
    client_id = data.get("client_id")
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if not client_id or not product_id or not quantity:
        return jsonify({"error": "Некорректные данные"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Ошибка подключения к БД"}), 500

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT price, total_quantity FROM products WHERE product_id = %s", (product_id,))
            product = cur.fetchone()
            if not product or product[1] < quantity:
                return jsonify({"error": "Недостаточно товара"}), 400

            total_price = product[0] * quantity

            cur.execute("""
                INSERT INTO purchase_history (client_id, product_id, quantity, price, total_price, purchase_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (client_id, product_id, quantity, product[0], total_price, datetime.date.today()))

            cur.execute("UPDATE products SET total_quantity = total_quantity - %s WHERE product_id = %s",
                        (quantity, product_id))

        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": f"Ошибка покупки: {e}"}), 500
    finally:
        conn.close()

    return jsonify({"message": "Покупка совершена успешно."})

@app.route('/login', methods=['POST'])
def login():
    """ Авторизация пользователя """
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Некорректные данные"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Ошибка подключения к БД"}), 500

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT user_id, user_role FROM users
                WHERE username = %s AND password = %s
            """, (username, password))
            user = cur.fetchone()
    except psycopg2.Error as e:
        return jsonify({"error": f"Ошибка входа: {e}"}), 500
    finally:
        conn.close()

    if not user:
        return jsonify({"error": "Неверное имя пользователя или пароль."}), 401

    return jsonify({"message": "Успешный вход", "user_id": user[0], "user_role": user[1]})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
