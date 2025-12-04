from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schema.schema import Login, Register
from model.users import Customer
from controller.user import get_db

# import login controller function
from controller.user import login_customer_controller

router = APIRouter()


# ------------ LOGIN CUSTOMER -------------
@router.post("/login")
def login_customer_route(data: Login, db: Session = Depends(get_db)):
    result = login_customer_controller(data, db)
    return result


# ------------ UPDATE USER -------------
@router.put("/update/{user_id}")
def update_user(user_id: int, data: Register, db: Session = Depends(get_db)):
    user = db.query(Customer).filter(Customer.id == user_id).first()

    if not user:
        raise HTTPException(404, "User not found")

    if db.query(Customer).filter(Customer.email == data.email, Customer.id != user_id).first():
        raise HTTPException(409, "Email already exists")

    if db.query(Customer).filter(Customer.phonenumber == data.phonenumber, Customer.id != user_id).first():
        raise HTTPException(409, "Phone already exists")

    user.customername = data.customername
    user.email = data.email
    user.phonenumber
    db.commit()
    db.refresh(user)

    return {"status": True, "msg": "User Updated", "data": user}


# ------------ DELETE USER -------------
@router.delete("/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Customer).filter(Customer.id == user_id).first()

    if not user:
        raise HTTPException(404, "User not found")

    db.delete(user)
    db.commit()

    return {"status": True, "msg": "User Deleted"}












from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schema.schema import Register, Login, UpdateProfile
from controller.user import (
    register_customer_controller,
    verify_otp_controller,
    login_customer_controller,
    update_profile_controller,
    
)

router = APIRouter(prefix="/customer")


@router.post("/register")
def register(data: Register, db: Session = Depends(get_db)):
    return register_customer_controller(data, db)


@router.post("/verify-otp")
def verify_otp(email: str, otp: str, db: Session = Depends(get_db)):
    return verify_otp_controller(email, otp, db)


@router.post("/login")
def login(data: Login, db: Session = Depends(get_db)):
    return login_customer_controller(data, db)


@router.put("/update/{user_id}")
def update_profile(user_id: int, data: UpdateProfile, db: Session = Depends(get_db)):
    return update_profile_controller(user_id, data, db)




















from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from schema.schema import Register, Login, VerifyOTP
from controller.user import (
    register_customer,
    verify_otp,
    login_customer
)

router = APIRouter(prefix="/customer")


@router.post("/register")
def register(data: Register, db: Session = Depends(get_db)):
    return register_customer(data, db)


@router.post("/verify-otp")
def verify(data: VerifyOTP, db: Session = Depends(get_db)):
    return verify_otp(data, db)


@router.post("/login")
def login(data: Login, db: Session = Depends(get_db)):
    return login_customer(data, db)
