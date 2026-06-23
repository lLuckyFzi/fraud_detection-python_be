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

        all_transactions = []
        date_now = datetime.now(timezone.utc)

        for i in range(200):
            rand_val = random.random()
            tx_time = date_now - timedelta(hours=random.randint(1, 720)) # 30 days range
            
            if rand_val < 0.80:
                # SCENARIO 1 (80%) Normal Transaction
                amount = float(random.randint(15, 500) * 1000)
                status = TransactionStatus.Success
                merchant = random.choice(merchants_normal)
                
                # Probabilitas Saluran: 90% Mobile, 10% Web Portal
                channel = "Mobile_Banking" if random.random() < 0.90 else "Web_Portal"
                
                ip = "114.120.10.5" # IP konsisten
                lat, lon = -6.9147, 107.6098
                
            elif rand_val < 0.90:
                # SCENARIO 2 (10% - Edge Case) High-Value Local Transaction
                amount = float(random.randint(10000, 30000) * 1000)
                status = TransactionStatus.Success
                merchant = random.choice(merchants_normal) 
                
                # propability 70% Mobile Banking, 30% Web Portal
                channel = "Mobile_Banking" if random.random() < 0.70 else "Web_Portal"
                
                ip = "114.120.10.5"
                lat, lon = -6.9147, 107.6098
                
            elif rand_val < 0.98:
                # SCENARIO 3 8% Fraud Tipikal
                amount = float(random.randint(5000, 50000) * 1000)
                status = TransactionStatus.Blocked
                
                # Probabilitas location 80% abroad, 20% hacker using local VPN
                if random.random() < 0.80:
                    merchant = merchant_london
                    ip = fake.ipv4()
                    lat, lon = 51.5074, -0.1278
                else:
                    merchant = random.choice(merchants_normal)
                    ip = fake.ipv4() # IP tetap aneh/acak meski lokasinya Bandung
                    lat, lon = -6.9147, 107.6098
                
                # propability 80% Web Portal, 20% Mobile Banking
                channel = "Web_Portal" if random.random() < 0.80 else "Mobile_Banking"
                
            else:
                # SCENARIO 4 (2% - Edge Case): Fraud Card Testing
                amount = float(random.randint(5, 50) * 1000)
                status = TransactionStatus.Blocked
                merchant = merchant_london
                ip = fake.ipv4()
                lat, lon = 51.5074, -0.1278
                channel = "Web_Portal" if random.random() < 0.90 else "Mobile_Banking"

            tx = Transaction(
                account_id=account_example.account_id,
                merchant_id=merchant.merchant_id,
                amount=amount,
                transaction_type=TransactionType.Online_Purchase,
                channel=channel,
                ip_address=ip,
                device_fingerprint=f"HASH_DEV_{'BUDI' if status == TransactionStatus.Success else 'HACKER_'+str(i)}",
                latitude=lat, longitude=lon,
                status=status,
                timestamp=tx_time
            )
            all_transactions.append(tx)

        db.add_all(all_transactions)
        db.commit()
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()