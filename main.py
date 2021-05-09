from typing import Optional

from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: int
    is_offer: Optional[bool] = None

@app.get("/")
async def root():
    return {"message" : "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id" : item_id, "q" : q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_name": item.name, **item.dict()}
    if q:
        result.update({"q":q})
    return result