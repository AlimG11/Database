<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Клиентское приложение</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    input, select, button { margin: 5px 0; display: block; }
    button { cursor: pointer; }
    .container { margin-bottom: 20px; }
    table { border-collapse: collapse; width: 100%; margin-top: 10px; }
    th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
    th { background-color: #f2f2f2; }
  </style>
</head>
<body>
  <h1>Клиентское приложение</h1>
  <!-- Блок авторизации -->
  <div id="auth" class="container">
    <button onclick="showRegister()">Регистрация</button>
    <button onclick="showLogin()">Вход</button>
  </div>
  
  <!-- Блок для вывода содержимого (форм, меню, результатов) -->
  <div id="content" class="container"></div>
  
  <script>
    const API_URL = "http://127.0.0.1:5000";
    let userData = null; // После авторизации будет содержать user_id, user_role и token

    // Функция для отображения формы регистрации
    function showRegister() {
      document.getElementById("content").innerHTML = `
        <h3>Регистрация</h3>
        <form id="registerForm">
          <input type="text" id="regUsername" placeholder="Имя пользователя" required />
          <input type="password" id="regPassword" placeholder="Пароль" required />
          <select id="regRole">
            <option value="client">Клиент</option>
            <option value="seller">Продавец</option>
          </select>
          <button type="submit">Зарегистрироваться</button>
        </form>
        <div id="registerResult"></div>
        <button onclick="clearContent()">Назад</button>
      `;
      document.getElementById("registerForm").addEventListener("submit", function(e) {
        e.preventDefault();
        const username = document.getElementById("regUsername").value;
        const password = document.getElementById("regPassword").value;
        const user_role = document.getElementById("regRole").value;
        fetch(API_URL + "/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password, user_role })
        })
        .then(res => res.json())
        .then(data => {
          document.getElementById("registerResult").innerText = JSON.stringify(data);
        })
        .catch(err => console.error(err));
      });
    }

    // Функция для отображения формы входа
    function showLogin() {
      document.getElementById("content").innerHTML = `
        <h3>Вход</h3>
        <form id="loginForm">
          <input type="text" id="loginUsername" placeholder="Имя пользователя" required />
          <input type="password" id="loginPassword" placeholder="Пароль" required />
          <button type="submit">Войти</button>
        </form>
        <div id="loginResult"></div>
        <button onclick="clearContent()">Назад</button>
      `;
      document.getElementById("loginForm").addEventListener("submit", function(e) {
        e.preventDefault();
        const username = document.getElementById("loginUsername").value;
        const password = document.getElementById("loginPassword").value;
        fetch(API_URL + "/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password })
        })
        .then(res => res.json())
        .then(data => {
          document.getElementById("loginResult").innerText = JSON.stringify(data);
          if (data.user_id && data.token) {
            userData = data;
            showUserMenu();
          }
        })
        .catch(err => console.error(err));
      });
    }

    // Отображение меню в зависимости от роли
    function showUserMenu() {
      let html = "";
      if (userData.user_role === "client") {
        html = `
          <h3>Меню клиента</h3>
          <button onclick="listProducts()">Список товаров</button>
          <button onclick="buyProduct()">Покупка товара</button>
          <button onclick="viewPurchaseHistory()">История покупок</button>
          <button onclick="logout()">Выход</button>
          <div id="resultArea"></div>
        `;
      } else if (userData.user_role === "seller") {
        html = `
          <h3>Меню продавца</h3>
          <button onclick="listProducts()">Список товаров</button>
          <button onclick="viewSellerProducts()">Мои товары</button>
          <button onclick="updateProduct()">Обновление товара</button>
          <button onclick="supplyProduct()">Поставка товара</button>
          <button onclick="addCategory()">Новая категория товаров</button>
          <button onclick="listCategories()">Список категорий</button>
          <button onclick="viewSupplyHistory()">История поставок</button>
          <button onclick="logout()">Выход</button>
          <div id="resultArea"></div>
        `;
      }
      document.getElementById("content").innerHTML = html;
    }

    function logout() {
      userData = null;
      clearContent();
    }

    function clearContent() {
      document.getElementById("content").innerHTML = "";
    }

    function formatDate(dateString) {
      let date = new Date(dateString);
      if (isNaN(date)) return "—";
      let day = date.getDate().toString().padStart(2, "0");
      const monthNames = ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"];
      let month = monthNames[date.getMonth()];
      let year = date.getFullYear();
      return `${day} ${month} ${year}`;
    }

    // Генерация таблицы истории покупок
    function generatePurchaseHistoryTable(history) {
      let html = '<table><thead><tr><th>№ покупки</th><th>ID товара</th><th>Кол-во</th><th>Цена</th><th>Итого</th><th>Дата</th></tr></thead><tbody>';
      history.forEach(item => {
        html += `<tr><td>${item.purchase_id}</td><td>${item.product_id}</td><td>${item.quantity}</td><td>${item.price}</td><td>${item.total_price}</td><td>${item.purchase_date?formatDate(item.purchase_date):'—'}</td></tr>`;
      });
      html += '</tbody></table>';
      return html;
    }
    
    function viewPurchaseHistory() {
      document.getElementById('content').innerHTML = `<h3>История покупок</h3><button onclick="fetchPurchaseHistory()">Показать</button><div id="purchaseHistoryResult"></div><button onclick="showUserMenu()">Назад</button>`;
    }
    function fetchPurchaseHistory() {
      fetch(API_URL+`/purchase_history?client_id=${userData.user_id}`,{headers:{'Authorization':'Bearer '+userData.token}})
        .then(r=>r.json())
        .then(data=>{
          const hist = data.purchase_history||[];
          document.getElementById('purchaseHistoryResult').innerHTML = generatePurchaseHistoryTable(hist);
        });
    }

    // Функции для продавца: показать и загрузить его товары с доходом
    function viewSellerProducts() {
      document.getElementById('content').innerHTML = `
        <h3>Мои товары</h3>
        <button onclick="fetchSellerProducts()">Показать мои товары</button>
        <div id="sellerProductsResult"></div>
        <button onclick="showUserMenu()">Назад</button>
      `;
    }

    function fetchSellerProducts() {
      fetch(API_URL + "/seller_products_revenue", {
        headers: { 'Authorization': 'Bearer ' + userData.token }
      })
      .then(res => res.json())
      .then(data => {
        const prods = data.products || [];
        let html = `<table>
          <thead>
            <tr><th>ID</th><th>Название</th><th>Описание</th><th>Цена</th><th>Кол-во</th><th>Заработано</th></tr>
          </thead>
          <tbody>`;
        let total = 0;
        prods.forEach(p => {
          html += `<tr>
            <td>${p.id}</td>
            <td>${p.name}</td>
            <td>${p.description}</td>
            <td>${p.price}</td>
            <td>${p.quantity}</td>
            <td>${p.revenue}</td>
          </tr>`;
          total += p.revenue;
        });
        html += `</tbody></table>`;
        html += `<p><strong>Общий доход: ${total}</strong></p>`;
        document.getElementById('sellerProductsResult').innerHTML = html;
      })
      .catch(err => console.error(err));
    }

    // Функция вывода списка товаров в виде таблицы
    function listProducts() {
      document.getElementById("content").innerHTML = `
        <h3>Список товаров</h3>
        <label for="sortCriteria">Сортировать по:</label>
        <select id="sortCriteria">
          <option value="id">ID</option>
          <option value="price">Цене</option>
          <option value="name">Названию</option>
          <option value="quantity">Количеству</option>
          <option value="date_of_update">Дате обновления</option>
        </select>
        <button onclick="fetchProducts()">Показать товары</button>
        <div id="productsResult"></div>
        <button onclick="showUserMenu()">Назад</button>
      `;
    }

    // Функция получения товаров и их сортировки
    function fetchProducts() {
      fetch(API_URL + "/products")
      .then(res => res.json())
      .then(data => {
        let products = data.products || [];
        const sortCriteria = document.getElementById("sortCriteria").value;
        // Сортировка товаров на стороне клиента
        products.sort((a, b) => {
          if (sortCriteria === "id") {
            return a.id - b.id;
          } else if (sortCriteria === "price") {
            return a.price - b.price;
          } else if (sortCriteria === "name") {
            return a.name.localeCompare(b.name);
          } else if (sortCriteria === "date_of_update") {
            // Предполагаем, что поля date_of_update присутствуют и содержат дату в формате, понятном Date
            let dateA = new Date(a.date_of_update);
            let dateB = new Date(b.date_of_update);
            // Если дата не определена, возвращаем 0, чтобы не менять порядок
            if (isNaN(dateA)) dateA = new Date(0);
            if (isNaN(dateB)) dateB = new Date(0);
            return dateA - dateB;
          } else if (sortCriteria === "quantity") {
            return a.quantity - b.quantity;
          }
          return 0;
        });
        displayProductsTable(products);
      })
      .catch(err => console.error(err));
    }

    // Функция отображения товаров в виде таблицы
    function displayProductsTable(products) {
    let html = `<table>
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Название</th>
                      <th>Описание</th>
                      <th>Цена</th>
                      <th>Количество</th>
                      <th>Дата обновления</th>
                    </tr>
                  </thead>
                  <tbody>`;
    products.forEach(prod => {
      // Если поле date_of_update существует, форматируем его, иначе выводим дефис.
      let date_of_update = prod.date_of_update ? formatDate(prod.date_of_update) : "—";
      html += `<tr>
                <td>${prod.id}</td>
                <td>${prod.name}</td>
                <td>${prod.description}</td>
                <td>${prod.price}</td>
                <td>${prod.quantity}</td>
                <td>${date_of_update}</td>
              </tr>`;
    });
    html += `</tbody></table>`;
    document.getElementById("productsResult").innerHTML = html;
  }

  // Функция для генерации HTML-кода таблицы товаров
  function generateProductsTable(products) {
    let html = `<table>
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Название</th>
                      <th>Описание</th>
                      <th>Цена</th>
                      <th>Количество</th>
                      <th>Дата обновления</th>
                    </tr>
                  </thead>
                  <tbody>`;
    products.forEach(prod => {
      let date_of_update = prod.date_of_update ? formatDate(prod.date_of_update) : "—";
      html += `<tr>
                 <td>${prod.id}</td>
                 <td>${prod.name}</td>
                 <td>${prod.description}</td>
                 <td>${prod.price}</td>
                 <td>${prod.quantity}</td>
                 <td>${date_of_update}</td>
               </tr>`;
    });
    html += `</tbody></table>`;
    return html;
  }

    // Функция для отображения таблицы товаров и формы покупки (для клиента)
    function buyProduct() {
      fetch(API_URL + "/products")
        .then(res => res.json())
        .then(data => {
          let products = data.products || [];
          let html = `<h3>Список товаров</h3>`;
          html += generateProductsTable(products);
          html += `<button onclick="showBuyForm()">Купить товар</button>`;
          html += `<button onclick="showUserMenu()">Назад</button>`;
          document.getElementById("content").innerHTML = html;
        })
        .catch(err => console.error(err));
    }

    // Функции для просмотра истории покупок (для клиента)
    function viewPurchaseHistory() {
      document.getElementById("content").innerHTML = `
        <h3>История покупок</h3>
        <button onclick="fetchPurchaseHistory()">Показать историю покупок</button>
        <div id="purchaseHistoryResult"></div>
        <button onclick="showUserMenu()">Назад</button>
      `;
    }
    function fetchPurchaseHistory() {
      fetch(API_URL + "/purchase_history?client_id=" + userData.user_id, {
        headers: {
          "Authorization": "Bearer " + userData.token
        }
      })
      .then(res => res.json())
      .then(data => {
        document.getElementById("purchaseHistoryResult").innerText = JSON.stringify(data);
      })
      .catch(err => console.error(err));
    }

  // Функция для отображения формы покупки товара (под таблицей)
  function showBuyForm() {
    let html = `
      <h3>Покупка товара</h3>
      <form id="buyForm">
        <input type="number" id="buyProductId" placeholder="ID товара" required />
        <input type="number" id="buyQuantity" placeholder="Количество" required />
        <button type="submit">Купить</button>
      </form>
      <div id="buyResult"></div>
      <button onclick="showUserMenu()">Назад</button>
    `;
    // Добавляем форму под таблицей
    document.getElementById("content").innerHTML += html;
    document.getElementById("buyForm").addEventListener("submit", function(e) {
      e.preventDefault();
      const product_id = parseInt(document.getElementById("buyProductId").value);
      const quantity = parseInt(document.getElementById("buyQuantity").value);
      fetch(API_URL + "/buy", {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Authorization": "Bearer " + userData.token
        },
        body: JSON.stringify({ client_id: userData.user_id, product_id, quantity })
      })
      .then(res => res.json())
      .then(data => {
        document.getElementById("buyResult").innerText = JSON.stringify(data);
      })
      .catch(err => console.error(err));
    });
  }

    // Функция обновления товара (для продавца)
    function updateProduct() {
      document.getElementById("content").innerHTML = `
        <h3>Обновление товара</h3>
        <form id="updateProductForm">
          <input type="number" id="updProductId" placeholder="ID товара" required />
          <select id="updField">
            <option value="product_name">Название</option>
            <option value="price">Цена</option>
            <option value="description">Описание</option>
          </select>
          <input type="text" id="updValue" placeholder="Новое значение" required />
          <button type="submit">Обновить</button>
        </form>
        <div id="updResult"></div>
        <button onclick="showUserMenu()">Назад</button>
      `;
      document.getElementById("updateProductForm").addEventListener("submit", function(e) {
        e.preventDefault();
        const product_id = parseInt(document.getElementById("updProductId").value);
        const field = document.getElementById("updField").value;
        let value = document.getElementById("updValue").value;
        const data = { product_id };
        if (field === "price") {
          data[field] = parseFloat(value);
        } else {
          data[field] = value;
        }
        fetch(API_URL + "/update_product", {
          method: "PUT",
          headers: { 
            "Content-Type": "application/json",
            "Authorization": "Bearer " + userData.token
          },
          body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(data => {
          document.getElementById("updResult").innerText = JSON.stringify(data);
        })
        .catch(err => console.error(err));
      });
    }

    // Функция поставки товара (для продавца)
    function supplyProduct() {
      document.getElementById("content").innerHTML = `
        <h3>Поставка товара</h3>
        <form id="supplyForm">
          <select id="supplyType">
            <option value="existing">Существующий товар</option>
            <option value="new">Новый товар</option>
          </select>
          <div id="supplyFields"></div>
          <button type="submit">Отправить поставку</button>
        </form>
        <div id="supplyResult"></div>
        <button onclick="showUserMenu()">Назад</button>
      `;
      document.getElementById("supplyType").addEventListener("change", renderSupplyFields);
      renderSupplyFields();
      document.getElementById("supplyForm").addEventListener("submit", function(e) {
        e.preventDefault();
        const supplyType = document.getElementById("supplyType").value;
        const data = { seller_id: userData.user_id };
        if (supplyType === "existing") {
          data.is_new = false;
          data.product_id = parseInt(document.getElementById("existProductId").value);
          data.quantity = parseInt(document.getElementById("existQuantity").value);
        } else {
          data.is_new = true;
          data.product_name = document.getElementById("newProductName").value;
          data.category_id = parseInt(document.getElementById("newCategoryId").value);
          data.description = document.getElementById("newDescription").value;
          data.price = parseFloat(document.getElementById("newPrice").value);
          data.quantity = parseInt(document.getElementById("newQuantity").value);
        }
        fetch(API_URL + "/supply", {
          method: "POST",
          headers: { 
            "Content-Type": "application/json",
            "Authorization": "Bearer " + userData.token
          },
          body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(data => {
          document.getElementById("supplyResult").innerText = JSON.stringify(data);
        })
        .catch(err => console.error(err));
      });
    }
    
    // Отрисовка полей для поставки в зависимости от типа
    function renderSupplyFields() {
      const supplyType = document.getElementById("supplyType").value;
      const fieldsDiv = document.getElementById("supplyFields");
      if (supplyType === "existing") {
        fieldsDiv.innerHTML = `
          <input type="number" id="existProductId" placeholder="ID товара" required />
          <input type="number" id="existQuantity" placeholder="Количество" required />
        `;
      } else {
        fieldsDiv.innerHTML = `
          <input type="text" id="newProductName" placeholder="Название товара" required />
          <input type="number" id="newCategoryId" placeholder="ID категории" required />
          <input type="text" id="newDescription" placeholder="Описание товара" />
          <input type="number" id="newPrice" placeholder="Цена" required step="0.01" />
          <input type="number" id="newQuantity" placeholder="Количество" required />
        `;
      }
    }

    // Функция добавления новой категории (для продавца)
    function addCategory() {
      document.getElementById("content").innerHTML = `
        <h3>Добавление категории</h3>
        <form id="addCategoryForm">
          <input type="text" id="catName" placeholder="Название категории" required />
          <button type="submit">Добавить категорию</button>
        </form>
        <div id="addCategoryResult"></div>
        <button onclick="showUserMenu()">Назад</button>
      `;
      document.getElementById("addCategoryForm").addEventListener("submit", function(e) {
        e.preventDefault();
        const category_name = document.getElementById("catName").value;
        fetch(API_URL + "/add_category", {
          method: "POST",
          headers: { 
            "Content-Type": "application/json",
            "Authorization": "Bearer " + userData.token
          },
          body: JSON.stringify({ category_name })
        })
        .then(res => res.json())
        .then(data => {
          document.getElementById("addCategoryResult").innerText = JSON.stringify(data);
        })
        .catch(err => console.error(err));
      });
    }

    // Список категорий для продавца (таблица)
    function listCategories() {
      document.getElementById("content").innerHTML = `
        <h3>Список категорий</h3>
        <button onclick="fetchCategories()">Показать категории</button>
        <div id="categoriesResult"></div>
        <button onclick="showUserMenu()">Назад</button>
      `;
    }

    function fetchCategories() {
      fetch(API_URL + "/categories")
        .then(res => res.json())
        .then(data => {
          const cats = data.categories || [];
          let html = `<table>
            <thead><tr><th>ID</th><th>Название</th></tr></thead><tbody>`;
          cats.forEach(c => {
            html += `<tr><td>${c.id}</td><td>${c.name}</td></tr>`;
          });
          html += `</tbody></table>`;
          document.getElementById("categoriesResult").innerHTML = html;
        })
        .catch(err => console.error(err));
    }

    // Функции для просмотра истории поставок (для продавца)
    function viewSupplyHistory() {
      document.getElementById("content").innerHTML = `
        <h3>История поставок</h3>
        <button onclick="fetchSupplyHistory()">Показать историю поставок</button>
        <div id="supplyHistoryResult"></div>
        <button onclick="showUserMenu()">Назад</button>
      `;
    }
    function fetchSupplyHistory() {
      fetch(API_URL + "/supply_history?seller_id=" + userData.user_id, {
        headers: { "Authorization": "Bearer " + userData.token }
      })
        .then(res => res.json())
        .then(data => {
          const supplies = data.supply_history || [];
          let html = `<table>
            <thead><tr><th>№ поставки</th><th>ID товара</th><th>Количество</th><th>Дата</th></tr></thead><tbody>`;
          supplies.forEach(item => {
            html += `<tr>
              <td>${item.supply_id}</td>
              <td>${item.product_id}</td>
              <td>${item.quantity}</td>
              <td>${formatDate(item.supply_date)}</td>
            </tr>`;
          });
          html += `</tbody></table>`;
          document.getElementById("supplyHistoryResult").innerHTML = html;
        })
        .catch(err => console.error(err));
    }

    // Функции для просмотра истории покупок (изменены только они)
    function viewPurchaseHistory() {
      document.getElementById("content").innerHTML = `
        <h3>История покупок</h3>
        <button onclick="fetchPurchaseHistory()">Показать историю покупок</button>
        <div id="purchaseHistoryResult"></div>
        <button onclick="showUserMenu()">Назад</button>
      `;
    }
    function fetchPurchaseHistory() {
      fetch(API_URL + "/purchase_history?client_id=" + userData.user_id, {
        headers: { "Authorization": "Bearer " + userData.token }
      })
      .then(res => res.json())
      .then(data => {
        const history = data.purchase_history || [];
        let html = `<table>
          <thead>
            <tr><th>№ покупки</th><th>ID товара</th><th>Количество</th><th>Цена за ед.</th><th>Итоговая цена</th><th>Дата</th></tr>
          </thead>
          <tbody>`;
        history.forEach(item => {
          html += `<tr>
            <td>${item.purchase_id}</td>
            <td>${item.product_id}</td>
            <td>${item.quantity}</td>
            <td>${item.price}</td>
            <td>${item.total_price}</td>
            <td>${formatDate(item.purchase_date)}</td>
          </tr>`;
        });
        html += `</tbody></table>`;
        document.getElementById("purchaseHistoryResult").innerHTML = html;
      })
      .catch(err => console.error(err));
    }
  </script>
</body>
</html>
