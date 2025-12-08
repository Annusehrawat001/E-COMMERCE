# from sqlalchemy import create_engine
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker, declarative_base,session
app=FastAPI()

# DATABASE_URL = "postgresql+psycopg2://postgres:8930@localhost/ecommerce"

# engine = create_engine(DATABASE_URL, echo=True)

# SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base = declarative_base()


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg2://postgres:8930@localhost/ecommerce"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


#dependncy to get db session

def get_db():
    db:session=SessionLocal()
    try:
        yield db
    finally:
        db.close()  

#create table 
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)



from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg2://postgres:8930@localhost/ecommerce"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
