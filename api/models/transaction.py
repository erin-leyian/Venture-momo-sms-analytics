from sqlalchemy import Column, Integer, String, DateTime, Text
from config.database import Base
import datetime


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(100), unique=True, index=True, nullable=False)
    amount = Column(String(50), nullable=True)
    sender = Column(String(255), nullable=True)
    receiver = Column(String(255), nullable=True)
    raw = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
