from sqlalchemy import Boolean, Float, Numeric, ForeignKey, Integer, String 
from sqlalchemy.orm import mapped_column, relationship 

from db import db 

class Customer(db.Model): 
    id = mapped_column(Integer, primary_key=True) 
    name = mapped_column(String(200), nullable=False, unique=True) 
    phone = mapped_column(String(20), nullable=False) 
    balance = mapped_column(Numeric, nullable=False, default=0)

class Product(db.Model): 
    id = mapped_column(Integer, primary_key=True) 
    name = mapped_column(String(200), nullable=False, unique=True) 
    price = mapped_column(String(20), nullable=False) 
    balance = mapped_column(Numeric, nullable=False, default=0)