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
from typing import List
from . import models, schemas, utils
from .database import engine, get_db
from .settings import config
from .routers import media, texts

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(media.router)
app.include_router(texts.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
