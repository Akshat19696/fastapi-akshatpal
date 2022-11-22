from typing import Optional
from pydantic import BaseModel,EmailStr
from pydantic.types import conint

class Userout(BaseModel):
    id:int
    email:EmailStr
    class Config:
        orm_mode= True

class Post(BaseModel): # for validation of data pydantic is imported
    title: str #if any value except the str is given in the title will return the error
    content: str #same for the contetnt also
    published : bool = True 
    owner_id:int
    owner:Userout
    
    class Config:
        orm_mode= True

class Postout(BaseModel):
    Post:Post
    votes:int
    class Config:
        orm_mode= True
class responsepost(BaseModel):
    title:str
    content:str
    
    class Config:
        orm_mode= True
class Usercreate(BaseModel):
    email:EmailStr
    password:str
class UserLogin(BaseModel):
    email:EmailStr
    password:str
class Userhashed(BaseModel):
    hash_password:str
    
class Token(BaseModel):
    access_token:str
    token_type:str
class TokenData(BaseModel):
    id:Optional[str]=None

class Vote(BaseModel):
    post_id:int
    dir: conint(le=1)


