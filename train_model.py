import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
from database import engine

def train_fraud_detection_model():
    query = """
        SELECT 
            t.amount,
            t.transaction_type,
            t.status,
            v.avg_amount_30d,
            v.tx_count_24h,
            v.failed_tx_count_24h
        FROM transactions t
        JOIN v_ml_user_features v ON t.account_id = v.account_id
    """
    
    df = pd.read_sql(query, engine)
    print(f"Berhasil menarik {len(df)} baris data transaksi.")

    df = pd.get_dummies(df, columns=['transaction_type'], drop_first=True)
    
    df['is_fraud'] = df['status'].apply(lambda x: 1 if x == 'Blocked' else 0)
    
    X = df.drop(columns=['status', 'is_fraud'])
    y = df['is_fraud']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(f"Akurasi Model: {accuracy_score(y_test, y_pred) * 100:.2f}%\n")

    print("Laporan Klasifikasi:")
    print(classification_report(y_test, y_pred, zero_division=0))

    model_filename = "fraud_model.pkl"
    joblib.dump(model, model_filename)
    print(f"Model berhasil disimpan sebagai {model_filename}!")

if __name__ == "__main__":
    train_fraud_detection_model()