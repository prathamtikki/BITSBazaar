from database import Base
from sqlalchemy import Column, Integer, String,ForeignKey,LargeBinary
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__='category_info'
    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(40), index=True)
    parent_id = Column(Integer, ForeignKey('category_info.id'))

    # Establish the parent-child relationship between categories
    children = relationship("Category", back_populates="parent", remote_side=[id])
    parent = relationship("Category", back_populates="children")

class Products(Base):
    __tablename__='products_info'
    id=Column(Integer,primary_key=True,index=True)
    product_name=Column(String(20),unique=True)
    photo=Column(LargeBinary)
'''
class ProdMapping(Base):
    __tablename__='prod_mapping'
    id=Column(Integer,primary_key=True,index=True)
    category_id=relationship("Category",back_populates="category_info")
    prod_id=relationship("Products",back_populates="products_info")



class ProductsData(Base):
    __tablename__='products_data'
    id=Column(Integer,primary_key=True,index=True)
    cat_id=relationship("ProductsData",back_populates="product_data")
    image=Column(LargeBinary)
    price=Column(Integer)

class Sellers(Base):
    __tablename__ = 'sellers_info'
    id=Column(Integer,primary_key=True,index=True)
    firstname = Column(String(20),unique=True)
    lastname = Column(String(20),unique=True)
    contact=Column(Integer)
    username = Column(String(20), unique=True)
    hashed_password = Column(String(100))
    parent_id=relationship("Category",back_populates="category_info")




'''