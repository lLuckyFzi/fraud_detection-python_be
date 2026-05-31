from database import Base
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship

from enums import AlertStatus

class FraudAlert(Base):
    __tablename__ = "fraud_alerts"

    alert_id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(Integer, ForeignKey("transactions.transaction_id"), nullable=False)
    trigger_rule_name = Column(String(100), nullable=False)
    calculated_risk_score = Column(Integer, nullable=False)
    status = Column(Enum(AlertStatus), default=AlertStatus.Open)
    investigator_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relation
    transaction = relationship("Transaction", back_populates="alerts")