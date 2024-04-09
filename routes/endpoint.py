from flask import Blueprint, render_template, redirect, url_for, request
from db import db
from models import Customer, Order, Product

endpoint = Blueprint('pages', __name__)

@endpoint.route('/')
def homepage():
    return render_template("base.html")

@endpoint.route('/customers', methods=['GET'])
def get_customers():
    statement = db.select(Customer).order_by(Customer.name)
    records = db.session.execute(statement)
    customers = records.scalars()
    return render_template('customers.html', customers=customers)

@endpoint.route('/products', methods=['GET'])
def get_products():
    statement = db.select(Product).order_by(Product.name)
    records = db.session.execute(statement)
    products = records.scalars()
    return render_template('products.html', products=products)

@endpoint.route('/orders', methods=['GET'])
def get_orders():
    request = db.session.execute(db.select(Order).order_by(Order.id)) 
    orders = []
    for i in request.scalars():
        order = {
            "id": i.id, 
            "customer_id": i.customer_id, 
            "products": [f"{p.product.product_orders} ({p.quantity})" for p in i.product_orders], 
            'total': Order.price(i),
            "processed": None
        }
        order['processed'] = i.processed or "Not processed"
        
        orders.append(order)
    
    return render_template("./orders.html", orders=orders)

@endpoint.route('/order/<int:id>', methods=['GET'])
def get_order(id):
    request = db.session.execute(db.select(Order).where(Order.id == id)).scalars().first()
    if not request:
        return redirect(url_for('pages.get_orders'))
    orders = []
    order = {
        'name': request.customer.name,
        'balance': int(request.customer.balance),
        'products': [f"{p.product.product} ({p.quantity} ${format((p.product.price*p.quantity),'.2f')})" for p in order.product_orders],
        'price':  Order.price(request),
    }
    orders.append(order)
    return render_template("detailed_order.html",id = id, orders = orders, customer_id=order.customer.id, processed = order.processed)

@endpoint.route('/customer/<int:id>', methods=['GET'])
def get_customer(id):
    request = db.session.execute(db.select(Customer).where(Customer.id == id)).scalars().first()
    if not customer:
        return redirect(url_for('html.get_customers'))
    
    customers = []
    
    customer = {
        "id": request.id, 
        "name": request.name, 
        "phone": request.phone, 
        'balance': int(request.balance), 
        'orders': request.orders
    }
    customers.append(customer)
    
    return render_template("detailed.html",id = id, customer = request.name, customers = customers)

@endpoint.route('/orders/<int:id>/delete', methods=['POST'])
def delete_order(id):
    order = Order.query.get_or_404(id)
    if order.processed:
        return redirect(url_for('pages.get_orders'))
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('pages.get_orders'))

@endpoint.route('/orders/<int:id>/process', methods=['POST'])
def process_order(id):
    order = Order.query.get_or_404(id)
    if order.processed:
        return redirect(url_for('pages.get_orders'))
    order.process()
    db.session.commit()
    return redirect(url_for('pages.get_orders'))
