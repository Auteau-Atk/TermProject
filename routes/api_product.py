from flask import Blueprint, request, jsonify
from db import db
from models import Product

api_product = Blueprint('api_product', __name__)

@api_product.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_json() for product in products])

@api_product.route('/', methods=['POST'])
def create_product():
    data = request.get_json()
    
    if data['name'] == '' or data['price'] == '' or not data:
        return jsonify({'status': 'error'}), 400
    
    product = Product(product = data['name'], price = data['price'])

    if product:
        db.session.add(product)
        db.session.commit()
        return jsonify({'status': 'success'}), 201
    else:
        return jsonify({'status': 'error'}), 400

@api_product.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({'status': 'error'}), 404
    
    return jsonify(product.to_json())

@api_product.route('/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'status': 'error'}), 404
    
    data = request.get_json()
    if data['name'] == '' or data['price'] == '' or data['available'] == '' or not data:
        return jsonify({'status': 'error'}), 400
    
    product.name = data['name']
    product.price = data['price']
    product.available = data['available']

    db.session.commit()
    return jsonify({'status': 'success'})

@api_product.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    return jsonify({'status': 'success'})

