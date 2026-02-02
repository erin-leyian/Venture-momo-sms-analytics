from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TransactionBase(BaseModel):
    transaction_id: str
    amount: Optional[str] = None
    sender: Optional[str] = None
    receiver: Optional[str] = None
    raw: Optional[str] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    amount: Optional[str] = None
    sender: Optional[str] = None
    receiver: Optional[str] = None
    raw: Optional[str] = None


class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
