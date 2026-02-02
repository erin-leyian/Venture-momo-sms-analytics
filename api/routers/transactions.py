from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from config.database import get_db
from schemas.transaction import (
    TransactionResponse,
    TransactionCreate,
    TransactionUpdate,
)
from services.transaction_service import TransactionService

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/", response_model=List[TransactionResponse])
async def list_transactions(db: Session = Depends(get_db)):
    """GET /transactions - list all"""
    return TransactionService.get_all(db)


@router.get("/{id}", response_model=TransactionResponse)
async def get_transaction(id: int, db: Session = Depends(get_db)):
    """GET /transactions/{id} - get single transaction by DB id"""
    tx = TransactionService.get_by_id(db, id)
    if not tx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return tx


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(payload: TransactionCreate, db: Session = Depends(get_db)):
    """POST /transactions - create new transaction"""
    if TransactionService.get_by_txid(db, payload.transaction_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Transaction already exists")
    tx = TransactionService.create(db, payload)
    return tx


@router.put("/{id}", response_model=TransactionResponse)
async def update_transaction(id: int, payload: TransactionUpdate, db: Session = Depends(get_db)):
    """PUT /transactions/{id} - update transaction"""
    tx = TransactionService.get_by_id(db, id)
    if not tx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    tx = TransactionService.update(db, tx, payload)
    return tx


@router.delete("/{id}")
async def delete_transaction(id: int, db: Session = Depends(get_db)):
    """DELETE /transactions/{id} - delete transaction"""
    tx = TransactionService.get_by_id(db, id)
    if not tx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    TransactionService.delete(db, tx)
    return {"message": f"Deleted {id}"}
