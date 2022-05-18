from typing import List
from requests import Session
from .. import models,schema,utils
from fastapi import Depends,status,HTTPException,Response,APIRouter
from ..database import  get_db
from pydantic import EmailStr
from sqlalchemy.orm import Session

router = APIRouter(
    
    prefix="/users",
    tags=["Users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.ResponseOnUserCreate)
def create_user(user: schema.UserCreate,db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.email == user.email).first()
    if query:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"User with {user.email} already exist")
    #hash the paasword
    user.password = utils.hash(user.password)    
    user_created=models.User(**user.dict())
    db.add(user_created)
    db.commit()
    db.refresh(user_created)
    return user_created
    


@router.get("/by_mail/{email}",response_model=schema.ResponseOnUserCreate)
def get_user_by_email(email :EmailStr,db:Session = Depends(get_db)):
        user_met = db.query(models.User).filter(models.User.email == email).first()
        if not user_met:    
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
        return user_met
    
    
        
@router.get("/{id}",response_model=schema.ResponseOnUserCreate)
def get_user(id:int,db:Session = Depends(get_db)):
    user_met = db.query(models.User).filter(models.User.id == id).first()
    if not user_met:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return user_met

   