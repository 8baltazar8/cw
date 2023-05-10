import os
import requests
import io
import random
import textwrap
# import asyncio

from fastapi import FastAPI, status, HTTPException, Depends, Request, File, APIRouter
from fastapi.params import Body
from fastapi.responses import Response, FileResponse
from PIL import Image, ImageDraw, ImageFont
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from .. import models, schemas, utils
from ..database import engine, get_db
from ..settings import config

router = APIRouter(
    tags=['Media generation']
)

async def parse_body(request: Request):
    data: bytes = await request.body()
    return data

@router.post("/meme_gen", status_code=status.HTTP_201_CREATED, response_class=Response)
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
        to_send = Image.open('./app/routers/lol.jpeg')
        return Response(content=utils.image_to_byte_array(to_send),
                        media_type="application/octet-stream",
                        headers={"X-Meme-id": '666'})
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"There is no category")

    memeb = random.choice(memes)
    meme = memeb[0].upper()
    meme_id = str(memeb[1])

    pic_to_out = utils.pic_gen(payload=payload, meme=meme)

    header = {"X-Meme-id": meme_id}
    return Response(content=pic_to_out,
                    media_type="application/octet-stream",
                    headers=header)
