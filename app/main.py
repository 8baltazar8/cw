import os
import requests
import io
import random
import textwrap
# import asyncio
from fastapi import FastAPI, status, HTTPException, Depends, Request, File
from fastapi.params import Body
from fastapi.responses import Response, FileResponse
from PIL import Image, ImageDraw, ImageFont
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def image_to_byte_array(in_image) -> bytes:
    imgByteArr = io.BytesIO()
    in_image.save(imgByteArr, format="jpeg")
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


async def parse_body(request: Request):
    data: bytes = await request.body()
    return data

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/meme_gen", status_code=status.HTTP_201_CREATED, response_class=Response)
async def memegen(payload: bytes = Depends(parse_body), db: Session = Depends(get_db)):
    api_key = os.environ['IMAGGA_KEY']
    api_secret = os.environ['IMAGGA_SECRET']

    response = requests.post('https://api.imagga.com/v2/tags',
                             auth=(api_key, api_secret),
                             files={'image': payload})

    categories = schemas.Result.parse_obj(response.json()).result.tags
    memes = db.query(models.Meme.meme_text).filter(and_(models.Meme.category.in_(categories),
                                                        models.Meme.rating >= 0)).all()
    if not memes:
        to_send = Image.open('./app/lol.jpeg')
        to_send.show()
        return Response(content=image_to_byte_array(to_send), media_type="application/octet-stream")
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"There is no category")

    meme = random.choice(memes)[0].upper()


    image = Image.open(io.BytesIO(payload))
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    if image_width < image_height:
        font_size = int(image_width/8)
    else:
        font_size = int(image_height/8)

    myFont = ImageFont.truetype(font='Impact.ttf', size=font_size)

    char_width, char_height = myFont.getsize('A')
    chars_per_line = image_width//char_width
    lines = textwrap.wrap(meme, width=chars_per_line)

    y = 10
    for line in lines:
        line_width, line_height = myFont.getsize(line)
        x = (image_width-line_width)//2
        draw.text((x, y), line, fill='white', font=myFont)
        y += line_height

    image.show()

    return Response(content=image_to_byte_array(image), media_type="application/octet-stream")







@app.post("/post_meme", status_code=status.HTTP_201_CREATED)
async def meme_post(meme: schemas.Meme, db: Session = Depends(get_db)):
    new_meme = models.Meme(**meme.dict())
    db.add(new_meme)
    db.commit()
    db.refresh(new_meme)

    return {"msg": new_meme}


@app.get("/meme_by_category")
async def find(category: str, db: Session = Depends(get_db)):
    memes = db.query(models.Meme.meme_text).filter(models.Meme.category == category).all()
    if not memes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no memes in {category} category")
    return memes


@app.get("/test_sql")
async def test_sql(db: Session = Depends(get_db)):
    print("SOME")
    memes = db.query(models.Meme).all()
    return {"data": memes}
