from fastapi import *
from pydantic import BaseModel
from typing import Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models,schemas,utils,oauth2
from sqlalchemy.orm import Session
from .database import engine,SessionLocal
from .routers import post,user,auth
models.Base.metadata.create_all(bind=engine)
app = FastAPI()
            
while True:
    try:
        conn=psycopg2.connect(host='localhost',database='data',user='postgres',password='453',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connected successfully")
        break 
    except Exception as error:
        print("Connection failed")
        print('error:',error)    

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)