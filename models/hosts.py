"""
HiddenYatra — Host Profile & Listing Database Operations
Handles host registration, profile management, listing CRUD, and admin moderation.
"""
import hashlib
import logging
from models.connection import get_cursor, get_db

logger = logging.getLogger(__name__)


# ════════════════════════════════════════════════════════════════
# HOST PROFILE OPERATIONS
# ════════════════════════════════════════════════════════════════

def create_host_profile(user_id, bio='', languages='Hindi', address_line='',
                        district_id=None, block_id=None, pin_code='',
                        profile_photo='', id_type='', id_number='',
                        emergency_name='', emergency_phone='',
                        latitude=None, longitude=None):
    """Create a new host profile and mark user as host."""
    # Hash government ID number for privacy
    id_number_hash = ''
    if id_number:
        id_number_hash = hashlib.sha256(id_number.strip().encode()).hexdigest()

    with get_cursor(commit=True) as cur:
        cur.execute("""
            INSERT INTO host_profiles
                (user_id, bio, languages, address_line, district_id, block_id,
                 pin_code, latitude, longitude, profile_photo,
                 id_type, id_number_hash, emergency_name, emergency_phone,
                 verification_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending')
        """, (user_id, bio.strip(), languages.strip(), address_line.strip(),
              district_id or None, block_id or None, pin_code.strip(),
              latitude, longitude, profile_photo,
              id_type.strip(), id_number_hash,
              emergency_name.strip(), emergency_phone.strip()))
        host_id = cur.lastrowid

        # Mark user as host
        cur.execute("UPDATE users SET is_host = 1 WHERE id = %s", (user_id,))
        return host_id


def get_host_profile_by_user(user_id):
    """Get host profile for a user."""
    with get_cursor() as cur:
        cur.execute("""
            SELECT hp.*, u.username, u.display_name, u.full_name, u.email,
                   u.phone, u.avatar_emoji, u.phone_verified, u.email_verified,
                   d.name AS district_name, b.name AS block_name,
                   s.name AS state_name
            FROM host_profiles hp
            JOIN users u ON u.id = hp.user_id
            LEFT JOIN districts d ON d.id = hp.district_id
            LEFT JOIN blocks b ON b.id = hp.block_id
            LEFT JOIN states s ON s.id = d.state_id
            WHERE hp.user_id = %s
        """, (user_id,))
        return cur.fetchone()


def get_host_profile_by_id(host_id):
    """Get host profile by host_profiles.id."""
    with get_cursor() as cur:
        cur.execute("""
            SELECT hp.*, u.username, u.display_name, u.full_name, u.email,
                   u.phone, u.avatar_emoji, u.phone_verified, u.email_verified,
                   d.name AS district_name, b.name AS block_name,
                   s.name AS state_name
            FROM host_profiles hp
            JOIN users u ON u.id = hp.user_id
            LEFT JOIN districts d ON d.id = hp.district_id
            LEFT JOIN blocks b ON b.id = hp.block_id
            LEFT JOIN states s ON s.id = d.state_id
            WHERE hp.id = %s
        """, (host_id,))
        return cur.fetchone()


def update_host_profile(host_id, **kwargs):
    """Update host profile fields. Only updates provided kwargs."""
    allowed = {
        'bio', 'languages', 'address_line', 'district_id', 'block_id',
        'pin_code', 'latitude', 'longitude', 'profile_photo',
        'emergency_name', 'emergency_phone'
    }
    updates = {k: v for k, v in kwargs.items() if k in allowed and v is not None}
    if not updates:
        return

    set_clause = ', '.join(f"{k} = %s" for k in updates)
    values = list(updates.values()) + [host_id]
    with get_cursor(commit=True) as cur:
        cur.execute(f"UPDATE host_profiles SET {set_clause} WHERE id = %s", values)


# ════════════════════════════════════════════════════════════════
# ADMIN HOST MANAGEMENT
# ════════════════════════════════════════════════════════════════

def get_all_hosts_admin(status=None, page=1, per_page=20):
    """Get all host profiles for admin panel with pagination."""
    offset = (page - 1) * per_page
    with get_cursor() as cur:
        where = ""
        params = []
        if status:
            where = "WHERE hp.verification_status = %s"
            params.append(status)

        cur.execute(f"""
            SELECT hp.*, u.username, u.display_name, u.full_name, u.email,
                   u.phone, u.status AS user_status,
                   d.name AS district_name
            FROM host_profiles hp
            JOIN users u ON u.id = hp.user_id
            LEFT JOIN districts d ON d.id = hp.district_id
            {where}
            ORDER BY
                CASE hp.verification_status
                    WHEN 'pending' THEN 1
                    WHEN 'under_review' THEN 2
                    WHEN 'approved' THEN 3
                    WHEN 'rejected' THEN 4
                    WHEN 'suspended' THEN 5
                END,
                hp.created_at DESC
            LIMIT %s OFFSET %s
        """, params + [per_page, offset])
        hosts = cur.fetchall()

        # Get total count
        cur.execute(f"""
            SELECT COUNT(*) AS cnt FROM host_profiles hp {where}
        """, params)
        total = cur.fetchone()['cnt']
        return hosts, total


