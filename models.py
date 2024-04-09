from sqlalchemy import Boolean, Float, Numeric, ForeignKey, Integer, String 
from sqlalchemy.orm import mapped_column, relationship 
from datetime import datetime

from db import db 

class Customer(db.Model):
    id = mapped_column(Integer, primary_key=True) 
    name = mapped_column(String(200), nullable=False, unique=True) 
    phone = mapped_column(String(20), nullable=False) 
    balance = mapped_column(Numeric, nullable=False, default=0)

    orders = relationship("Order")

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'balance': self.balance
        }

class Product(db.Model): 
    id = mapped_column(Integer, primary_key=True) 
    name = mapped_column(String(200), nullable=False, unique=True) 
    price = mapped_column(Integer, nullable=False)
    available = mapped_column(Numeric, nullable=False, default=0)
    
    product_orders = relationship("ProductOrder")
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'balance': self.balance
        }
    
class Order(db.Model): 
    id = mapped_column(Integer, primary_key=True)
    customer_id = mapped_column(Integer, ForeignKey(Customer.id), nullable=False) 
    total = mapped_column(Numeric, nullable=True)
    created = mapped_column(String(20), default=datetime.now, nullable=False)
    processed = mapped_column(String(20), nullable=True)
    customer = relationship("Customer", back_populates="orders")

    product_orders = relationship("ProductOrder", cascade="all, delete-orphan")
    def process(self,strategy="adjust"):
        if self.processed == 'None':
            return False, "Already processed"
        if (self.customer.balance <= 0 ):
            return False, "Poor lol"
        for u in self.product_orders:
            if u.quantity > u.product.available:
                if strategy == "adjust":
                    u.quantity = u.product.available #adjust
                if strategy == "reject":
                    return False, "Order too big"
                if strategy == "ignore":
                    u.quantity = 0 # ignore
                    
            u.product.available = u.product.available - u.quantity
            self.customer.balance = self.customer.balance - int(u.product.price * u.quantity )
            self.processed = datetime.now()
        db.session.commit()
        return True, self.processed
    def price(self):
        return format((sum([(u.product.price) * u.quantity for u in self.product_orders])), '.2f')
    
class ProductOrder(db.Model):
    id = mapped_column(Integer, primary_key=True)
    order_id = mapped_column(Integer, ForeignKey(Order.id), nullable=False)
    product_id = mapped_column(Integer, ForeignKey(Product.id), nullable=False)
    quantity = mapped_column(Integer, nullable=False)

    order = relationship("Order", back_populates="product_orders")
    product = relationship("Product", back_populates="product_orders")