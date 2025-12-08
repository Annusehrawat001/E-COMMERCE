from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from schema.schema import CustomerCreate, VerifyOTP, LoginSchema, ResetPasswordSchema
from controller.user import (
    register_customer, verify_otp, login_user,
    send_reset_otp, reset_password
)

router = APIRouter()


@router.post("/register")
def register(data: CustomerCreate, db: Session = Depends(get_db)):
    return register_customer(data, db)


@router.post("/verify-otp")
def verify(data: VerifyOTP, db: Session = Depends(get_db)):
    return verify_otp(data, db)


@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    return login_user(data, db)


@router.post("/send-reset-otp")
def send_reset(email: str, db: Session = Depends(get_db)):
    return send_reset_otp(email, db)


@router.post("/reset-password")
def reset_pass(data: ResetPasswordSchema, db: Session = Depends(get_db)):
    return reset_password(data, db)



from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from schema.schema import CustomerCreate, VerifyOTP, LoginSchema, ResetPasswordSchema
from controller.user import (
    register_customer, verify_otp, login_user,
    send_reset_otp, reset_password
)

router = APIRouter()


@router.post("/register")
def register(data: CustomerCreate, db: Session = Depends(get_db)):
    return register_customer(data, db)


@router.post("/verify-otp")
def verify(data: VerifyOTP, db: Session = Depends(get_db)):
    return verify_otp(data, db)


@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    return login_user(data, db)


@router.post("/send-reset-otp")
def send_reset(email: str, db: Session = Depends(get_db)):
    return send_reset_otp(email, db)


@router.post("/reset-password")
def reset_pass(data: ResetPasswordSchema, db: Session = Depends(get_db)):
    return reset_password(data, db)



from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from schema.schema import ManufacturerCreate
from controller.user import (
    create_manufacturer, get_all_manufacturers, get_manufacturer,
    update_manufacturer, delete_manufacturer
)

router = APIRouter(prefix="/manufacturer", tags=["Manufacturer"])


@router.post("/dataposting")
def create(data: ManufacturerCreate, db: Session = Depends(get_db)):
    return create_manufacturer(data, db)


@router.get("/all")
def get_all(db: Session = Depends(get_db)):
    return get_all_manufacturers(db)


@router.get("/byid{man_id}")
def get_one(man_id: int, db: Session = Depends(get_db)):
    return get_manufacturer(man_id, db)


@router.put("/up{man_id}")
def update(man_id: int, data: ManufacturerCreate, db: Session = Depends(get_db)):
    return update_manufacturer(man_id, data, db)


@router.delete("/del{man_id}")
def delete(man_id: int, db: Session = Depends(get_db)):
    return delete_manufacturer(man_id, db)



from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from schema.schema import CategoryCreate
from controller.user import (
    create_category, get_all_categories, get_category,
    update_category, delete_category
)

router = APIRouter()


@router.post("/post")
def create(data: CategoryCreate, db: Session = Depends(get_db)):
    return create_category(data, db)


@router.get("/all")
def get_all(db: Session = Depends(get_db)):
    return get_all_categories(db)


@router.get("/get{cat_id}")
def get_one(cat_id: int, db: Session = Depends(get_db)):
    return get_category(cat_id, db)


@router.put("/put{cat_id}")
def update(cat_id: int, data: CategoryCreate, db: Session = Depends(get_db)):
    return update_category(cat_id, data, db)


@router.delete("/delete{cat_id}")
def delete(cat_id: int, db: Session = Depends(get_db)):
    return delete_category(cat_id, db)


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from schema.schema import ProductCreate
from controller.user import (
    create_product, get_product, update_product, delete_product
)

router = APIRouter()


@router.post("/create")
def create(data: ProductCreate, db: Session = Depends(get_db)):
    return create_product(data, db)


@router.get("/id{prod_id}")
def get_one(prod_id: int, db: Session = Depends(get_db)):
    return get_product(prod_id, db)


@router.put("/update{prod_id}")
def update(prod_id: int, data: ProductCreate, db: Session = Depends(get_db)):
    return update_product(prod_id, data, db)


@router.delete("/delete{prod_id}")
def delete(prod_id: int, db: Session = Depends(get_db)):
    return delete_product(prod_id, db)




