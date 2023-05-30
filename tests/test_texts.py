import pytest
import pydantic
from app import schemas
from . import bad_schemas


@pytest.mark.parametrize("meme_text, category", [
    ("lol", "bar"),
    ("FOO", "foo"),
    ("lo9934234", "bar")])
def test_meme_post(client, meme_text, category):
    res = client.post('/post_meme', json={'meme_text': meme_text, "category": category})
    js = schemas.Post_Meme(**res.json())
    assert js.meme_text == meme_text
    assert js.category == category
    assert isinstance(js.id, int)
    assert res.status_code == 201


@pytest.mark.parametrize("meme_text, category", [
    ("lol", "211212"),
    ("FOO", "foo ggg"),
    ("lo9934234", "bar2"),
    ("000", '')])
def test_wrong_category(client, meme_text, category):
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        res = client.post('/post_meme', json={"meme_text": meme_text, "category": category})
        res = schemas.Post_Meme(**res.json())


def test_random_meme_404(client):
    res = client.get('/random_meme')
    assert res.status_code == 404


def test_random_meme(client):
    client.post('/post_meme', json={"meme_text": "foo", "category": "bar"})
    res = client.get('/random_meme')
    resj = schemas.Random_meme(**res.json())
    assert isinstance(resj.meme_text, str)
    assert res.status_code == 200


def test_wrong_rate(client):
    res = client.put('/rate_meme', json={"id": 1, "grade": 1})
    assert res.status_code == 404


@pytest.mark.parametrize("grade", [
    ("12312"),
    ("-1212"),
    ("0"),
    (""),
    ("qweqw")])
def test_bad_rate(client, grade):
    client.post('/post_meme', json={"meme_text": "meme_text", "category": "category"})
    res = client.put('/rate_meme', json={"id": 1, "grade": grade})
    resj = bad_schemas.Model(**res.json())
    assert resj.detail[0].msg == 'value is not a valid integer' or resj.detail[0].msg == "Grade should be from 1 to 10"
