from pydantic import BaseModel,EmailStr
from typing import Optional
class Post(BaseModel):
    title: str
    content: str
    published:bool=True 
class Createpost(Post):
    pass
class basepost(Post):
    id:int 
    class Config:
        from_attributes=True

class Usercreate(BaseModel):
    email: EmailStr
    password:str
class Userout(BaseModel):
    id:int
    email:EmailStr
    class config:
        from_attributes=True 

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str 
    token_type:str
class Tokendata(BaseModel):
    user_id:Optional[int]=None

