from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Literal
from uuid import uuid4, UUID
import secrets
from sqlalchemy import create_engine, Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

import enum

# --- Настройка базы данных ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Для простоты используем SQLite

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# --- Enum для роли ---
class RoleEnum(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"

# --- Модель для БД ---
class UserDB(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)  # UUID храним как строку
    name = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER, nullable=False)
    api_key = Column(String, nullable=False, unique=True)

# --- Создаём таблицы ---
Base.metadata.create_all(bind=engine)

# --- Pydantic модели ---
class NewUser(BaseModel):
    name: str

class User(BaseModel):
    id: UUID
    name: str
    role: RoleEnum
    api_key: str

    class Config:
        orm_mode = True

# --- FastAPI приложение ---
app = FastAPI()

# --- Зависимость для получения сессии БД ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_api_key(length: int = 32) -> str:
    return secrets.token_hex(length)

@app.post("/api/v1/public/register", response_model=User)
def register_user(new_user: NewUser, db: Session = Depends(get_db)):
    # Генерируем UUID и API key
    user_id = str(uuid4())
    api_key = generate_api_key(16)

    user_db = UserDB(
        id=user_id,
        name=new_user.name,
        role=RoleEnum.USER,
        api_key=api_key
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)  # Чтобы получить обновлённый объект из БД

    return user_db
