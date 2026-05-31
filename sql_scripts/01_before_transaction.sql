DROP TRIGGER IF EXISTS before_transaction_insert;

-- SPLIT --

CREATE TRIGGER before_transaction_insert
BEFORE INSERT ON transactions
FOR EACH ROW
BEGIN
    DECLARE prev_lat DECIMAL(9, 6);
    DECLARE prev_lon DECIMAL(9, 6);
    DECLARE prev_time TIMESTAMP;
    DECLARE dist_km FLOAT;
    DECLARE time_diff_hours FLOAT;
    DECLARE travel_speed FLOAT;

    -- CONSTANT VARIABLES
    DECLARE METERS_IN_KM INT DEFAULT 1000;
    DECLARE SECONDS_IN_HOUR INT DEFAULT 3600;
    DECLARE MAX_ALLOWED_SPEED_KMH FLOAT DEFAULT 900.0;

    -- Get the most recent transaction for the same card
    SELECT latitude, longitude, timestamp
    INTO prev_lat, prev_lon, prev_time
    FROM transactions
    WHERE account_id = NEW.account_id AND status = 'Success'
    ORDER BY timestamp DESC
    LIMIT 1;

    -- If there is a previous transaction, calculate distance and speed
    IF prev_lat IS NOT NULL THEN
        -- Calculate distance using Haversine formula
        SET dist_km = ST_Distance_Sphere(
            point(prev_lon, prev_lat),
            point(NEW.longitude, NEW.latitude)
        ) / METERS_IN_KM; -- Convert meters to kilometers

        SET time_diff_hours = TIMESTAMPDIFF(SECOND, prev_time, NEW.timestamp) / SECONDS_IN_HOUR; -- Convert seconds to hours

        IF time_diff_hours > 0 THEN
            SET travel_speed = dist_km / time_diff_hours;

            IF travel_speed > MAX_ALLOWED_SPEED_KMH THEN
                SET NEW.status = 'Blocked';

                SET @is_fraud = 1;
                SET @fraud_dist = dist_km;
                SET @fraud_time = time_diff_hours;
                SET @fraud_speed = travel_speed;
            ELSE
                SET @is_fraud = 0;
            END IF;
        ELSE
            SET @is_fraud = 0;
        END IF;
    ELSE
        SET @is_fraud = 0;
    END IF;
END;