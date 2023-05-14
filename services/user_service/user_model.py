from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from decimal import Decimal


class Role(str, Enum):
    user = "User"
    admin = "Admin"


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
    role: Optional[Role]


class UpdateUserModel(BaseModel):
    name: Optional[str]
    password: Optional[str]
    phone: Optional[str]


class RewardModel(BaseModel):
    id: int
    name: str
    description: str
    points: Decimal
