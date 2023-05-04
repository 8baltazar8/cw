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
from .settings import config

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
    api_key = config.imagga_key.get_secret_value()
    api_secret = config.imagga_secret.get_secret_value()

    response = requests.post('https://api.imagga.com/v2/tags',
                             auth=(api_key, api_secret),
                             files={'image': payload})

    categories = schemas.Result.parse_obj(response.json()).result.tags
    memes = db.query(models.Meme.meme_text, models.Meme.id).filter(and_(models.Meme.category.in_(categories),
                                                                        models.Meme.rating >= 0)).all()
    if not memes:
        to_send = Image.open('./app/lol.jpeg')
        return Response(content=image_to_byte_array(to_send),
                         media_type="application/octet-stream")
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"There is no category")

    memeb = random.choice(memes)
    meme = memeb[0].upper()
    meme_id = str(memeb[1])


    image = Image.open(io.BytesIO(payload))
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    if image_width < image_height:
        font_size = int(image_width/10)
    else:
        font_size = int(image_height/10)

    myFont = ImageFont.truetype(font='Impact.ttf', size=font_size)

    char_width, char_height = myFont.getsize('A')
    chars_per_line = image_width//char_width
    lines = textwrap.wrap(meme, width=chars_per_line)
    if len(lines) == 1:
        line_width, line_height = myFont.getsize(lines[0])
        y = image_height - line_height - 10
        x = (image_width-line_width)//2
        draw.text((x, y), lines[0], fill='white', font=myFont)
    else:
        y = 10
        line_width, line_height = myFont.getsize(lines[0])
        x = (image_width-line_width)//2
        draw.text((x, y), lines[0], fill='white', font=myFont)
        y = image_height - (len(lines)-1) * char_height - 10
        for line in lines[1:]:
            line_width, line_height = myFont.getsize(line)
            x = (image_width-line_width)//2
            draw.text((x, y), line, fill='white', font=myFont)
            y += line_height

    image.show()
    header = {"X-Meme-id": meme_id}
    return Response(content=image_to_byte_array(image),
                    media_type="application/octet-stream",
                    headers=header)







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


@app.get("/meme_by_id")
async def meme_by_id(id: int, db: Session = Depends(get_db)):
    memes = db.query(models.Meme).filter(models.Meme.id == id).first()
    if not memes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no meme with id {id}")
    return memes

@app.get("/test_sql")
async def test_sql(db: Session = Depends(get_db)):
    print("SOME")
    memes = db.query(models.Meme).all()
    return {"data": memes}


@app.put("/rate_meme")
async def rate_meme(id: int, user_rate: int, db: Session = Depends(get_db)):
    meme_query = db.query(models.Meme).filter(models.Meme.id == id)
    meme_inf = meme_query.first()
    rating, num_of_grades = meme_inf.rating, meme_inf.num_of_grades
    new_rating = int(((rating*num_of_grades)+user_rate)/(num_of_grades+1))
    meme_query.update({'rating': new_rating, 'num_of_grades': num_of_grades+1}, synchronize_session=False)
    db.commit()
    return new_rating
