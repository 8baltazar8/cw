import pytest
import pydantic
from app import schemas, utils
from . import bad_schemas
import base64


@pytest.fixture
def get_pic_b():
    with open("tests/t_pic.jpeg", 'rb') as pic:
        return base64.b64encode(pic.read()).decode('utf-8')


# def test_meme_gen(client, get_pic_b):
#     res = client.post('/meme_gen', data=schemas.Meme_in(payload=get_pic_b).json())
#     js = schemas.Meme_generated(**res.json())
#     assert isinstance(js.id, int)
#     assert isinstance(js.content, bytes)
#     assert isinstance(js.categories, list)


@pytest.mark.parametrize("text", [
    ("lfweff"),
    ("fwfwf"),
    ("AJSJ AJdJWjd"),
    ("2312")])
def test_dem_gen(client, get_pic_b, text):
    res = client.post('/dem_gen', data=schemas.Dem_in(text=text, payload=get_pic_b).json())
    js = schemas.Dem_generated(**res.json())
    assert isinstance(js.content, bytes)
