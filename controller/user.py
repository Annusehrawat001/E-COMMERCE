import random
from fastapi import HTTPException
from sqlalchemy.orm import Session
from model.users import Customer
from schema.schema import Register, Login, VerifyOTP
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

SECRET_KEY = "MESSHO"
ALGORITHM = "HS256"

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="logintoken")

def create_token(data: dict):
    payload = {
        **data,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)


# ----------- REGISTER ------------
def register_customer(data: Register, db: Session):

    if db.query(Customer).filter(Customer.email == data.email).first():
        raise HTTPException(409, "Email already exists")

    if db.query(Customer).filter(Customer.phonenumber == data.phonenumber).first():
        raise HTTPException(409, "Phone number already exists")

    otp = str(random.randint(1000, 9999))

    new_user = Customer(
        customername=data.customername,
        email=data.email,
        phonenumber=data.phonenumber,
        otp=otp
    )

    db.add(new_user)
    db.commit()

    return {"msg": "OTP sent", "otp": otp}


# ----------- VERIFY OTP ----------
def verify_otp(data: VerifyOTP, db: Session):

    user = db.query(Customer).filter(Customer.email == data.email).first()

    if not user:
        raise HTTPException(404, "User not found")

    if user.otp != data.otp:
        raise HTTPException(400, "Incorrect OTP")

    user.is_verified = True
    user.otp = None
    db.commit()

    return {"msg": "OTP Verified"}


# ----------- LOGIN -----------
def login_customer(data: Login, db: Session):

    user = db.query(Customer).filter(Customer.email == data.email).first()

    if not user:
        raise HTTPException(404, "User not found")

    if not user.is_verified:
        raise HTTPException(403, "OTP not verified")

    token = create_token({"user_id": user.id})

    return {"msg": "Login Successful", "token": token}
