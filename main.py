from flask import Flask, render_template, redirect, jsonify, url_for, request
from csv import DictReader
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from pathlib import Path
from db import db
from models import Customer, Product, Order, ProductOrder

app = Flask(__name__)

# This will make Flask use a 'sqlite' database with the filename provided
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main_database.db"
# This will make Flask store the database file in the path provided
app.instance_path = Path("data").resolve()  
# Adjust to your needs / liking. Most likely, you want to use "." for your instance path. You may also use "data".
db.init_app(app)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/customers')
def show_customers():
    statement = db.select(Customer).order_by(Customer.name)
    records = db.session.execute(statement)
    customers = records.scalars()
    return render_template('customers.html', customers=customers)

@app.route('/products')
def show_products():
    statement = db.select(Product).order_by(Product.name)
    records = db.session.execute(statement)
    products = records.scalars()
    return render_template('products.html', products=products)

@app.route("/api/customers")
def customers_json(): 
    statement = db.select(Customer).order_by(Customer.name) 
    results = db.session.execute(statement) 
    print(type(results))
    customers = [] # output variable 
    for customer in results.scalars():
        json_record = { 
            "id": customer.id, 
            "name": customer.name, 
            "phone": customer.phone, 
            "balance": customer.balance, 
        } 
        customers.append(json_record) 

    return jsonify(customers)

@app.route("/api/customers/<int:customer_id>")
def customer_detail_json(customer_id): 
    statement = db.select(Customer).where(Customer.id == customer_id) 
    result = db.session.execute(statement).scalar()
    
    json_record = { 
            "id": result.id, 
            "name": result.name, 
            "phone": result.phone, 
            "balance": result.balance, 
        }

    return jsonify(json_record)

@app.route("/api/customers/<int:customer_id>", methods=["DELETE"])
def customer_delete(customer_id): 
    customer = db.session.execute(db.select(Customer).where(Customer.id == 
customer_id)).scalar() 
    db.session.delete(customer) 
    db.session.commit()

    return "deleted"

@app.route("/api/orders", methods=["POST"])
def accept_orders():
    if request.method == "POST":
        data = {
        'customer_id': request.form['customer_id'],
        'items': [
        {"name": request.form['item'],'quantity': request.form['quantity']}
        ]
    }

        return jsonify({"message": "Order submitted successfully"})

    return jsonify({"error": "Method Not Allowed"}), 405

@app.route("/api/orders", methods=["GET"])
def submit_orders():
    return render_template('send_order.html')


@app.route('/orders/<int:order_id>/delete', methods=['POST'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('show_orders'))

@app.route("/orders/<int:order_id>/delete", methods=["GET"])
def remove_orders(order_id):
    return render_template('delete_order.html', order_id=order_id)

@app.route("/orders/<int:order_id>")
def specific_orders(order_id): 
    statement = db.select(Order).where(Order.id == order_id) 
    result = db.session.execute(statement).scalar()

    return render_template('specific_order.html', order=result)

@app.route("/orders")
def show_orders(): 
    statement = db.select(Order).order_by(Order.total)
    records = db.session.execute(statement)
    orders = records.scalars()
    return render_template('orders.html', orders=orders)

@app.route("/product_orders")
def show_product_orders(): 
    statement = db.select(ProductOrder).order_by(ProductOrder.quantity)
    records = db.session.execute(statement)
    product_orders = records.scalars()
    return render_template('product_orders.html', product_orders=product_orders)

if __name__ == '__main__':
    app.run(debug=True, port=8080)