CREATE OR REPLACE VIEW v_ml_user_features AS
SELECT 
    t1.transaction_id,
    t1.account_id,
    
    COALESCE((SELECT AVG(t2.amount) 
     FROM transactions t2 
     WHERE t2.account_id = t1.account_id 
       AND t2.timestamp <= t1.timestamp 
       AND t2.timestamp >= t1.timestamp - INTERVAL 30 DAY), 0) AS avg_amount_30d,
       
    COALESCE((SELECT COUNT(t2.transaction_id) 
     FROM transactions t2 
     WHERE t2.account_id = t1.account_id 
       AND t2.timestamp <= t1.timestamp 
       AND t2.timestamp >= t1.timestamp - INTERVAL 24 HOUR), 0) AS tx_count_24h,
       
    COALESCE((SELECT COUNT(t2.transaction_id) 
     FROM transactions t2 
     WHERE t2.account_id = t1.account_id 
       AND t2.status IN ('Failed', 'Blocked')
       AND t2.timestamp <= t1.timestamp 
       AND t2.timestamp >= t1.timestamp - INTERVAL 24 HOUR), 0) AS failed_tx_count_24h

FROM transactions t1;