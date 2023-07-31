from datetime import timedelta,datetime
from http.client import HTTPException
from typing import Annotated
from database import SessionLocal
from fastapi import FastAPI,APIRouter,Depends
from pydantic import BaseModel
#from models import Sellers
from passlib.context import CryptContext
from starlette import status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

SECRET_KEY='1110c181344a182392bbaa12bdb5b5fdf1c9fe7e7055bd6827596684ade405c6'
ALGO='HS256'

router=APIRouter(prefix='/auth',tags=['auth'])
bcrypt_contect=CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    username: str
    password: str
    contact : int  
    first_name : str
    last_name : str
    

class Token(BaseModel):
    token_type:str
    access_token:str


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

db_dependancy=Annotated[SessionLocal,Depends(get_db)]

def authenticate_user(username:str,password:str,db):
    user=db.query(Sellers).filter(Sellers.username==username).first()
    if not user:
        return False
    if not bcrypt_contect.verify(password,user.hashed_password):
        return False
    return user


def create_access_token(username: str , user_id : str , expires_delta: timedelta):
    encode={'sub':username,'id':user_id}
    expires=datetime.utcnow()+expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGO)

async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGO])
        username:str=payload.get('sub')
        user_id:int=payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORISED,
                                detail='could not validate')
        return {'username':username,'id':user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORISED,
                                detail='could not validate')
    
@router.post('/',status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependancy,
                      create_user_request: CreateUserRequest):
    create_user_model=Sellers(firstname=create_user_request.first_name,
                                lastname=create_user_request.last_name,
                                contact=create_user_request.contact,
                                username=create_user_request.username,
                                hashed_password=bcrypt_contect.hash(create_user_request.password))
    db.add(create_user_model)
    db.commit()

@router.post('/token',response_model=Token)
async def login(form_data:Annotated[OAuth2PasswordRequestForm  ,Depends()],
                db:db_dependancy):
    user=authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORISED,
                                detail='could not validate')
    token=create_access_token(user.username,user.id,timedelta(minutes=20))

    return {'access_token': token,'token_type':'bearer'}

@router.get('/allsellers')
async def get_all_sellers(db:db_dependancy,current_user:Annotated[dict,Depends(get_current_user)]):
    user=db.query(Sellers)
    return user.all()