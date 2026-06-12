CREATE OR REPLACE VIEW v_ml_user_features AS
SELECT 
    t.account_id,
    AVG(CASE WHEN t.timestamp >= NOW() - INTERVAL 30 DAY THEN t.amount ELSE 0 END) AS avg_amount_30d,
    
    SUM(CASE WHEN t.timestamp >= NOW() - INTERVAL 24 HOUR THEN 1 ELSE 0 END) AS tx_count_24h,
    
    SUM(CASE WHEN t.status IN ('Failed', 'Blocked') AND t.timestamp >= NOW() - INTERVAL 24 HOUR THEN 1 ELSE 0 END) AS failed_tx_count_24h,
    
    (SELECT m.country_code 
     FROM transactions tr 
     JOIN merchants m ON tr.merchant_id = m.merchant_id 
     WHERE tr.account_id = t.account_id 
     ORDER BY tr.timestamp DESC LIMIT 1) AS last_known_country

FROM transactions t
GROUP BY t.account_id;