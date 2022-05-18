from fastapi import APIRouter, Depends,status,HTTPException,Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schema,utils,database,models,Oauth2



router = APIRouter(tags=["Authentication"])


@router.post("/login",response_model=schema.Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(database.get_db)):
    user_met= db.query(models.User).filter(models.User.email == user_credential.username).first()
    if not user_met:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    if not utils.verifyHashedPaasword(user_credential.password,user_met.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")

    #create a token
    access_token = Oauth2.create_access_token({"user_id": user_met.id})
    
    return {"access_token":access_token,"token_type":"bearer"}