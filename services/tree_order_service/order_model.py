from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from fastapi import UploadFile


class OrderModel(BaseModel):
    id: int
    type_id: int
    user_id: int
    location_id: int
    progress_id: int
    donation_id: int
    created_at: datetime
    updated_at: datetime


class FullOrderModel(BaseModel):
    id: int
    type_id: int
    user_id: int
    location_id: int
    progress_id: int
    donation_id: int
    created_at: datetime
    updated_at: datetime


class CreateOrderModel(BaseModel):
    type_id: int
    user_id: int
    location_name: str
    longitude: Decimal
    latitude: Decimal
    donation_amount: Decimal


class UpdateOrderModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    planting_cost: Optional[Decimal]
    price: Optional[Decimal]
    image_url: Optional[UploadFile]
