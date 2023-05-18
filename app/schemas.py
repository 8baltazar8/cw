from pydantic import BaseModel, ValidationError, validator, Field
from typing import Optional, List, IO

import re


class Meme(BaseModel):
    meme_text: str
    category: str

    @validator('category')
    def category_must_be_lowercasealpha(cls, category):
        assert re.match(r"^[a-zA-Z]+$", category), "Category should consist of lowercase letters, should be a word"
        return category.lower()


class Post_Meme(Meme):
    id: int
    meme_text: str
    category: str

    class Config:
        orm_mode = True

class Meme_by_category(BaseModel):
    memes: List[Post_Meme]
# ________________________________


class Guesed_category(BaseModel):
    en: str


class Guess(BaseModel):
    confidence: float
    tag: Guesed_category


class Tags(BaseModel):
    tags: List[Guess]

    @validator('tags')
    def confidence_hun(cls, tags):
        out_list = []
        for tag in tags:
            if tag.confidence >= 70.0 and re.match(r"^[a-z]+$", tag.tag.en):
                out_list.append(tag.tag.en)
        return out_list


class Result(BaseModel):
    result: Tags


class Meme_generated(BaseModel):
    id: int
    content: bytes


class User_rate(BaseModel):
    id: int
    grade: int
