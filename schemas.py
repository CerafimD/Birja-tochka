from pydantic import BaseModel
from typing import Literal
from uuid import UUID
import enum

class RoleEnum(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class NewUser(BaseModel):
    name: str

class User(BaseModel):
    id: UUID
    name: str
    role: RoleEnum
    api_key: str

    class Config:
        orm_mode = True
