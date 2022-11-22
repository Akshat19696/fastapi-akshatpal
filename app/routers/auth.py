from os import access
from fastapi import APIRouter,status,Depends,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from.. import models,utils,schemas,auth2
router = APIRouter()
@router.post("/login",response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"The User with email:{user_credentials.email} not found")
    if not utils.verify_password(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credentials")
    #create token
    #return token
    access_token= auth2.create_acess_token(data={"user_id":user.id})

    return{"access_token": access_token,"token_type":"bearer"}
