from fastapi import FastAPI
from . import models
from .database import engine
from .routers import media, texts

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(media.router)
app.include_router(texts.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
