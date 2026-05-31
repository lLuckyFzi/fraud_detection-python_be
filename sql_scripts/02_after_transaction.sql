DROP TRIGGER IF EXISTS after_transaction_insert;

-- SPLIT --

CREATE TRIGGER after_transaction_insert
AFTER INSERT ON transactions
FOR EACH ROW
BEGIN
    IF @is_fraud = 1 AND NEW.status = 'Blocked' THEN
        
        INSERT INTO fraud_alerts (
            transaction_id,
            trigger_rule_name,
            calculated_risk_score,
            status,
            investigator_notes,
            created_at
        ) VALUES (
            NEW.transaction_id,
            'Impossible Travel Detection',
            99,
            'Open',
            CONCAT('Transaction blocked due to impossible travel. Distance: ', ROUND(@fraud_dist, 2), ' km, Time Difference: ', ROUND(@fraud_time, 2), ' hours, Speed: ', ROUND(@fraud_speed, 2), ' km/h.'),
            NOW()
        );

        UPDATE accounts SET status = 'Suspended' WHERE account_id = NEW.account_id;

        SET @is_fraud = 0;
    END IF;
END;