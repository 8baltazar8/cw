from fastapi import FastAPI, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel, ValidationError, validator
from PIL import Image, ImageDraw, ImageFont
from psycopg2.extras import RealDictCursor
import os
import requests
import re
import io
import psycopg2
import time

app = FastAPI()

db_host = os.environ['DB_HOST']
db_name = os.environ['DB_NAME']
db_user = os.environ['DB_USER']
db_pass = os.environ['DB_PASS']

while True:
    try:
        conn = psycopg2.connect(host=db_host, database=db_name,
                                user=db_user, password=db_pass,
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB CONNECCTION SUCCEED")
        break
    except Exception as e:
        print(e)
        time.sleep(3)

#GAVNO
class Suggest_Meme_test(BaseModel):
    text: str
    category: str

    @validator('category')
    def category_must_be_lowercasealpha(cls, category):
        assert re.match(r"^[a-zA-Z]+$", category), "Category should consist of lowercase letters, should be a word"
        return category.lower()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/meme_gen", status_code=status.HTTP_201_CREATED)
def memegen(payload: bytes = Body(...)):
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
def meme_post(meme: Suggest_Meme_test):
    cursor.execute("INSERT INTO texts (category, text) VALUES (%s, %s) RETURNING *",
                   (meme.category, meme.text))
    meme_resp = cursor.fetchone()
    conn.commit()
    return meme_resp

@app.get("/meme_by_category")
def find(category: str):
    print("SOME")
    cursor.execute("SELECT * FROM texts WHERE category = %s", (category,))
    memes = cursor.fetchall()
    if not memes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no memes in {category} category")
    return memes
