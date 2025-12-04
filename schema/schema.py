from pydantic import BaseModel,EmailStr
from typing import Optional,List



class Register(BaseModel):
    customername:str
    email:EmailStr
    phonenumber:int


class Login(BaseModel):
    email:EmailStr

class OTP(BaseModel):
    email:EmailStr
    OTP:str

class Verifyotp(BaseModel):
    email:EmailStr
    otp:str




from pydantic import BaseModel, EmailStr

class Register(BaseModel):
    customername: str
    email: EmailStr
    phonenumber: str


class Login(BaseModel):
    email: EmailStr


class VerifyOTP(BaseModel):
    email: EmailStr
    otp: str
