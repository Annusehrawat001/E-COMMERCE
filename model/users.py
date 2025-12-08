
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db import Base

# -------------------- CUSTOMER --------------------
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customername = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phonenumber = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    city = Column(String)
    state = Column(String)
    pincode = Column(Integer)
    otp = Column(String, nullable=True)
    verified = Column(Boolean, default=False)

    orders = relationship("Order", back_populates="customer")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    total_amount = Column(Integer, nullable=False)
    status = Column(String, default="Pending")
    created = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="orders")


# -------------------- MANUFACTURER --------------------
class Manufacturer(Base):
    __tablename__ = "manufacturers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=True)
    country = Column(String, nullable=True)

    products = relationship("Product", back_populates="manufacturer")


# -------------------- CATEGORY --------------------
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    products = relationship("Product", back_populates="category")


# -------------------- PRODUCT --------------------
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)
    stock = Column(Integer, default=0)
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    manufacturer = relationship("Manufacturer", back_populates="products")
    category = relationship("Category", back_populates="products")
