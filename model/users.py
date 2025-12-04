from sqlalchemy import Column, Integer, String, Boolean
from database.db import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customername = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phonenumber = Column(String, unique=True, nullable=False)
    city=Column(String)
    state=Column (String)
    pincode=Column(Integer)



class Otp(Base):
    __tablename__="otp"
    id=Column(Integer,primary_key=True)
    email=Column(String,nullable=False)
    otp=Column(Integer,nullable=False)
    is_verified = Column(Boolean, default=False)
    