from datetime import datetime, timedelta, timezone
from faker import Faker
from database import SessionLocal
from enums import RiskProfile, AccountType, TransactionType, TransactionStatus
from models.user import User
from models.account import Account
from models.merchant import Merchant
from models.transaction import Transaction

# use locale Indonesia
fake = Faker('id_ID')


def seed_data():
    db = SessionLocal()
    try:
        user_example = User(
            full_name="Budi Santoso",
            email="budi.santoso@example.com",
            phone_number=fake.phone_number(),
            risk_profile_level=RiskProfile.Low
        )

        db.add(user_example)
        db.commit()
        db.refresh(user_example)

        account_example = Account(
            user_id=user_example.user_id,
            account_number="100200300400",
            balance=50000000.00,
            account_type=AccountType.Savings
        )
        db.add(account_example)
        db.commit()
        db.refresh(account_example)

        merchant_bandung = Merchant(
            merchant_name="Kopi Kenangan Senja", 
            merchant_category_code="5814", # Makanan/Minuman
            city="Bandung", country_code="ID", risk_score=10
        )
        merchant_london = Merchant(
            merchant_name="Harrods Luxury Watches", 
            merchant_category_code="5094", # Perhiasan/Barang Mewah
            city="London", country_code="UK", risk_score=75
        )
        db.add_all([merchant_bandung, merchant_london])
        db.commit()
        db.refresh(merchant_bandung)
        db.refresh(merchant_london)

        # Impossible Travel Scenario
        date_now = datetime.now(timezone.utc)

        tx_bandung = Transaction(
            account_id=account_example.account_id,
            merchant_id=merchant_bandung.merchant_id,
            amount=45000.00, 
            transaction_type=TransactionType.Online_Purchase,
            channel="Mobile_Banking", ip_address="114.120.10.5",
            device_fingerprint="HASH_IPHONE_BUDI_123",
            latitude=-6.9147, longitude=107.6098,
            status=TransactionStatus.Success,
            timestamp=date_now - timedelta(minutes=15)
        )

        tx_london = Transaction(
            account_id=account_example.account_id,
            merchant_id=merchant_london.merchant_id,
            amount=25000000.00, 
            transaction_type=TransactionType.Online_Purchase,
            channel="Web_Portal", ip_address="82.163.20.1",
            device_fingerprint="HASH_UNKNOWN_PC_999",
            latitude=51.5074, longitude=-0.1278,
            status=TransactionStatus.Success, 
            timestamp=date_now - timedelta(minutes=5)
        )

        db.add_all([tx_bandung, tx_london])
        db.commit()
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()