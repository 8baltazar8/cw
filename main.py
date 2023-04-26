from fastapi import FastAPI, status, HTTPException
import os
import requests
from fastapi.params import Body
from pydantic import BaseModel, ValidationError, validator
import re

app = FastAPI()

#GAVNO
class Suggest_Meme_test(BaseModel):
    category: str
    text: str

    @validator('category')
    def category_must_be_lowercasealpha(cls, category):
        assert re.match(r"^[a-zA-Z]+$", category), "Category should consist of lowercase letters, should be a word"
        return category.lower()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/meme")
def find():
    api_key = os.environ['IMAGGA_KEY']
    api_secret = os.environ['IMAGGA_SECRET']
    image_path = 'falcon.jpeg'
    response = requests.post(
        'https://api.imagga.com/v2/tags',
        auth=(api_key, api_secret),
        files={'image': open(image_path, 'rb')})
    # imagee = Image.open(image_path)
    return response.json()


@app.post("/memepost", status_code=status.HTTP_201_CREATED)
def memepost(payload: bytes = Body(...)):
    api_key = os.environ['IMAGGA_KEY']
    api_secret = os.environ['IMAGGA_SECRET']
    # image_path = 'falcon.jpeg'

    response = requests.post(
        'https://api.imagga.com/v2/tags',
        auth=(api_key, api_secret),
        files={'image': payload})
    # imagee = Image.open(image_path)
    return response.json()

@app.post("/testpost")
def test_post(test_model: Suggest_Meme_test):
    print(test_model)
    return test_model.dict()
