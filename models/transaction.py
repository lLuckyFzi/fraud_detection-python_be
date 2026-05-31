from database import Base
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship

from enums import TransactionType, TransactionStatus

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False)
    merchant_id = Column(Integer, ForeignKey("merchants.merchant_id"), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    channel = Column(String(50)) # Mobile_Banking, ATM, Web_Portal
    ip_address = Column(String(45))
    device_fingerprint = Column(String(255))
    latitude = Column(Numeric(9, 6))
    longitude = Column(Numeric(9, 6))
    status = Column(Enum(TransactionStatus), default=TransactionStatus.Success)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))

    # Relation
    account = relationship("Account", back_populates="transactions")
    merchant = relationship("Merchant", back_populates="transactions")
    alerts = relationship("FraudAlert", back_populates="transaction")