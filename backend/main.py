from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator

import functions

app = FastAPI(title="Lost and Found API")


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=1000)
    contact: str = Field(min_length=1, max_length=200)
    location: Optional[str] = Field(default=None, max_length=200)

    @field_validator("name", "description", "contact")
    @classmethod
    def strip_required_text(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Field must not be blank")
        return value

    @field_validator("location")
    @classmethod
    def strip_location(cls, value):
        if value is None:
            return None
        return value.strip() or None


@app.get("/items")
def items():
    return functions.get_all_items()


@app.get("/items/{item_id}")
def item(item_id: int):
    lost_item = functions.get_item(item_id)
    if lost_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    return lost_item


@app.post("/items", status_code=status.HTTP_201_CREATED)
def add_item(data: ItemCreate):
    return functions.add_lost_item(
        name=data.name,
        description=data.description,
        contact=data.contact,
        location=data.location,
    )
