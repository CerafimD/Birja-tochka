from sqlalchemy import Column, String, Enum, Integer, DateTime
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


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, index=True)  # UUID для уникальности транзакции
    ticker = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
