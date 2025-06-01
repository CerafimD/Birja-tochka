from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from db import get_db
from models import Transaction as TransactionDB
from schemas import Transaction

router = APIRouter(prefix="/api/v1/public", tags=["public"])


@router.get("/transactions/{ticker}", response_model=List[Transaction])
def get_transaction_history(
        ticker: str,
        limit: int = Query(10, le=100, description="Максимальное число записей"),
        db: Session = Depends(get_db)
):
    transactions = (
        db.query(TransactionDB)
        .filter(TransactionDB.ticker == ticker)
        .order_by(TransactionDB.timestamp.desc())
        .limit(limit)
        .all()
    )

    if not transactions:
        # Можно вернуть пустой список или 404, в зависимости от логики
        return []

    return transactions
