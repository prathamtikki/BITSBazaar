from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,DATE,LargeBinary

class Buyers(Base):
    __tablename__ = 'buyers_info'
    id=Column(Integer,primary_key=True,index=True)
    firstname = Column(String(20),unique=True)
    lastname = Column(String(20),unique=True)
    contact=Column(Integer)
    username = Column(String(20), unique=True)
    hashed_password = Column(String(100))

