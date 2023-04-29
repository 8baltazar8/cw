from pydantic import BaseModel, ValidationError, validator
import re


class Meme(BaseModel):
    meme_text: str
    category: str

    @validator('category')
    def category_must_be_lowercasealpha(cls, category):
        assert re.match(r"^[a-zA-Z]+$", category), "Category should consist of lowercase letters, should be a word"
        return category.lower()
