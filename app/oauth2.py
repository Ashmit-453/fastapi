from jose import JWTError,jwt
from typing import Annotated
from . import schemas
from sqlalchemy.orm import Session
from . import database, models, schemas
from fastapi.security import OAuth2PasswordBearer
from fastapi import status,Response,HTTPException,Depends
from datetime import datetime,timedelta,timezone

outh2scheme=OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY="hello"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
def create_access_tokens(data:dict,expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_tokens(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id:int=payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data=schemas.Tokendata(user_id=user_id)
    except JWTError:
        raise credentials_exception
    return token_data 

def get_current_user(token:str=Depends(outh2scheme),db: Session = Depends(database.get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorised access",
                                       headers={"WWW-Authenticate":"Bearer"})
    token_data= verify_access_tokens(token,credentials_exception) 
    user = db.query(models.User).filter(models.User.id == token_data.user_id).first()
    return user 
      
    