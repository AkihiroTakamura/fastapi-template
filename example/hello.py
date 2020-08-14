from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()


@app.get("/")
async def hello():
    return {"text": "hello world"}


class ExampleData(BaseModel):
    name: str
    age: Optional[int] = None
    emails: List[str]


@app.post("/post")
async def create_example_data(data: ExampleData):
    return {"text": f"hello, {data.name}, {data.age}, {data.emails}"}
