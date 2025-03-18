import requests

API_URL = "http://127.0.0.1:5000"

def register():
    """ Регистрация нового пользователя """
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    user_role = input("Введите роль (client/seller): ")

    data = {
        "username": username,
        "password": password,
        "user_role": user_role
    }

    response = requests.post(f"{API_URL}/register", json=data)
    print(response.json())

def login():
    """ Вход пользователя """
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")

    data = {
        "username": username,
        "password": password
    }

    response = requests.post(f"{API_URL}/login", json=data)
    print(response.json())
    if response.status_code == 200:
        user_data = response.json()
        return user_data
    else:
        print(response.json().get("error", "Ошибка авторизации"))
        return None

def update_product():
    """ Обновление информации о товаре для продавцов """
    product_id = input("Введите ID товара для обновления: ")

    print("Выберите параметр для обновления:")
    print("1. Название")
    print("2. Цена")
    print("3. Описание")
    choice = input("Ваш выбор: ")

    data = {"product_id": int(product_id)}
    if choice == "1":
        new_name = input("Введите новое название: ")
        data["product_name"] = new_name
    elif choice == "2":
        try:
            new_price = float(input("Введите новую цену: "))
            data["price"] = new_price
        except ValueError:
            print("Некорректная цена.")
            return
    elif choice == "3":
        new_description = input("Введите новое описание: ")
        data["description"] = new_description
    else:
        print("Некорректный выбор.")
        return

    response = requests.put(f"{API_URL}/update_product", json=data)
    print(response.json())

def add_category():
    """ Добавление новой категории товаров """
    category_name = input("Введите название новой категории: ")
    data = {"category_name": category_name}
    response = requests.post(f"{API_URL}/add_category", json=data)
    print(response.json())

def list_categories():
    """ Вывод списка доступных категорий """
    response = requests.get(f"{API_URL}/categories")
    if response.status_code == 200:
        categories = response.json().get("categories", [])
        if not categories:
            print("Нет доступных категорий.")
        else:
            print("\nДоступные категории:")
            for category in categories:
                print(f"ID: {category['id']}, Название: {category['name']}")
    else:
        print("Ошибка при получении списка категорий:", response.json().get("error", "Неизвестная ошибка"))

def supply_product(seller_id):
    """ Поставка товара от продавца """
    print("Выберите тип поставки:")
    print("1. Поставка уже существующего товара")
    print("2. Поставка нового товара")
    choice = input("Ваш выбор: ")

    data = {"seller_id": seller_id}
    if choice == "1":
        product_id = input("Введите ID товара: ")
        quantity = input("Введите количество для поставки: ")
        data["is_new"] = False
        data["product_id"] = int(product_id)
        data["quantity"] = int(quantity)
    elif choice == "2":
        # Получаем список категорий
        response = requests.get(f"{API_URL}/categories")
        if response.status_code == 200:
            categories = response.json().get("categories", [])
            if not categories:
                print("Нет доступных категорий.")
                return
            print("\nДоступные категории:")
            for category in categories:
                print(f"ID: {category['id']}, Название: {category['name']}")
        else:
            print("Ошибка при получении категорий.")
            return
        name = input("Введите название нового товара: ")
        category_id = input("Введите ID категории: ")
        description = input("Введите описание товара: ")
        price = input("Введите цену товара: ")
        quantity = input("Введите количество для поставки: ")
        data["is_new"] = True
        data["product_name"] = name
        data["category_id"] = int(category_id)
        data["description"] = description
        try:
            data["price"] = float(price)
        except ValueError:
            print("Некорректная цена.")
            return
        data["quantity"] = int(quantity)
    else:
        print("Некорректный выбор.")
        return

    response = requests.post(f"{API_URL}/supply", json=data)
    print(response.json())


def get_products():
    """ Получить список доступных товаров """
    response = requests.get(f"{API_URL}/products")
    if response.status_code == 200:
        products = response.json().get("products", [])
        if not products:
            print("Нет доступных товаров.")
            return None

        print("\nДоступные товары:")
        for product in products:
            print(f"ID: {product['id']}, Название: {product['name']}, Описание: {product['description']}, Цена: {product['price']}, Количество: {product['quantity']}")
        return products
    else:
        print("Ошибка при получении списка товаров:", response.json().get("error", "Неизвестная ошибка"))
        return None

def buy_product(client_id):
    """ Клиент покупает товар """
    products = get_products()
    if not products:
        return

    product_id = input("Введите ID товара для покупки: ")
    quantity = input("Введите количество: ")

    data = {
        "client_id": client_id,
        "product_id": int(product_id),
        "quantity": int(quantity)
    }

    response = requests.post(f"{API_URL}/buy", json=data)
    print(response.json())


def main():
    """ Основное меню клиента """
    user_data = None
    user_role = None
    user_id = None
    while True:
        if user_role is None:
            print("\n1. Регистрация\n2. Вход\n3. Выход")
            choice = input("Выберите действие: ")

            if choice == "1":
                register()
            elif choice == "2":
                user_data = login()
                user_role = user_data.get("user_role")
                user_id = user_data.get("user_id")
            elif choice == "3":
                print("Выход из программы.")
                break
            else:
                print("Некорректный ввод, попробуйте снова.")
        else:
            user_role = user_data.get("user_role")
            user_id = user_data.get("user_id")
            print(f"Вы вошли как {user_role}.\n==========\n")
            if user_role == "client":
                while True:
                    print("\n1. Покупка\n2. Выход")
                    choice = input("Выберите действие: ")

                    if choice == "1":
                        buy_product(user_id)
                        get_products()
                    elif choice == "2":
                        break
                    else:
                        print("Некорректный ввод, попробуйте снова.")                 
            else:
                while True:
                    print("\n1. Обновление товара\n2. Поставка нового товара\n3. Новая категория товаров\n4. Вывести список категорий\n5. Выход")
                    choice = input("Выберите действие: ")
                    if choice == "1":
                        get_products()
                        update_product()
                        get_products()
                    elif choice == "2":
                        get_products()
                        supply_product(user_id)
                        get_products()
                    elif choice == "3":
                        add_category()
                    elif choice == "4":
                        list_categories()    
                    elif choice == "5":
                        break
                    else:
                        print("Некорректный ввод, попробуйте снова.")  
            break

if __name__ == "__main__":
    main()
