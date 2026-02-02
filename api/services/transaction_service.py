from sqlalchemy.orm import Session
from models.transaction import Transaction
from schemas.transaction import TransactionCreate, TransactionUpdate


class TransactionService:

    @staticmethod
    def get_all(db: Session):
        return db.query(Transaction).all()

    @staticmethod
    def get_by_id(db: Session, id: int):
        return db.query(Transaction).filter(Transaction.id == id).first()

    @staticmethod
    def get_by_txid(db: Session, transaction_id: str):
        return db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()

    @staticmethod
    def create(db: Session, data: TransactionCreate) -> Transaction:
        db_obj = Transaction(
            transaction_id=data.transaction_id,
            amount=data.amount,
            sender=data.sender,
            receiver=data.receiver,
            raw=data.raw,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update(db: Session, db_obj: Transaction, patch: TransactionUpdate) -> Transaction:
        for field, value in patch.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def delete(db: Session, db_obj: Transaction):
        db.delete(db_obj)
        db.commit()
