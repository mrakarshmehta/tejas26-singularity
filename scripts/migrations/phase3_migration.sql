-- ═══════════════════════════════════════════════════════════════════
-- Phase 3 — HiddenYatra Local Host / Homestay & Free Stay Platform
-- Migration Script (ADDITIVE ONLY — no existing tables modified)
-- ═══════════════════════════════════════════════════════════════════

USE hiddenyatra;

-- ──────────────────────────────────────────────
-- STEP 1: Add 2 columns to existing users table
-- (safe, non-destructive ALTER TABLE ADD COLUMN)
-- ──────────────────────────────────────────────

-- Add is_host flag
SET @col_exists = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'hiddenyatra' AND TABLE_NAME = 'users' AND COLUMN_NAME = 'is_host');
SET @sql = IF(@col_exists = 0,
    'ALTER TABLE users ADD COLUMN is_host TINYINT(1) NOT NULL DEFAULT 0 AFTER is_admin',
    'SELECT "Column is_host already exists"');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Add phone_verified flag
SET @col_exists = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'hiddenyatra' AND TABLE_NAME = 'users' AND COLUMN_NAME = 'phone_verified');
SET @sql = IF(@col_exists = 0,
    'ALTER TABLE users ADD COLUMN phone_verified TINYINT(1) NOT NULL DEFAULT 0 AFTER email_verified',
    'SELECT "Column phone_verified already exists"');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ──────────────────────────────────────────────
