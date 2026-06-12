import random
from datetime import datetime, timedelta, timezone
from faker import Faker
from database import SessionLocal
from enums import RiskProfile, AccountType, TransactionType, TransactionStatus
from models.user import User
from models.account import Account
from models.merchant import Merchant
from models.transaction import Transaction

fake = Faker('id_ID')

def seed_data():
    db = SessionLocal()
    try:
        user_example = User(
            full_name="Budi Santoso", email="budi.santoso@example.com",
            phone_number=fake.phone_number(), risk_profile_level=RiskProfile.Low
        )
        db.add(user_example)
        db.commit()
        db.refresh(user_example)

        account_example = Account(
            user_id=user_example.user_id, account_number="100200300400",
            balance=50000000.00, account_type=AccountType.Savings
        )
        db.add(account_example)
        db.commit()
        db.refresh(account_example)

        merchants_normal = [
            Merchant(merchant_name="Kopi Kenangan Senja", merchant_category_code="5814", city="Bandung", country_code="ID", risk_score=10),
            Merchant(merchant_name="Borma Supermarket", merchant_category_code="5411", city="Bandung", country_code="ID", risk_score=5),
            Merchant(merchant_name="SPBU Pertamina Pasteur", merchant_category_code="5541", city="Bandung", country_code="ID", risk_score=5),
            Merchant(merchant_name="Rumah Makan Sunda", merchant_category_code="5812", city="Cimahi", country_code="ID", risk_score=15)
        ]
        db.add_all(merchants_normal)
        
        merchant_london = Merchant(merchant_name="Harrods Luxury Watches", merchant_category_code="5094", city="London", country_code="UK", risk_score=75)
        db.add(merchant_london)
        db.commit()
        
        for m in merchants_normal: db.refresh(m)
        db.refresh(merchant_london)

        date_now = datetime.now(timezone.utc)
        normal_transactions = []
        
        for i in range(50):
            random_days_ago = random.randint(1, 30)
            random_hours_ago = random.randint(1, 23)
            tx_time = date_now - timedelta(days=random_days_ago, hours=random_hours_ago)
            
            random_amount = float(random.randint(15, 300) * 1000)
            random_merchant = random.choice(merchants_normal)

            tx = Transaction(
                account_id=account_example.account_id,
                merchant_id=random_merchant.merchant_id,
                amount=random_amount,
                transaction_type=TransactionType.Online_Purchase,
                channel="Mobile_Banking", ip_address=fake.ipv4(),
                device_fingerprint="HASH_IPHONE_BUDI_123",
                latitude=float(fake.coordinate(center=-6.9147, radius=0.1)),
                longitude=float(fake.coordinate(center=107.6098, radius=0.1)),
                status=TransactionStatus.Success,
                timestamp=tx_time
            )
            normal_transactions.append(tx)
            
        db.add_all(normal_transactions)
        db.commit()

        tx_bandung = Transaction(
            account_id=account_example.account_id, merchant_id=merchants_normal[0].merchant_id,
            amount=45000.00, transaction_type=TransactionType.Online_Purchase, channel="Mobile_Banking", 
            ip_address="114.120.10.5", device_fingerprint="HASH_IPHONE_BUDI_123",
            latitude=-6.9147, longitude=107.6098, status=TransactionStatus.Success,
            timestamp=date_now - timedelta(minutes=15)
        )
        tx_london = Transaction(
            account_id=account_example.account_id, merchant_id=merchant_london.merchant_id,
            amount=25000000.00, transaction_type=TransactionType.Online_Purchase, channel="Web_Portal", 
            ip_address="82.163.20.1", device_fingerprint="HASH_UNKNOWN_PC_999",
            latitude=51.5074, longitude=-0.1278, status=TransactionStatus.Success, 
            timestamp=date_now - timedelta(minutes=5)
        )

        db.add_all([tx_bandung, tx_london])
        db.commit()

        fraud_txs = []
        for i in range(15):
            random_hours_ago = random.randint(1, 72)
            tx_time = date_now - timedelta(hours=random_hours_ago)
            
            fraud_amount = float(random.randint(15000, 50000) * 1000)
            
            tx = Transaction(
                account_id=account_example.account_id,
                merchant_id=merchant_london.merchant_id, 
                amount=fraud_amount, 
                transaction_type=TransactionType.Online_Purchase,
                channel="Web_Portal", 
                ip_address=fake.ipv4(),
                device_fingerprint=f"HASH_HACKER_DEVICE_{i}",
                latitude=51.5074, longitude=-0.1278,
                status=TransactionStatus.Blocked, 
                timestamp=tx_time
            )
            fraud_txs.append(tx)
            
        db.add_all(fraud_txs)
        db.commit()
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()