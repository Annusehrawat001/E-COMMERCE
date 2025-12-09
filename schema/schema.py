from pydantic import BaseModel, EmailStr
from typing import Optional, List

# ------------------ Customer ------------------
class CustomerCreate(BaseModel):
    customername: str
    email: EmailStr
    phonenumber: str
    password: str
    city: str
    state:str
    pincode: int

class CustomerResponse(BaseModel):
    id: int
    customername: str
    email: EmailStr
    phonenumber: str
    city: Optional[str]
    state: Optional[str]
    pincode: Optional[int]

    class Config:
        from_attributes = True

class VerifyOTP(BaseModel):
    email: EmailStr
    otp: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class ResetPasswordSchema(BaseModel):
    email: EmailStr
    otp: int
    new_password: str

# ------------------ Manufacturer ------------------
class ManufacturerCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    country: Optional[str] = None

class ManufacturerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    country: str

    class Config:
        from_attributes = True

# ------------------ Category ------------------
class CategoryCreate(BaseModel):
    name: str
    description: str 

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True

# ------------------ Product ------------------
class ProductCreate(BaseModel):
    name: str
    description:str
    price: int
    stock: int 
    manufacturer_id: int 
    category_id: int

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: int
    stock: int
    manufacturer_id: str
    category_id: str

    class Config:
        from_attributes = True


class ProductSearch(BaseModel):
    product_id: Optional[int] = None
    product_name: Optional[str] = None

# ------------------ Order ------------------
class OrderCreate(BaseModel):
    customer_id: int
    total_amount: int

class OrderResponse(BaseModel):
    id: int
    customer_id: int
    total_amount: int
    status: str

    class Config:
        from_attributes = True

class ProductSearch(BaseModel):
    product_id: Optional[int] = None
    product_name: Optional[str] = None
