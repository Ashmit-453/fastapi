
from ..database import get_db
from fastapi import Response,status,HTTPException,Depends,APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models,schemas,utils,oauth2
router=APIRouter(
    prefix="/users",
    tags=['users']
)
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Userout)
def create_user(u:schemas.Usercreate,db:Session=Depends(get_db)):
    hashed_password=utils.hash(u.password)
    u.password=hashed_password
    new_user=models.User(**u.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@router.get("/{id}",response_model=schemas.Userout,dependencies=[Depends(oauth2.get_current_user)])
def get_user(id:int,db:Session=Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user)):
    if id==current_user.id:
        user=db.query(models.User).filter(models.User.id==id).first()
        return user 
    
    else:
        credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorised access",
                                       headers={"WWW-Authenticate":"Bearer"})
        raise credentials_exception 