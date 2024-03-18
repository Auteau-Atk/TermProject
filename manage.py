from main import app, db
from models import Customer, Product
from csv import DictReader

def drop_all_tables():
    """Drop all tables from the database."""
    with app.app_context():
        db.drop_all()

def create_all_tables():
    """Create all tables in the database."""
    with app.app_context():
        db.create_all()

def import_data_from_csv(customers_csv_path, products_csv_path):
    """
    Import data from CSV files, create instances, and save them to the database.
    
    Args:
        customers_csv_path (str): Path to the CSV file containing customer data.
        products_csv_path (str): Path to the CSV file containing product data.
    """
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

if __name__ == '__main__':
    # Example usage
    # drop_all_tables()
    create_all_tables()
    import_data_from_csv('./data/customers.csv', './data/products.csv')
