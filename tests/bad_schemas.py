from __future__ import annotations

from typing import List

from pydantic import BaseModel


class DetailItem(BaseModel):
    loc: List[str]
    msg: str
    type: str


class Model(BaseModel):
    detail: List[DetailItem]
