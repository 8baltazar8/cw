from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.params import Body
from PIL import Image, ImageDraw, ImageFont
from psycopg2.extras import RealDictCursor
import os
import requests
import io
import psycopg2
import time
# import asyncio
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/meme_gen", status_code=status.HTTP_201_CREATED)
async def memegen(payload: bytes = Body(...)):
    api_key = os.environ['IMAGGA_KEY']
    api_secret = os.environ['IMAGGA_SECRET']
    response = requests.post('https://api.imagga.com/v2/tags',
                             auth=(api_key, api_secret),
                             files={'image': payload})

    image = Image.open(io.BytesIO(payload))
    #image.show()
    text = response.json()["result"]["tags"][0]["tag"]['en']
    font_size = int(image.size[1]/8)
    I1 = ImageDraw.Draw(image)
    myFont = ImageFont.truetype('Arial.ttf', font_size)
    I1.text((int(image.size[1]/2), 10), f"{image.size}", font=myFont, fill=(255, 255, 255))
    I1.text((int(image.size[1]/2), int(image.size[1])-font_size-10), f"{text}", font=myFont, fill=(255, 255, 255))
    image.show()


    # imagee = Image.open(image_path)
    return response.json()

@app.post("/post_meme", status_code=status.HTTP_201_CREATED)
async def meme_post(meme: schemas.Meme, db: Session = Depends(get_db)):
    new_meme = models.Meme(**meme.dict())
    db.add(new_meme)
    db.commit()
    db.refresh(new_meme)
    return {"msg": new_meme}


@app.get("/meme_by_category")
async def find(category: str, db: Session = Depends(get_db)):
    memes = db.query(models.Meme).filter(models.Meme.category == category).all()
    if not memes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no memes in {category} category")
    return memes


@app.get("/test_sql")
async def test_sql(db: Session = Depends(get_db)):
    print("SOME")
    memes = db.query(models.Meme).all()
    return {"data": memes}
