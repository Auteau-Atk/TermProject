from app import app, db
from sqlalchemy.sql import functions as func
from models import Customer, Product, ProductOrder, Order
from csv import DictReader
import random

def drop_all_tables():
    with app.app_context():
        db.drop_all()

def create_all_tables():
    with app.app_context():
        db.create_all()

def import_data_from_csv(customers_csv_path, products_csv_path):
    with app.app_context():
        with open(customers_csv_path, 'r') as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                customer = Customer(name=row['name'], phone=row['phone'], balance = random.uniform(100.00,2000.00))
                db.session.add(customer)
        
        with open(products_csv_path, 'r') as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                product = Product(name=row['name'], price=row['price'], available = random.randint(1000,2000))
                db.session.add(product)
        
        db.session.commit()
def randomize_orders():
    with app.app_context():

        rand_qty = random.randint(10, 20) 
        
        cust_stmt = db.select(Customer).order_by(func.random()).limit(1) 
        customer = db.session.execute(cust_stmt).scalar() 
        
        order = Order(customer=customer) 
        db.session.add(order) 
        
        prod_stmt = db.select(Product).order_by(func.random()).limit(1) 
        product = db.session.execute(prod_stmt).scalar() 
        
        association_1 = ProductOrder(order=order, product=product, quantity=rand_qty) 
        db.session.add(association_1) 
        
        prod_stmt = db.select(Product).order_by(func.random()).limit(1) 
        product = db.session.execute(prod_stmt).scalar() 
        rand_qty = random.randint(10, 20) 
        association_2 = ProductOrder(order=order, product=product, quantity=rand_qty) 
        db.session.add(association_2) 
        
        db.session.commit() 

if __name__ == '__main__':
    drop_all_tables()
    create_all_tables()
    import_data_from_csv('./data/customers.csv', './data/products.csv')
    for i in range(0, 20):
        randomize_orders()