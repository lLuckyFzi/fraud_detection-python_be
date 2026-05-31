from database import Base
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

class Merchant(Base):
    __tablename__ = "merchants"

    merchant_id = Column(Integer, primary_key=True, autoincrement=True)
    merchant_name = Column(String(100), nullable=False)
    merchant_category_code = Column(String(4), nullable=False) # MCC Code
    risk_score = Column(Integer, default=10) # 1 - 100
    city = Column(String(50))
    country_code = Column(String(3))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relation
    transactions = relationship("Transaction", back_populates="merchant")