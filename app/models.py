from pydantic import BaseModel, Field
from flask_login import UserMixin
from typing import List, Dict, Any


class ItemDetail(BaseModel):
    id: str = Field(..., example="252")


class Item(BaseModel):
    item: ItemDetail
    rate: float = Field(..., gt=0, example=100.0)
    quantity: int = Field(..., gt=0, example=10)


class ItemContainer(BaseModel):
    items: List[Item]


class Entity(BaseModel):
    id: str = Field(..., example="1341")


class Location(BaseModel):
    id: str = Field(..., examples="6")


class InvoiceData(BaseModel):
    entity: Entity
    location: Location
    item: ItemContainer


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