-- STEP 2: Host Profiles
-- ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS host_profiles (
    id                  INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id             INT UNSIGNED NOT NULL UNIQUE,
    bio                 TEXT NOT NULL DEFAULT (''),
    languages           VARCHAR(500) NOT NULL DEFAULT 'Hindi',
    address_line        VARCHAR(500) NOT NULL DEFAULT '',
    district_id         INT UNSIGNED DEFAULT NULL,
    block_id            INT UNSIGNED DEFAULT NULL,
    pin_code            VARCHAR(10) NOT NULL DEFAULT '',
    latitude            DECIMAL(10,7) DEFAULT NULL,
    longitude           DECIMAL(10,7) DEFAULT NULL,
    profile_photo       VARCHAR(255) NOT NULL DEFAULT '',
    id_type             VARCHAR(50) NOT NULL DEFAULT '',
    id_number_hash      VARCHAR(255) NOT NULL DEFAULT '',
    emergency_name      VARCHAR(100) NOT NULL DEFAULT '',
    emergency_phone     VARCHAR(20) NOT NULL DEFAULT '',
    verification_status ENUM('pending','under_review','approved','rejected','suspended')
                        NOT NULL DEFAULT 'pending',
    verified_at         DATETIME DEFAULT NULL,
    verified_by         VARCHAR(100) DEFAULT NULL,
    rejection_reason    TEXT DEFAULT NULL,
    is_verified_badge   TINYINT(1) NOT NULL DEFAULT 0,
    avg_host_rating     DECIMAL(3,1) NOT NULL DEFAULT 0.0,
    total_hosted        INT UNSIGNED NOT NULL DEFAULT 0,
    response_rate       DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    response_time_hrs   DECIMAL(5,1) NOT NULL DEFAULT 0.0,
    created_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_host_district (district_id),
    INDEX idx_host_status (verification_status),
    INDEX idx_host_verified (is_verified_badge),
    CONSTRAINT fk_host_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_host_district FOREIGN KEY (district_id) REFERENCES districts(id) ON DELETE SET NULL,
    CONSTRAINT fk_host_block FOREIGN KEY (block_id) REFERENCES blocks(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ──────────────────────────────────────────────
-- STEP 3: Host Listings
-- ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS host_listings (
    id                  INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    host_id             INT UNSIGNED NOT NULL,
    listing_type        ENUM('paid_homestay','free_stay','local_experience')
                        NOT NULL DEFAULT 'paid_homestay',
    title               VARCHAR(200) NOT NULL,
    slug                VARCHAR(250) NOT NULL,
    description         TEXT NOT NULL DEFAULT (''),
    district_id         INT UNSIGNED DEFAULT NULL,
    block_id            INT UNSIGNED DEFAULT NULL,
    address_text        VARCHAR(500) NOT NULL DEFAULT '',
    address_full        VARCHAR(500) NOT NULL DEFAULT '',
    latitude            DECIMAL(10,7) DEFAULT NULL,
    longitude           DECIMAL(10,7) DEFAULT NULL,
    price_per_night     DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    currency            VARCHAR(5) NOT NULL DEFAULT 'INR',
    max_guests          SMALLINT UNSIGNED NOT NULL DEFAULT 2,
    num_rooms           SMALLINT UNSIGNED NOT NULL DEFAULT 1,
    num_beds            SMALLINT UNSIGNED NOT NULL DEFAULT 1,
    num_bathrooms       SMALLINT UNSIGNED NOT NULL DEFAULT 1,
    property_type       VARCHAR(50) NOT NULL DEFAULT 'room',
    amenities           JSON DEFAULT NULL,
    house_rules         TEXT NOT NULL DEFAULT (''),
    check_in_time       VARCHAR(20) NOT NULL DEFAULT '14:00',
    check_out_time      VARCHAR(20) NOT NULL DEFAULT '11:00',
    cancellation_policy VARCHAR(50) NOT NULL DEFAULT 'flexible',
    cover_image         VARCHAR(255) NOT NULL DEFAULT '',
    status              ENUM('draft','submitted','under_review','published','rejected','suspended','archived')
                        NOT NULL DEFAULT 'draft',
    rejection_reason    TEXT DEFAULT NULL,
    is_featured         TINYINT(1) NOT NULL DEFAULT 0,
    avg_rating          DECIMAL(3,1) NOT NULL DEFAULT 0.0,
    review_count        INT UNSIGNED NOT NULL DEFAULT 0,
    view_count          INT UNSIGNED NOT NULL DEFAULT 0,
    created_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_listing_slug (slug),
    INDEX idx_listing_host (host_id),
    INDEX idx_listing_district (district_id),
    INDEX idx_listing_type (listing_type),
    INDEX idx_listing_status (status),
    INDEX idx_listing_price (price_per_night),
    INDEX idx_listing_featured (is_featured),
    INDEX idx_listing_lat_lng (latitude, longitude),
    CONSTRAINT fk_listing_host FOREIGN KEY (host_id) REFERENCES host_profiles(id) ON DELETE CASCADE,
    CONSTRAINT fk_listing_district FOREIGN KEY (district_id) REFERENCES districts(id) ON DELETE SET NULL,
    CONSTRAINT fk_listing_block FOREIGN KEY (block_id) REFERENCES blocks(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ──────────────────────────────────────────────
-- STEP 4: Listing Photos
-- ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS listing_photos (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    listing_id  INT UNSIGNED NOT NULL,
    filename    VARCHAR(255) NOT NULL,
    caption     VARCHAR(500) NOT NULL DEFAULT '',
    sort_order  INT NOT NULL DEFAULT 0,
    uploaded_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_listing_photos (listing_id),
    CONSTRAINT fk_lphotos_listing FOREIGN KEY (listing_id) REFERENCES host_listings(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ──────────────────────────────────────────────
-- STEP 5: Listing Availability Calendar
-- ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS listing_availability (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    listing_id      INT UNSIGNED NOT NULL,
    date            DATE NOT NULL,
    is_available    TINYINT(1) NOT NULL DEFAULT 1,
    custom_price    DECIMAL(10,2) DEFAULT NULL,
    notes           VARCHAR(255) NOT NULL DEFAULT '',
    UNIQUE KEY uq_listing_date (listing_id, date),
    INDEX idx_avail_listing (listing_id),
    CONSTRAINT fk_avail_listing FOREIGN KEY (listing_id) REFERENCES host_listings(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ──────────────────────────────────────────────
-- STEP 6: Stay Requests
-- ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS stay_requests (
    id                  INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    listing_id          INT UNSIGNED NOT NULL,
    traveller_id        INT UNSIGNED NOT NULL,
    host_id             INT UNSIGNED NOT NULL,
    check_in_date       DATE NOT NULL,
    check_out_date      DATE NOT NULL,
    num_guests          SMALLINT UNSIGNED NOT NULL DEFAULT 1,
    total_price         DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    message             TEXT NOT NULL DEFAULT (''),
    status              ENUM('pending','accepted','rejected','expired',
                             'confirmed','checked_in','completed',
                             'cancelled_by_traveller','cancelled_by_host')
                        NOT NULL DEFAULT 'pending',
    host_response       TEXT NOT NULL DEFAULT (''),
    responded_at        DATETIME DEFAULT NULL,
    confirmed_at        DATETIME DEFAULT NULL,
    cancelled_at        DATETIME DEFAULT NULL,
    cancellation_reason TEXT DEFAULT NULL,
    expires_at          DATETIME DEFAULT NULL,
    created_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_req_listing (listing_id),
    INDEX idx_req_traveller (traveller_id),
    INDEX idx_req_host (host_id),
    INDEX idx_req_status (status),
    INDEX idx_req_dates (check_in_date, check_out_date),
    INDEX idx_req_expires (expires_at),
    CONSTRAINT fk_req_listing FOREIGN KEY (listing_id) REFERENCES host_listings(id) ON DELETE CASCADE,
    CONSTRAINT fk_req_traveller FOREIGN KEY (traveller_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_req_host FOREIGN KEY (host_id) REFERENCES host_profiles(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ──────────────────────────────────────────────
-- STEP 7: Stay Reviews (bidirectional)
-- ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS stay_reviews (
    id                  INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    stay_request_id     INT UNSIGNED NOT NULL,
    reviewer_id         INT UNSIGNED NOT NULL,
    reviewee_type       ENUM('host','traveller') NOT NULL,
    rating              TINYINT UNSIGNED NOT NULL,
    cleanliness         TINYINT UNSIGNED DEFAULT NULL,
    communication       TINYINT UNSIGNED DEFAULT NULL,
    location            TINYINT UNSIGNED DEFAULT NULL,
    value               TINYINT UNSIGNED DEFAULT NULL,
    comment             TEXT NOT NULL DEFAULT (''),
    is_public           TINYINT(1) NOT NULL DEFAULT 1,
    created_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_stay_review (stay_request_id, reviewer_id),
    INDEX idx_sreview_request (stay_request_id),
    INDEX idx_sreview_reviewer (reviewer_id),
    CONSTRAINT fk_sreview_request FOREIGN KEY (stay_request_id) REFERENCES stay_requests(id) ON DELETE CASCADE,
    CONSTRAINT fk_sreview_reviewer FOREIGN KEY (reviewer_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT chk_sreview_rating CHECK (rating BETWEEN 1 AND 5)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ──────────────────────────────────────────────
-- STEP 8: Local Experiences
-- ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS local_experiences (
    id                  INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    host_id             INT UNSIGNED NOT NULL,
    title               VARCHAR(200) NOT NULL,
    description         TEXT NOT NULL DEFAULT (''),
    experience_type     VARCHAR(50) NOT NULL DEFAULT 'guided_tour',
    duration_hours      DECIMAL(4,1) NOT NULL DEFAULT 2.0,
    price               DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    max_participants    SMALLINT UNSIGNED NOT NULL DEFAULT 5,
    cover_image         VARCHAR(255) NOT NULL DEFAULT '',
    district_id         INT UNSIGNED DEFAULT NULL,
    status              ENUM('draft','published','suspended') NOT NULL DEFAULT 'draft',
    created_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_exp_host (host_id),
    INDEX idx_exp_district (district_id),
    INDEX idx_exp_type (experience_type),
    CONSTRAINT fk_exp_host FOREIGN KEY (host_id) REFERENCES host_profiles(id) ON DELETE CASCADE,
    CONSTRAINT fk_exp_district FOREIGN KEY (district_id) REFERENCES districts(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ──────────────────────────────────────────────
-- STEP 9: Reports (safety/moderation)
-- ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS host_reports (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    reporter_id     INT UNSIGNED NOT NULL,
    reported_type   ENUM('host','listing','traveller','review') NOT NULL,
    reported_id     INT UNSIGNED NOT NULL,
    reason          VARCHAR(50) NOT NULL,
    details         TEXT NOT NULL DEFAULT (''),
    status          ENUM('pending','investigating','resolved','dismissed')
                    NOT NULL DEFAULT 'pending',
    admin_notes     TEXT DEFAULT NULL,
    resolved_by     VARCHAR(100) DEFAULT NULL,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at     DATETIME DEFAULT NULL,
    INDEX idx_report_status (status),
    INDEX idx_report_type (reported_type, reported_id),
    CONSTRAINT fk_report_reporter FOREIGN KEY (reporter_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ──────────────────────────────────────────────
-- STEP 10: Notifications
-- ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS notifications (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id     INT UNSIGNED NOT NULL,
    type        VARCHAR(50) NOT NULL,
    title       VARCHAR(200) NOT NULL,
    message     TEXT NOT NULL DEFAULT (''),
    link        VARCHAR(500) NOT NULL DEFAULT '',
    is_read     TINYINT(1) NOT NULL DEFAULT 0,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_notif_user (user_id, is_read),
    INDEX idx_notif_created (created_at),
    CONSTRAINT fk_notif_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ──────────────────────────────────────────────
-- STEP 11: User Blocks (safety — block/mute)
-- ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS user_blocks (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    blocker_id  INT UNSIGNED NOT NULL,
    blocked_id  INT UNSIGNED NOT NULL,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_user_block (blocker_id, blocked_id),
    CONSTRAINT fk_block_blocker FOREIGN KEY (blocker_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_block_blocked FOREIGN KEY (blocked_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ══════════════════════════════════════════════
-- Verification: count tables after migration
-- ══════════════════════════════════════════════
SELECT COUNT(*) AS total_tables FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'hiddenyatra' AND TABLE_TYPE = 'BASE TABLE';
