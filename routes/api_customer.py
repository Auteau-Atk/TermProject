from flask import Blueprint, request, jsonify
from db import db
from models import Customer

api_customer = Blueprint('api_customer', __name__)

@api_customer.route('/', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([customer.to_jsonialize() for customer in customers])

@api_customer.route('/', methods=['POST'])
def create_customer():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Data not found"}), 400
    new_customer = Customer(name=data['name'], phone=data['phone'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"success": "Data found"}), 201

@api_customer.route('/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({'status': 'error'}), 404
    return jsonify(customer.to_jsonialize())


@api_customer.route('/<int:id>', methods=['DELETE'])
def delete_customer(customer_id):
    statement = db.select(Customer).where(Customer.id == customer_id) 
    result = db.session.execute(statement).scalar()
    if not result:
        return jsonify({"error": "Customer not found"}), 404
    db.session.delete(result) 
    db.session.commit()
    return jsonify({'status': 'success'}), 204

@api_customer.route('/<int:customer_id>', methods=['PUT'])
def all_bal(customer_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Data not found"}), 404
    customer = db.get_or_404(Customer, customer_id) 

    if "balance" not in data:
        return "Invalid request", 400 
    
    balance = data["balance"]
    if not isinstance(balance, (int, float)): 
        return "Invalid request: balance", 400 
    
    customer.balance = balance
    
    db.session.commit() 
    return jsonify({"success": "Data found"}), 204