def count_hosts_by_status():
    """Count hosts grouped by verification status."""
    with get_cursor() as cur:
        cur.execute("""
            SELECT verification_status, COUNT(*) AS cnt
            FROM host_profiles
            GROUP BY verification_status
        """)
        result = {row['verification_status']: row['cnt'] for row in cur.fetchall()}
        result['total'] = sum(result.values())
        return result


def approve_host(host_id, admin_user='admin'):
    """Approve a host application."""
    with get_cursor(commit=True) as cur:
        cur.execute("""
            UPDATE host_profiles
            SET verification_status = 'approved',
                verified_at = NOW(),
                verified_by = %s,
                is_verified_badge = 1,
                rejection_reason = NULL
            WHERE id = %s
        """, (admin_user, host_id))

        # Get user_id for notification
        cur.execute("SELECT user_id FROM host_profiles WHERE id = %s", (host_id,))
        row = cur.fetchone()
        if row:
            _notify(cur, row['user_id'], 'host_approved',
                    'Host Application Approved! 🎉',
                    'Congratulations! Your host profile has been verified. You can now create listings.',
                    '/host/dashboard')
        return True


def reject_host(host_id, reason='', admin_user='admin'):
    """Reject a host application."""
    with get_cursor(commit=True) as cur:
        cur.execute("""
            UPDATE host_profiles
            SET verification_status = 'rejected',
                verified_at = NOW(),
                verified_by = %s,
                rejection_reason = %s,
                is_verified_badge = 0
            WHERE id = %s
        """, (admin_user, reason, host_id))

        cur.execute("SELECT user_id FROM host_profiles WHERE id = %s", (host_id,))
        row = cur.fetchone()
        if row:
            _notify(cur, row['user_id'], 'host_rejected',
                    'Host Application Update',
                    f'Your host application needs updates. Reason: {reason}',
                    '/host/become')
        return True


def suspend_host(host_id, reason='', admin_user='admin'):
    """Suspend an approved host."""
    with get_cursor(commit=True) as cur:
        cur.execute("""
            UPDATE host_profiles
            SET verification_status = 'suspended',
                rejection_reason = %s,
                is_verified_badge = 0
            WHERE id = %s
        """, (reason, host_id))

        # Also suspend all their listings
        cur.execute("""
            UPDATE host_listings SET status = 'suspended'
            WHERE host_id = %s AND status = 'published'
        """, (host_id,))
        return True


def reinstate_host(host_id, admin_user='admin'):
    """Reinstate a suspended host."""
    with get_cursor(commit=True) as cur:
        cur.execute("""
            UPDATE host_profiles
            SET verification_status = 'approved',
                is_verified_badge = 1,
                rejection_reason = NULL
            WHERE id = %s
        """, (host_id,))
        return True


def set_host_review_status(host_id, admin_user='admin'):
    """Mark a host as 'under_review'."""
    with get_cursor(commit=True) as cur:
        cur.execute("""
            UPDATE host_profiles
            SET verification_status = 'under_review',
                verified_by = %s
            WHERE id = %s AND verification_status = 'pending'
        """, (admin_user, host_id))


# ════════════════════════════════════════════════════════════════
# NOTIFICATIONS HELPER
# ════════════════════════════════════════════════════════════════

def _notify(cur, user_id, notif_type, title, message, link=''):
    """Insert a notification (used within an existing cursor context)."""
    cur.execute("""
        INSERT INTO notifications (user_id, type, title, message, link)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, notif_type, title, message, link))


# ════════════════════════════════════════════════════════════════
# NOTIFICATIONS PUBLIC API
# ════════════════════════════════════════════════════════════════

def get_notifications(user_id, limit=20, unread_only=False):
    """Get notifications for a user."""
    with get_cursor() as cur:
        where = "WHERE user_id = %s"
        params = [user_id]
        if unread_only:
            where += " AND is_read = 0"
        cur.execute(f"""
            SELECT * FROM notifications {where}
            ORDER BY created_at DESC LIMIT %s
        """, params + [limit])
        return cur.fetchall()


def count_unread_notifications(user_id):
    """Count unread notifications for a user."""
    with get_cursor() as cur:
        cur.execute("""
            SELECT COUNT(*) AS cnt FROM notifications
            WHERE user_id = %s AND is_read = 0
        """, (user_id,))
        return cur.fetchone()['cnt']


def mark_notifications_read(user_id, notification_ids=None):
    """Mark notifications as read."""
    with get_cursor(commit=True) as cur:
        if notification_ids:
            placeholders = ','.join(['%s'] * len(notification_ids))
            cur.execute(f"""
                UPDATE notifications SET is_read = 1
                WHERE user_id = %s AND id IN ({placeholders})
            """, [user_id] + list(notification_ids))
        else:
            cur.execute("""
                UPDATE notifications SET is_read = 1
                WHERE user_id = %s AND is_read = 0
            """, (user_id,))


def create_notification(user_id, notif_type, title, message, link=''):
    """Create a notification for a user."""
    with get_cursor(commit=True) as cur:
        _notify(cur, user_id, notif_type, title, message, link)
