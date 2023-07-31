
from fastapi import FastAPI,Depends
from typing import Annotated
from sqlalchemy.orm import Session
import models as models
from database import engine, SessionLocal
from models import Buyers
from routes import auth


app=FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
print(90)

