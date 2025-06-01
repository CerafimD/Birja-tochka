from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from db import get_db
from models import UserDB, RoleEnum, Transaction
from schemas import NewUser, User
from utils import generate_api_key

router = APIRouter(prefix="/api/v1/public", tags=["auth"])

@router.post("/register", response_model=User)
def register_user(new_user: NewUser, db: Session = Depends(get_db)):
    user_id = str(uuid4())
    api_key = generate_api_key(16)

    # Проверка уникальности api_key
    while db.query(UserDB).filter(UserDB.api_key == api_key).first():
        api_key = generate_api_key(16)

    user_db = UserDB(
        id=user_id,
        name=new_user.name,
        role=RoleEnum.USER,
        api_key=api_key
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    return user_db
