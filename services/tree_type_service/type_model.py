from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from fastapi import UploadFile

class TypeModel(BaseModel):
    id: int
    name: str
    description: str
    planting_cost: Decimal
    price: Decimal
    image_url: str
    created_at: datetime
    updated_at: datetime


class CreateTypeModel(BaseModel):
    name: str
    description: str
    planting_cost: Decimal
    price: Decimal


class UpdateTypeModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    planting_cost: Optional[Decimal]
    price: Optional[Decimal]
    image_url: Optional[UploadFile]
