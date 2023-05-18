from .database import Base
from sqlalchemy import Column, Integer, Text, String, Float
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Meme(Base):
    __tablename__ = "memes"
    id = Column(Integer, primary_key=True, nullable=False)
    meme_text = Column(Text, nullable=False)
    category = Column(String, nullable=False)
    rating = Column(Float, server_default='1')
    num_of_grades = Column(Integer, server_default='1')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
