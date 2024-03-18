from flask import Flask, render_template
from csv import DictReader
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from pathlib import Path
from db import db
from models import Customer, Product

app = Flask(__name__)

# This will make Flask use a 'sqlite' database with the filename provided
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///i_copy_pasted_this.db"
# This will make Flask store the database file in the path provided
app.instance_path = Path("data").resolve()  
# Adjust to your needs / liking. Most likely, you want to use "." for your instance path. You may also use "data".
db.init_app(app)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/customers')
def show_customers():
    """Route to display a list of customers."""
    statement = db.select(Customer).order_by(Customer.name)
    records = db.session.execute(statement)
    customers = records.scalars()
    return render_template('customers.html', customers=customers)

@app.route('/products')
def show_products():
    """Route to display a list of products."""
    statement = db.select(Product).order_by(Product.name)
    records = db.session.execute(statement)
    products = records.scalars()
    return render_template('products.html', products=products)



if __name__ == '__main__':
    app.run(debug=True, port=8080)