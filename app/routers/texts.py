import os
import requests
import io
import random
import textwrap
# import asyncio

from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from fastapi.responses import Response, FileResponse
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from .. import models, schemas, utils
from ..database import engine, get_db
from ..settings import config

router = APIRouter(
    tags=['Meme texts']
)


@router.post("/post_meme", status_code=status.HTTP_201_CREATED, response_model=schemas.Post_Meme)
async def meme_post(meme: schemas.Meme, db: Session = Depends(get_db)):
    new_meme = models.Meme(**meme.dict())
    db.add(new_meme)
    db.commit()
    db.refresh(new_meme)
    return new_meme


@router.get("/meme_by_category", response_model=List[schemas.Post_Meme])
async def find(category: str, db: Session = Depends(get_db)):
    memes = db.query(models.Meme).filter(models.Meme.category == category).all()
    if not memes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no memes in {category} category")
    return memes


@router.get("/meme_by_id")
async def meme_by_id(id: int, db: Session = Depends(get_db)):
    memes = db.query(models.Meme).filter(models.Meme.id == id).first()
    if not memes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no meme with id {id}")
    return memes


@router.get("/test_sql")
async def test_sql(db: Session = Depends(get_db)):
    print("SOME")
    memes = db.query(models.Meme).all()
    return {"data": memes}


@router.put("/rate_meme")
async def rate_meme(id: int, user_rate: int, db: Session = Depends(get_db)):
    meme_query = db.query(models.Meme).filter(models.Meme.id == id)
    meme_inf = meme_query.first()
    rating, num_of_grades = meme_inf.rating, meme_inf.num_of_grades
    new_rating = int(((rating*num_of_grades)+user_rate)/(num_of_grades+1))
    meme_query.update({'rating': new_rating, 'num_of_grades': num_of_grades+1}, synchronize_session=False)
    db.commit()
    return new_rating
