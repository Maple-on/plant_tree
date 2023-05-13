from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class UserModel(BaseModel):
    id: int
    name: str
    email: str
    password: str
    phone: str
    reward_id: int
    created_at: datetime
    updated_at: datetime


class CreateUserModel(BaseModel):
    name: str
    email: str
    password: str
    phone: str


class UpdateUserModel(BaseModel):
    name: Optional[str]
    password: Optional[str]
    phone: Optional[str]
