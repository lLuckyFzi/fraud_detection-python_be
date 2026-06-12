import pandas as pd
from database import engine

def extract_to_csv():
    print("Menarik data terintegrasi dari database...")
    
    query = """
        SELECT 
            t.transaction_id,
            t.amount,
            t.channel,
            t.latitude,
            t.longitude,
            v.avg_amount_30d,
            v.tx_count_24h,
            v.failed_tx_count_24h,
            t.status
        FROM transactions t
        JOIN v_ml_user_features v ON t.transaction_id = v.transaction_id
    """
    
    df = pd.read_sql(query, engine)
    
    df['is_fraud'] = df['status'].apply(lambda x: 1 if x == 'Blocked' else 0)
    df.drop(columns=['status'], inplace=True)
    
    filename = "raw_fraud_dataset.csv"
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    extract_to_csv()