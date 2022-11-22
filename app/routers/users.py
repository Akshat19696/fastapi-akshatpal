from .. import models,schemas,utils
from typing import List
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi    import FastAPI , status , HTTPException,Depends,APIRouter
router=APIRouter()#you can use prefix="/kuchbhi"inside the parenthesis of Apirouter

@router.post("/users",status_code = status.HTTP_201_CREATED,response_model=schemas.Userout)
def create_user(user:schemas.Usercreate,db: Session = Depends(get_db)):
    #hash the password-User.password
    #hash_password=pwd_context.hash(user.password)
    schemas.Userhashed.hash_password=utils.hash(user.password)
    user.password= schemas.Userhashed.hash_password
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/user/{id}",status_code=status.HTTP_302_FOUND,response_model=List[schemas.Userout])
def get_user(id:int,db: Session = Depends(get_db)):
    user_details=db.query(models.User).filter(models.User.id==id).all()
    if not user_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The post with id:{id} not found")
    else:
        return user_details

@router.get("/allusers",status_code=status.HTTP_302_FOUND,response_model=List[schemas.Userout])
def get_users(db: Session = Depends(get_db)):
    users=db.query(models.User).all()
    return users