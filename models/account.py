from database import Base
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from enums import AccountType, AccountStatus

class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    account_number = Column(String(20), unique=True, nullable=False)
    balance = Column(Numeric(15, 2), default=0.00)
    account_type = Column(Enum(AccountType), nullable=False)
    daily_withdrawal_limit = Column(Numeric(15, 2))
    status = Column(Enum(AccountStatus), default=AccountStatus.Active)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relation
    owner = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")