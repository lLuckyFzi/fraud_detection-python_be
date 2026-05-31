from database import Base
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric

class MLFeature(Base):
    __tablename__ = "ml_features"

    feature_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False)
    avg_amount_30d = Column(Numeric(15, 2), default=0.00)
    tx_count_24h = Column(Integer, default=0)
    failed_tx_count_24h = Column(Integer, default=0)
    last_known_country = Column(String(3))
    last_updated = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))