
from fastapi import FastAPI,Depends
from typing import Annotated
from sqlalchemy.orm import Session
import models as models
from database import engine, SessionLocal
from models import Products
from routers import auth,books


app=FastAPI()

models.Base.metadata.create_all(bind=engine)

#app.include_router(auth.router)
app.include_router(books.router)
print(90)

