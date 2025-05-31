from sqlalchemy import Column, String, Enum
from db import Base
import enum

class RoleEnum(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class UserDB(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)  # UUID как строка
    name = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER, nullable=False)
    api_key = Column(String, nullable=False, unique=True)
