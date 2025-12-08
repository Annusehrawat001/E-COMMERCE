from fastapi import FastAPI,APIRouter
from database.db import Base, engine
from routes.userroutes import router as user_router
from routes.userroutes import router as manufacturer_router
from routes.userroutes import router as category_router
from routes.userroutes import router as product_router
from routes.userroutes import  router as customer_router


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(manufacturer_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(customer_router)