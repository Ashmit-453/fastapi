
from ..database import get_db
from fastapi import Response,status,HTTPException,Depends,APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models,schemas,utils,oauth2
router=APIRouter(
    prefix="/posts",
    tags=['posts']
)
@router.get("/",response_model=List[schemas.basepost])
def get_posts(db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    posts=db.query(models.Post).all()
    return posts

@router.post("/createposts")
def create_posts(post: schemas.Createpost,db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
    #                (post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    new_post=models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
@router.get("/{id}",response_model=schemas.basepost)
def get_post(id:int,db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id=%s """,(str(id),))
    # post=cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id==id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    return post 
@router.delete("/{id}")
def delete_post(id:int,db:Session=Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id=%s RETURNING *""",(str(id),))
    # ans=cursor.fetchone()
    # conn.commit()
    ans=db.query(models.Post).filter(models.Post.id==id).first()
    if ans==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} not exist")
    db.delete(ans)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
@router.put("/{id}",response_model=schemas.basepost)
def update_post(id:int,post:schemas.basepost,db:Session=Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,str(id)))
    # upost=cursor.fetchone()
    # conn.commit()
    upost=db.query(models.Post).filter(models.Post.id==id).first()
    if upost==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} not exist")
    upost.title=post.title
    upost.content=post.content
    upost.published=post.published
    db.commit()
    db.refresh(upost)
    return upost