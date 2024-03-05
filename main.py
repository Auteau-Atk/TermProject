from flask import Flask, render_template
from csv import DictReader
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.orm import DeclarativeBase 

class Base(DeclarativeBase): 
    pass 

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

# This will make Flask use a 'sqlite' database with the filename provided 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///i_copy_pasted_this.db"
# This will make Flask store the database file in the path provided 
app.instance_path = Path("data").resolve() 
# Adjust to your needs / liking. Most likely, you want to use "." for your instance path. You may also use "data".
db.init_app(app)

@app.route('/')
def home():
    return render_template('customers.html')

@app.route('/customers')
def customers():
    with open('./data/customers.csv', 'r') as file:
        reader_csv = DictReader(file)
        return render_template('customers.html', customers = reader_csv)

@app.route('/products')
def products():
    with open('./data/products.csv', 'r') as file:
        reader_csv = DictReader(file)
        return render_template('products.html', products = reader_csv)



if __name__ == '__main__':
    app.run(debug=True, port=8080)
