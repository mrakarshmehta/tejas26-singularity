-- Phase 3.2A Migration: Additive columns for min/max stay nights
-- Safe: Only ADDs columns. Does NOT modify/drop/delete anything.

-- Check if columns exist first via procedure
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS _phase32a_migrate()
BEGIN
    -- Add min_stay_nights if not exists
    IF NOT EXISTS (
        SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = 'host_listings'
          AND COLUMN_NAME = 'min_stay_nights'
    ) THEN
        ALTER TABLE host_listings
            ADD COLUMN min_stay_nights SMALLINT UNSIGNED NOT NULL DEFAULT 1 AFTER max_guests;
    END IF;

    -- Add max_stay_nights if not exists
    IF NOT EXISTS (
        SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = 'host_listings'
          AND COLUMN_NAME = 'max_stay_nights'
    ) THEN
        ALTER TABLE host_listings
            ADD COLUMN max_stay_nights SMALLINT UNSIGNED NOT NULL DEFAULT 0 AFTER min_stay_nights;
    END IF;
END //
DELIMITER ;

CALL _phase32a_migrate();
DROP PROCEDURE IF EXISTS _phase32a_migrate;

-- Verify
SELECT COLUMN_NAME, COLUMN_TYPE, COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME = 'host_listings'
  AND COLUMN_NAME IN ('min_stay_nights', 'max_stay_nights', 'max_guests')
ORDER BY ORDINAL_POSITION;
