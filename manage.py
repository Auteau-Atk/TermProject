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
        random_cust = db.select(Customer).order_by(func.random()).limit(1)
        cust_records = db.session.execute(random_cust).scalar()

        random_prod = db.select(Product).order_by(func.random()).limit(1)
        prod_records = db.session.execute(random_prod).scalar()

        product_order = ProductOrder(customer_id = cust_records.id, 
                                    product_id = prod_records.id, 
                                    quantity = random.randint(0, 20))
        db.session.commit()

if __name__ == '__main__':
    # Example usage
    # drop_all_tables()
    # create_all_tables()
    # import_data_from_csv('./data/customers.csv', './data/products.csv')
    randomize_orders()
