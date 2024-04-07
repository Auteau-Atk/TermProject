from main import app, db
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
        # Import customer data
        with open(customers_csv_path, 'r') as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                customer = Customer(name=row['name'], phone=row['phone'])
                db.session.add(customer)
        
        # Import product data
        with open(products_csv_path, 'r') as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                product = Product(name=row['name'], price=row['price'])
                db.session.add(product)
        
        # Commit changes
        db.session.commit()
def randomize_orders():
    with app.app_context():

        rand_qty = random.randint(10, 20) 
        # Find a random customer 
        cust_stmt = db.select(Customer).order_by(func.random()).limit(1) 
        customer = db.session.execute(cust_stmt).scalar() 
        
        # Make an order 
        order = Order(customer=customer, total=rand_qty) 
        db.session.add(order) 
        
        # Find a random product 
        prod_stmt = db.select(Product).order_by(func.random()).limit(1) 
        product = db.session.execute(prod_stmt).scalar() 
        
        # Add that product to the order 
        association_1 = ProductOrder(order=order, product=product, quantity=rand_qty) 
        db.session.add(association_1) 
        
        # Do it again 
        prod_stmt = db.select(Product).order_by(func.random()).limit(1) 
        product = db.session.execute(prod_stmt).scalar() 
        rand_qty = random.randint(10, 20) 
        association_2 = ProductOrder(order=order, product=product, quantity=rand_qty) 
        db.session.add(association_2) 
        
        # Commit to the database 
        db.session.commit() 

if __name__ == '__main__':
    # Example usage
    drop_all_tables()
    create_all_tables()
    import_data_from_csv('./data/customers.csv', './data/products.csv')
    randomize_orders()
    randomize_orders()
    randomize_orders()
