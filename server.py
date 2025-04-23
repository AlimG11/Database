from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_migrate import Migrate # type: ignore
from flask_cors import CORS
from sqlalchemy import func # type: ignore
from datetime import date
import uuid

app = Flask(__name__)
CORS(app)

# Настройки подключения
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Сессии
sessions = {}

# Модели
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    user_role = db.Column(db.String, nullable=False)  # 'client' или 'seller'
    created_at = db.Column(db.Date, default=date.today)

class ProductCategory(db.Model):
    __tablename__ = 'product_categories'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String, nullable=False)

class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.category_id'), nullable=False)
    description = db.Column(db.String)
    price = db.Column(db.Numeric, nullable=False)
    total_quantity = db.Column(db.Integer, nullable=False)
    date_of_update = db.Column(db.Date, default=date.today)

class PurchaseHistory(db.Model):
    __tablename__ = 'purchase_history'
    purchase_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    total_price = db.Column(db.Numeric, nullable=False)
    purchase_date = db.Column(db.Date, default=date.today)

class SupplyHistory(db.Model):
    __tablename__ = 'supply_history'
    supply_id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    supply_date = db.Column(db.Date, default=date.today)

# Аутентификация

def get_auth_token():
    auth = request.headers.get('Authorization')
    if not auth or not auth.startswith('Bearer '):
        return None
    return auth[7:]

def require_auth(expected_role=None):
    token = get_auth_token()
    if not token or token not in sessions:
        return jsonify({"error": "Неавторизованный запрос"}), 401
    user = sessions[token]
    if expected_role and user.get("role") != expected_role:
        return jsonify({"error": "Недостаточно прав"}), 403
    return user

# Маршруты

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user = User(username=data['username'], password=data['password'], user_role=data['user_role'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Регистрация прошла успешно."})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if not user:
        return jsonify({"error": "Неверное имя пользователя или пароль."}), 401
    token = str(uuid.uuid4())
    sessions[token] = {"user_id": user.user_id, "role": user.user_role}
    return jsonify({"message": "Успешный вход", "user_id": user.user_id, "user_role": user.user_role, "token": token})

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = ProductCategory.query.all()
    return jsonify({"categories": [{"id": c.category_id, "name": c.category_name} for c in categories]})

@app.route('/add_category', methods=['POST'])
def add_category():
    auth = require_auth("seller")
    if isinstance(auth, tuple): return auth
    data = request.json
    category = ProductCategory(category_name=data['category_name'])
    db.session.add(category)
    db.session.commit()
    return jsonify({"message": "Категория успешно добавлена.", "category_id": category.category_id})

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.filter(Product.total_quantity > 0).all()
    return jsonify({"products": [{
        "id": p.product_id,
        "name": p.product_name,
        "description": p.description,
        "price": float(p.price),
        "quantity": p.total_quantity,
        "date_of_update": p.date_of_update.isoformat()
    } for p in products]})

@app.route('/buy', methods=['POST'])
def buy():
    auth = require_auth("client")
    if isinstance(auth, tuple): return auth
    data = request.json
    product = Product.query.get(data['product_id'])
    if not product or product.total_quantity < data['quantity']:
        return jsonify({"error": "Недостаточно товара"}), 400
    purchase = PurchaseHistory(
        client_id=data['client_id'],
        product_id=data['product_id'],
        quantity=data['quantity'],
        price=product.price,
        total_price=product.price * data['quantity']
    )
    product.total_quantity -= data['quantity']
    db.session.add(purchase)
    db.session.commit()
    return jsonify({"message": "Покупка совершена успешно."})

@app.route('/purchase_history', methods=['GET'])
def get_purchase_history():
    auth = require_auth("client")
    if isinstance(auth, tuple): return auth
    client_id = request.args.get("client_id", type=int)
    if client_id != auth["user_id"]:
        return jsonify({"error": "Неверный client_id"}), 403
    purchases = PurchaseHistory.query.filter_by(client_id=client_id).all()
    return jsonify({"purchase_history": [{
        "purchase_id": p.purchase_id,
        "product_id": p.product_id,
        "quantity": p.quantity,
        "price": float(p.price),
        "total_price": float(p.total_price),
        "purchase_date": p.purchase_date.isoformat()
    } for p in purchases]})

@app.route('/supply', methods=['POST'])
def supply():
    auth = require_auth("seller")
    if isinstance(auth, tuple): return auth
    data = request.json
    if data.get("is_new"):
        product = Product(
            product_name=data['product_name'],
            seller_id=auth['user_id'],
            category_id=data['category_id'],
            description=data.get('description'),
            price=data['price'],
            total_quantity=data['quantity']
        )
        db.session.add(product)
        db.session.flush()
    else:
        product = Product.query.get(data['product_id'])
        if not product:
            return jsonify({"error": "Товар не найден"}), 404
        product.total_quantity += data['quantity']
    supply = SupplyHistory(
        seller_id=auth['user_id'],
        product_id=product.product_id,
        quantity=data['quantity']
    )
    db.session.add(supply)
    db.session.commit()
    return jsonify({"message": "Поставка товара успешно выполнена."})

@app.route('/supply_history', methods=['GET'])
def supply_history():
    auth = require_auth("seller")
    if isinstance(auth, tuple): return auth
    seller_id = request.args.get("seller_id", type=int)
    if seller_id != auth['user_id']:
        return jsonify({"error": "Неверный seller_id"}), 403
    history = SupplyHistory.query.filter_by(seller_id=seller_id).all()
    return jsonify({"supply_history": [{
        "supply_id": h.supply_id,
        "product_id": h.product_id,
        "quantity": h.quantity,
        "supply_date": h.supply_date.isoformat()
    } for h in history]})

@app.route('/update_product', methods=['PUT'])
def update_product():
    auth = require_auth("seller")
    if isinstance(auth, tuple):
        return auth
    data = request.json or {}
    product_id = data.get('product_id')
    if not product_id:
        return jsonify({"error": "Не указан ID товара"}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Товар не найден"}), 404

    # Новая проверка: только владелец (seller_id) может редактировать
    if product.seller_id != auth['user_id']:
        return jsonify({"error": "Нет прав на изменение этого товара"}), 403

    # Применяем изменения
    if 'product_name' in data:
        product.product_name = data['product_name']
    if 'price' in data:
        product.price = data['price']
    if 'description' in data:
        product.description = data['description']

    db.session.commit()
    return jsonify({"message": "Товар успешно обновлён."})


@app.route('/seller_products_revenue', methods=['GET'])
def seller_products_revenue():
    auth = require_auth("seller")
    if isinstance(auth, tuple): return auth
    seller_id = auth['user_id']
    query = db.session.query(
        Product,
        func.coalesce(func.sum(PurchaseHistory.total_price), 0).label("revenue")
    ).outerjoin(PurchaseHistory, Product.product_id == PurchaseHistory.product_id) \
    .filter(Product.seller_id == seller_id) \
    .group_by(Product.product_id)

    result = [
        {
            "id": p.product_id,
            "name": p.product_name,
            "description": p.description,
            "price": float(p.price),
            "quantity": p.total_quantity,
            "revenue": float(rev)
        }
        for p, rev in query.all()
    ]
    return jsonify({"products": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
