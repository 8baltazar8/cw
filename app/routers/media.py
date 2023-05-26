import requests
import random
import base64
from fastapi import status, Depends, Request, APIRouter
from PIL import Image
from sqlalchemy.orm import Session
from sqlalchemy import and_
from .. import models, schemas, utils
from ..database import get_db
from ..settings import config

router = APIRouter(
    tags=['Media generation']
)


async def parse_body(request: Request):
    data: bytes = await request.body()
    return data


@router.post("/meme_gen", status_code=status.HTTP_201_CREATED, response_model=schemas.Meme_generated)
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
        fin = {'id': '404',
               'content': base64.b64encode(utils.image_to_byte_array(to_send)).decode('utf-8'),
               'categories': categories}
        return fin
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"There is no category")

    memeb = random.choice(memes)
    meme = memeb[0].upper()
    meme_id = str(memeb[1])

    fin = {'id': meme_id,
           'content': base64.b64encode(utils.pic_gen(payload=payload, meme=meme)).decode('utf-8'),
           'categories': categories}

    return fin


@router.post("/dem_gen", status_code=status.HTTP_201_CREATED, response_model=schemas.Dem_generated)
async def demegen(user_data: schemas.Dem_in, db: Session = Depends(get_db)):
    fin = {'content': base64.b64encode(utils.dem_gen(payload=base64.b64decode(user_data.payload), meme_text=user_data.text)).decode('utf-8')}
    return fin
# base64.b64decode(user_data.payload)
