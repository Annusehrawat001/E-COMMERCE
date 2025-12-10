
#
import random
from datetime import datetime, timedelta
from typing import Optional
from database.db import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext
from jose import jwt

from model.users import Customer, Manufacturer, Category, Product
from schema.schema import CustomerCreate, VerifyOTP, LoginSchema, ResetPasswordSchema, ManufacturerCreate, CategoryCreate, ProductCreate,ProductSearch

# TOKEN 
SECRET_KEY = "MESSHO"
ALGORITHM = "HS256"
EXPIRY_MINUTES = 60 * 24

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(pwd: str) :
    return pwd_context.hash(pwd)

def verify_password(plain: str, hashed: str) :
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expiry_minutes: Optional[int] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=(expiry_minutes or EXPIRY_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ---------------- Customer ----------------
def register_customer(data: CustomerCreate, db: Session):
    if db.query(Customer).filter(Customer.email == data.email).first():
        raise HTTPException(status_code=409, detail="Email already exists")
    if db.query(Customer).filter(Customer.phonenumber == data.phonenumber).first():
        raise HTTPException(status_code=409, detail="Phone number already exists")

    otp = str(random.randint(1000, 9999))
    new = Customer(
        customername=data.customername,
        email=data.email,
        phonenumber=data.phonenumber,
        password=hash_password(data.password),
        city=data.city,
        state=data.state,
        pincode=data.pincode,
        otp=otp,
        verified=False
    )
    db.add(new)
    db.commit()
    db.refresh(new)

    return {"msg": "OTP generated", "otp": otp, "email": new.email}

def verify_otp(data: VerifyOTP, db: Session):
    user = db.query(Customer).filter(Customer.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.otp != data.otp:
        raise HTTPException(status_code=400, detail="Incorrect OTP")
    user.verified = True
    user.otp = None
    db.commit()
    return {"msg": "OTP verified"}

def login_user(data: LoginSchema, db: Session):
    user = db.query(Customer).filter(Customer.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not user.verified:
        raise HTTPException(status_code=403, detail="OTP not verified")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "id": user.id}

def send_reset_otp(email: str, db: Session):
    user = db.query(Customer).filter(Customer.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    otp = random.randint(1000, 9999)
    user.otp = str(otp)
    db.commit()
    return {"msg": "OTP generated for reset", "otp": otp}

def reset_password(data: ResetPasswordSchema, db: Session):
    user = db.query(Customer).filter(Customer.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.otp is None or int(user.otp) != data.otp:
        raise HTTPException(status_code=400, detail="Incorrect OTP")
    user.password = hash_password(data.new_password)
    user.otp = None
    db.commit()
    return {"msg": "Password reset successful"}


# ---------------- Manufacturer ----------------
def create_manufacturer(data: ManufacturerCreate, db: Session):
    if db.query(Manufacturer).filter(Manufacturer.name == data.name).first():
        raise HTTPException(status_code=409, detail="Manufacturer already exists")
    m = Manufacturer(name=data.name, email=data.email, country=data.country)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

def get_all_manufacturers(db: Session):
    return db.query(Manufacturer).all()

def get_manufacturer(man_id: int, db: Session):
    m = db.query(Manufacturer).filter(Manufacturer.id == man_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    return m

def update_manufacturer(man_id: int, data: ManufacturerCreate, db: Session):
    m = db.query(Manufacturer).filter(Manufacturer.id == man_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    m.name = data.name
    m.email = data.email
    m.country = data.country
    db.commit()
    db.refresh(m)
    return m

def delete_manufacturer(man_id: int, db: Session):
    m = db.query(Manufacturer).filter(Manufacturer.id == man_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    db.delete(m)
    db.commit()
    return {"msg": "Manufacturer deleted"}


# ---------------- Category ----------------
def create_category(data: CategoryCreate, db: Session):
    if db.query(Category).filter(Category.name == data.name).first():
        raise HTTPException(status_code=409, detail="Category already exists")
    c = Category(name=data.name, description=data.description)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

def get_all_categories(db: Session):
    return db.query(Category).all()

def get_category(cat_id: int, db: Session):
    c = db.query(Category).filter(Category.id == cat_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Category not found")
    return c

def update_category(cat_id: int, data: CategoryCreate, db: Session):
    c = db.query(Category).filter(Category.id == cat_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Category not found")
    c.name = data.name
    c.description = data.description
    db.commit()
    db.refresh(c)
    return c

def delete_category(cat_id: int, db: Session):
    c = db.query(Category).filter(Category.id == cat_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(c)
    db.commit()
    return {"msg": "Category deleted"}


# ---------------- Product ----------------
def create_product(data: ProductCreate, db: Session):
    if data.manufacturer_id:
        if not db.query(Manufacturer).filter(Manufacturer.id == data.manufacturer_id).first():
            raise HTTPException(status_code=404, detail="Manufacturer not found")
    if data.category_id:
        if not db.query(Category).filter(Category.id == data.category_id).first():
            raise HTTPException(status_code=404, detail="Category not found")

  
    p = Product(
    product_name=data.product_name,
    description=data.description,
    price=data.price,
    stock=data.stock,
    manufacturer_id=data.manufacturer_id,
    category_id=data.category_id
)

    
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

def get_product(prod_id: int, db: Session):
    p = db.query(Product).filter(Product.id == prod_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return p

def update_product(prod_id: int, data: ProductCreate, db: Session):
    p = db.query(Product).filter(Product.id == prod_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    p.name = data.name
    p.description = data.description
    p.price = data.price
    p.stock = data.stock
    p.manufacturer_id = data.manufacturer_id
    p.category_id = data.category_id
    db.commit()
    db.refresh(p)
    return p

def delete_product(prod_id: int, db: Session):
    p = db.query(Product).filter(Product.id == prod_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(p)
    db.commit()
    return {"msg": "Product deleted"}



def search(filters: ProductSearch, db: Session):
    query = db.query(Product)

    if filters.product_id:
        query = query.filter(Product.id == filters.product_id)

    if filters.product_name:
        query = query.filter(Product.product_name.ilike(f"%{filters.product_name}%"))

    return query.all()

from sqlalchemy import asc, desc
def by_order(order_by: str, order_type: str, db: Session):
    query = db.query(Product)

    if order_by == "name":
        if order_type == "asc":
            ordered = query.order_by(asc(Product.product_name))
        else:
            ordered = query.order_by(desc(Product.product_name))
    else:
        if order_type == "desc":
            ordered = query.order_by(desc(Product.id))
        else:
            ordered = query.order_by(asc(Product.id))

    return ordered.all()


