# from flask import Flask, render_template, redirect, jsonify, url_for, request
# from csv import DictReader
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql import functions as func
# from sqlalchemy.orm import DeclarativeBase
# from pathlib import Path
# from db import db
# from models import Customer, Product, Order, ProductOrder

# app = Flask(__name__)

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main_database.db"

# app.instance_path = Path("data").resolve()  

# db.init_app(app)

# @app.route('/')
# def home():
#     return render_template('base.html')

# @app.route('/customers')
# def show_customers():
#     statement = db.select(Customer).order_by(Customer.name)
#     records = db.session.execute(statement)
#     customers = records.scalars()
#     return render_template('customers.html', customers=customers)

# @app.route('/products')
# def show_products():
#     statement = db.select(Product).order_by(Product.name)
#     records = db.session.execute(statement)
#     products = records.scalars()
#     return render_template('products.html', products=products)

# @app.route("/api/customers", methods=["POST"])
# def add_customer(): 
#     data = request.get_json()
#     if not data:
#         return jsonify({"error": "Data not found"}), 400
#     with app.app_context():
#         new_customer = Customer(name=data['name'], phone=data['phone'])
#         db.session.add(new_customer)
#         db.session.commit()
#     return jsonify({"success": "Data found"}), 201

# @app.route("/customer/<int:customer_id>")
# def customer_detail(customer_id):
#     customer = Customer.query.get(customer_id)
    
#     orders = Order.query.filter_by(customer_id=customer_id).all()
    
#     return render_template('customer_detail.html', customer=customer, orders=orders)

# @app.route("/api/customers/<int:customer_id>", methods=["PUT"])
# def update_customer(customer_id): 
#     data = request.get_json()
#     if not data:
#         return jsonify({"error": "Data not found"}), 404
#     customer = db.get_or_404(Customer, customer_id) 

#     if "balance" not in data:
#         return "Invalid request", 400 
    
#     balance = data["balance"]
#     if not isinstance(balance, (int, float)): 
#         return "Invalid request: balance", 400 
    
#     customer.balance = balance  # corrected this line
    
#     db.session.commit() 
#     return jsonify({"success": "Data found"}), 204

# @app.route("/api/customers/<int:customer_id>", methods=["DELETE"])
# def customer_delete(customer_id): 
#     statement = db.select(Customer).where(Customer.id == customer_id) 
#     result = db.session.execute(statement).scalar()
#     if not result:
#         return jsonify({"error": "Customer not found"}), 404
#     db.session.delete(result) 
#     db.session.commit()
#     return jsonify({'status': 'success'}), 204

# # Products
# @app.route("/api/products", methods=["POST"])
# def add_products(): 
#     data = request.get_json()
#     if not data:
#         return jsonify({"error": "Data not found"}), 400
#     with app.app_context():
#         new_product = Customer(name=data['name'], phone=data['price'])
#         db.session.add(new_product)
#         db.session.commit()
#     return jsonify({"success": "Data found"}), 201

# @app.route("/api/products/<int:product_id>", methods=["PUT"])
# def update_products(product_id): 
#     data = request.get_json()
#     if not data:
#         return jsonify({"error": "Data not found"}), 404
#     product = db.get_or_404(Product, product_id)

#     if "name" not in data or "price" not in data:
#         return "Invalid request", 400 
    
#     name = data["name"]
#     price = data["price"]
#     if not isinstance(price, (int, float)): 
#         return "Invalid request: balance", 400 
    
#     product.name = name
#     product.price = price
    
#     db.session.commit() 
#     return jsonify({"success": "Data found"}), 204

# @app.route("/api/products/<int:product_id>", methods=["DELETE"])
# def customer_products(product_id): 
#     statement = db.select(Product).where(Product.id == product_id) 
#     result = db.session.execute(statement).scalar()
#     if not result:
#         return jsonify({"error": "Product not found"}), 404
#     db.session.delete(result) 
#     db.session.commit()
#     return jsonify({'status': 'success'}), 204

# @app.route("/api/customers/<int:customer_id>")
# def customer_detail_json(customer_id): 
#     statement = db.select(Customer).where(Customer.id == customer_id) 
#     result = db.session.execute(statement).scalar()
#     return jsonify(result.to_json())

# @app.route("/api/orders", methods=["POST"])
# def add_order():
#     data = request.get_json()
#     if not data:
#         return jsonify({"error": "Data not found"}), 400
    
#     customer = db.get_or_404(Customer, data['customer_id'])
#     if not customer:
#         return jsonify({"error": "Customer not found"}), 404
    
#     if not data.get('items'):
#         return jsonify({"error": "No items found"}), 404
    
#     with app.app_context():
#         order = Order(customer_id=customer.id, total=len(data['items']))
#         db.session.add(order)
#         db.session.commit()
    
#     for i in data['items']:
#         statement = db.select(Product).where(Product.name == i['name']) 
#         result = db.session.execute(statement).scalar()
        
#         if not result:
#             return jsonify({"error": "Product not found"}), 404
        
#     return jsonify({"success": "Data found"}), 201

# @app.route('/orders/<int:order_id>/delete', methods=['POST'])
# def delete_order(order_id):
#     order = Order.query.get_or_404(order_id)
#     if order.processed:
#         return redirect(url_for('show_orders'))
#     db.session.delete(order)
#     db.session.commit()
#     return redirect(url_for('show_orders'))

# @app.route("/orders/<int:order_id>")
# def specific_orders(order_id): 
#     statement = db.select(Order).where(Order.id == order_id) 
#     result = db.session.execute(statement).scalar()

#     return render_template('specific_order.html', order=result)

# @app.route("/orders")
# def show_orders(): 
#     statement = db.select(Order)
#     records = db.session.execute(statement)
#     orders = records.scalars()
#     for i in orders:
#         i.total = i.price
#         print(i.total)
#     return render_template('orders.html', orders=orders)

# @app.route('/api/orders/<int:order_id>', methods=['PUT'])
# def process_order(order_id):
#     data = request.get_json()
#     if not data:
#         return jsonify({"error": "Order not found"}), 404
#     if data['process'] != True:
#         return jsonify({"error": "Order ignored"}), 400
    
#     order = db.get_or_404(Order, order_id)
#     if not data.get("strategy"):
#         test = order.process()
#     else:
#         test = order.process(data["strategy"])
#     if test:
#         return jsonify({"success": "Found"}), 201

# @app.route('/orders/<int:id>/process', methods=['POST'])
# def process(id):
#     order = Order.query.get_or_404(id)
#     if order.processed:
#         return redirect(url_for('show_orders'))
#     order.process()
#     db.session.commit()
#     return redirect(url_for('show_orders'))

# @app.route("/product_orders")
# def show_product_orders(): 
#     statement = db.select(ProductOrder).order_by(ProductOrder.quantity)
#     records = db.session.execute(statement)
#     product_orders = records.scalars()
#     return render_template('product_orders.html', product_orders=product_orders)

# if __name__ == '__main__':
#     app.run(debug=True, port=8080)