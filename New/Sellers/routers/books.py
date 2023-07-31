from fastapi import FastAPI,Depends,APIRouter,UploadFile,File,Form
from database import SessionLocal
from typing import Annotated
from models import Category,Products
from pydantic import BaseModel
from io import BytesIO
from PIL import Image
from fastapi.responses import FileResponse
from enum import Enum


router=APIRouter(prefix='/books',tags=['books'])

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

db_dependancy=Annotated[SessionLocal,Depends(get_db)]

class AddBook(BaseModel):
    bookname:str
    edition:int
    condition:str
    owner_id:int
    price:int
    photo: bytes

class AddCategory(BaseModel):
    category_name:str
    parent_id:int=None


    

# everyhting related to CATEGORY
@router.post('/add_catergory')
async def add_catergory(db:db_dependancy,add_category:AddCategory):
    # Create a new category with the provided name and parent_id
    new_category = Category(category_name=add_category.category_name, parent_id=add_category.parent_id)
    # Add the new category to the session and commit changes
    db.add(new_category)
    db.commit()
    return new_category


@router.get('/get_catergory')
async def get_catergory(db:db_dependancy):
    catergory=db.query(Category).all()
    return catergory

# adding only products
@router.post('/add_products')
async def add_products(db:db_dependancy,add_product:str,image: UploadFile = File(...)):
    image_data = await image.read()
    data = Products(photo=image_data,product_name=add_product)
    db.add(data)
    db.commit()
    return {"success"}

@router.get('/get_products')
async def get_products(db:db_dependancy):
    products=db.query(Products).all()
    photo=products[0].photo
    image = Image.open(BytesIO(photo))
    image.save('retrieved_image.jpg')
    return FileResponse('retrieved_image.jpg', media_type='image/jpeg')

''''
@router.get('/get_books')
async def books_info(db:db_dependancy):
    books=db.query(Books).all()
    bookphoto=books[1].photo
    image = Image.open(BytesIO(bookphoto))
    image.save('retrieved_image.jpg')
    return FileResponse('retrieved_image.jpg', media_type='image/jpeg')

@router.post('/add_image')
async def add_image(db:db_dependancy,file: UploadFile = File(...)):
    return {"filename": file.filename}

@router.post('/add_books')
async def add_books(db:db_dependancy,add_book:AddBook,file: UploadFile = File(...)):
    contents = await file.read()
    data = AddBook(photo=contents)
    value=data.photo
    db.add(Books(bookname=add_book.bookname,
                 edition=add_book.edition,
                 condition=add_book.condition,
                 owner_id=add_book.owner_id,
                 price=add_book.price,
                 photo=value))
    db.commit()
    return {'Book add is successful'}


'''