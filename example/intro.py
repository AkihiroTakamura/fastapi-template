from fastapi import FastAPI, Query, Path, Body, HTTPException, BackgroundTasks
from typing import Optional, List, Set
from pydantic import BaseModel, HttpUrl, Field
from time import sleep
from datetime import datetime
from enum import Enum

app = FastAPI()


@app.get("/")
async def hello():
    return {"text": "hello world!"}


@app.get("/get/{id}")
async def path_parameter_example(
    id: int, name: Optional[str] = None, gender: List[str] = Query(None)
):
    return {"text": f"path parameter: {id} query parameter: {name} list: {gender}"}


class Gender(str, Enum):
    male = "male"
    female = "female"


@app.get("/enum/{gender}")
async def enum_parameter_example(gender: Gender):
    if gender == Gender.male:
        return {"text": "male set"}
    elif gender == Gender.female:
        return {"text": "female set"}
    else:
        return {"text": "unknown set"}


@app.get("/validation/{path}")
async def validation_example(
    string: str = Query(None, min_length=2, max_length=5, regex=r"[a-c]+."),
    integer: int = Query(..., gt=1, le=3),
    alias_query: str = Query(None, alias="default"),
    path: int = Path(None, le=10),
):
    return {
        "string": string,
        "integer": integer,
        "alias-query": alias_query,
        "path": path,
    }


class ExampleData(BaseModel):
    name: str
    age: Optional[int] = None
    emails: Optional[List[str]] = []


@app.post("/post")
async def receive_request_body(data: ExampleData):
    return {"text": f"name: {data.name} age: {data.age} emails: {data.emails}"}


@app.post("/post/embed")
async def receive_nested_request_body(
    data: ExampleData = Body(..., embed=True), data2: ExampleData = Body(..., embed=True)
):
    return {"text": f"name: {data.name} age: {data.age} emails: {data.emails}"}


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []
    images: Optional[List[Image]] = None


class Offer(BaseModel):
    name: str = Field(..., min_length=3, max_length=20)
    description: str = Field(None)
    price: float = Field(0, lt=99999)
    items: List[Item]


@app.post("/offers")
async def create_offer(offer: Offer):
    return offer


@app.get("/item", response_model=Item)
async def get_item():
    return {
        "name": "hoge",
        "description": "this is description",
        "price": 200,
        "images": [{"url": "http://hoge.com", "name": "image name"}],
    }


@app.get("/status", status_code=200)
async def response_status_example(integer: int):
    if integer > 400:
        # use HTTPException
        raise HTTPException(status_code=404, detail="this is error message")
    else:
        return {"text": "this is default message"}


def background_method(count: int):
    sleep(count)
    print(f"fired!! {datetime.utcnow()}")


@app.get("/background")
async def execute_background_task(count: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(background_method, count)
    return {"text": "background task executed"}
