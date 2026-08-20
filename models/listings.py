"""
HiddenYatra — Listing CRUD & Search Operations
Handles host listing creation, updates, photo management, traveller search,
and admin moderation for the Local Stay / Homestay platform.
"""
import os
import re
import uuid
import logging
from models.connection import get_cursor

logger = logging.getLogger(__name__)

# ════════════════════════════════════════════════════════════════
# SLUG GENERATION
# ════════════════════════════════════════════════════════════════

def generate_listing_slug(title):
    """Generate a unique URL slug from listing title."""
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower().strip()).strip('-')[:200]
    if not slug:
        slug = 'listing'
    with get_cursor() as cur:
        base = slug
        counter = 0
        while True:
            cur.execute("SELECT id FROM host_listings WHERE slug = %s", (slug,))
            if not cur.fetchone():
                return slug
            counter += 1
            slug = f"{base}-{counter}"


# ════════════════════════════════════════════════════════════════
# LISTING CRUD
# ════════════════════════════════════════════════════════════════

def create_listing(host_id, listing_type='paid_homestay', title='', description='',
                   district_id=None, block_id=None, address_text='', address_full='',
                   latitude=None, longitude=None, price_per_night=0,
                   max_guests=2, min_stay_nights=1, max_stay_nights=0,
                   num_rooms=1, num_beds=1, num_bathrooms=1,
                   property_type='room', amenities=None, house_rules='',
                   check_in_time='14:00', check_out_time='11:00',
                   cancellation_policy='flexible'):
    """Create a new listing in draft status."""
    import json
    slug = generate_listing_slug(title)
    amenities_json = json.dumps(amenities) if amenities else None

    # Free stays must have price = 0
    if listing_type == 'free_stay':
        price_per_night = 0

    with get_cursor(commit=True) as cur:
        cur.execute("""
            INSERT INTO host_listings
                (host_id, listing_type, title, slug, description,
                 district_id, block_id, address_text, address_full,
                 latitude, longitude, price_per_night, max_guests,
                 min_stay_nights, max_stay_nights,
                 num_rooms, num_beds, num_bathrooms,
                 property_type, amenities, house_rules,
                 check_in_time, check_out_time, cancellation_policy,
                 status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'draft')
        """, (host_id, listing_type, title.strip(), slug, description.strip(),
              district_id or None, block_id or None,
              address_text.strip(), address_full.strip(),
              latitude, longitude, price_per_night, max_guests,
              min_stay_nights, max_stay_nights,
              num_rooms, num_beds, num_bathrooms,
              property_type, amenities_json, house_rules.strip(),
              check_in_time, check_out_time, cancellation_policy))
        listing_id = cur.lastrowid
        logger.info(f"Created listing {listing_id} (type={listing_type}) for host {host_id}")
        return listing_id


def update_listing(listing_id, host_id, **kwargs):
    """Update a listing. Only the owning host can update. Only draft/rejected can be edited."""
    import json

    with get_cursor(commit=True) as cur:
        # Verify ownership + editable status
        cur.execute("""
            SELECT id, status FROM host_listings
            WHERE id = %s AND host_id = %s
        """, (listing_id, host_id))
        listing = cur.fetchone()
        if not listing:
            return False
        if listing['status'] not in ('draft', 'rejected'):
            return False

        allowed = {
            'listing_type', 'title', 'description', 'district_id', 'block_id',
            'address_text', 'address_full', 'latitude', 'longitude',
            'price_per_night', 'max_guests', 'min_stay_nights', 'max_stay_nights',
            'num_rooms', 'num_beds', 'num_bathrooms', 'property_type',
            'amenities', 'house_rules', 'check_in_time', 'check_out_time',
            'cancellation_policy'
        }
        updates = {}
        for k, v in kwargs.items():
            if k in allowed and v is not None:
                if k == 'amenities' and isinstance(v, (list, dict)):
                    v = json.dumps(v)
                if k == 'title':
                    v = v.strip()
                    # Regenerate slug if title changed
                    updates['slug'] = generate_listing_slug(v)
                updates[k] = v

        if not updates:
            return True

        # Enforce free_stay price = 0
        if updates.get('listing_type') == 'free_stay':
            updates['price_per_night'] = 0

        set_clause = ', '.join(f"{k} = %s" for k in updates)
        values = list(updates.values()) + [listing_id, host_id]
        cur.execute(
            f"UPDATE host_listings SET {set_clause} WHERE id = %s AND host_id = %s",
            values
        )
        return True


def get_listing_by_id(listing_id):
    """Get a listing with host info."""
    with get_cursor() as cur:
        cur.execute("""
            SELECT hl.*,
                   hp.bio AS host_bio, hp.languages AS host_languages,
                   hp.profile_photo AS host_photo,
                   hp.is_verified_badge, hp.avg_host_rating, hp.total_hosted,
                   hp.response_rate, hp.response_time_hrs,
                   u.display_name AS host_name, u.username AS host_username,
                   d.name AS district_name, d.slug AS district_slug,
                   s.name AS state_name
            FROM host_listings hl
            JOIN host_profiles hp ON hl.host_id = hp.id
            JOIN users u ON hp.user_id = u.id
            LEFT JOIN districts d ON hl.district_id = d.id
            LEFT JOIN states s ON d.state_id = s.id
            WHERE hl.id = %s
        """, (listing_id,))
        listing = cur.fetchone()
        if listing and listing.get('amenities'):
            import json
            try:
                listing['amenities_list'] = json.loads(listing['amenities'])
            except (json.JSONDecodeError, TypeError):
                listing['amenities_list'] = []
        return listing


def get_listing_by_slug(slug):
    """Get a published listing by slug (for public detail page)."""
    with get_cursor() as cur:
        cur.execute("""
            SELECT hl.*,
                   hp.bio AS host_bio, hp.languages AS host_languages,
                   hp.profile_photo AS host_photo, hp.user_id AS host_user_id,
                   hp.is_verified_badge, hp.avg_host_rating, hp.total_hosted,
                   hp.response_rate, hp.response_time_hrs,
                   u.display_name AS host_name, u.username AS host_username,
                   d.name AS district_name, d.slug AS district_slug,
                   s.name AS state_name
            FROM host_listings hl
            JOIN host_profiles hp ON hl.host_id = hp.id
            JOIN users u ON hp.user_id = u.id
            LEFT JOIN districts d ON hl.district_id = d.id
            LEFT JOIN states s ON d.state_id = s.id
            WHERE hl.slug = %s AND hl.status = 'published'
        """, (slug,))
        listing = cur.fetchone()
        if listing and listing.get('amenities'):
            import json
            try:
                listing['amenities_list'] = json.loads(listing['amenities'])
            except (json.JSONDecodeError, TypeError):
                listing['amenities_list'] = []
        return listing


def get_listings_by_host(host_id, status=None):
    """Get all listings for a host, optionally filtered by status."""
    with get_cursor() as cur:
        sql = """
            SELECT hl.*, d.name AS district_name,
                   (SELECT COUNT(*) FROM listing_photos lp WHERE lp.listing_id = hl.id) AS photo_count
            FROM host_listings hl
            LEFT JOIN districts d ON hl.district_id = d.id
            WHERE hl.host_id = %s
        """
        params = [host_id]
        if status:
            sql += " AND hl.status = %s"
            params.append(status)
        sql += " ORDER BY hl.updated_at DESC"
        cur.execute(sql, params)
        return cur.fetchall()


def submit_listing(listing_id, host_id):
    """Submit a draft listing for admin review."""
    with get_cursor(commit=True) as cur:
        cur.execute("""
            UPDATE host_listings
            SET status = 'submitted'
            WHERE id = %s AND host_id = %s AND status IN ('draft', 'rejected')
        """, (listing_id, host_id))
        if cur.rowcount:
            logger.info(f"Listing {listing_id} submitted for review by host {host_id}")
            return True
        return False


def archive_listing(listing_id, host_id):
    """Archive/deactivate a listing (soft delete)."""
    with get_cursor(commit=True) as cur:
        cur.execute("""
            UPDATE host_listings SET status = 'archived'
            WHERE id = %s AND host_id = %s AND status != 'archived'
        """, (listing_id, host_id))
        return bool(cur.rowcount)


def reactivate_listing(listing_id, host_id):
    """Reactivate an archived listing back to draft."""
    with get_cursor(commit=True) as cur:
        cur.execute("""
            UPDATE host_listings SET status = 'draft'
            WHERE id = %s AND host_id = %s AND status = 'archived'
        """, (listing_id, host_id))
        return bool(cur.rowcount)


# ════════════════════════════════════════════════════════════════
# COVER IMAGE
# ════════════════════════════════════════════════════════════════

def set_cover_image(listing_id, host_id, filename):
    """Set the cover image for a listing."""
    with get_cursor(commit=True) as cur:
        cur.execute("""
            UPDATE host_listings SET cover_image = %s
            WHERE id = %s AND host_id = %s
        """, (filename, listing_id, host_id))
        return bool(cur.rowcount)


# ════════════════════════════════════════════════════════════════
# LISTING PHOTOS
# ════════════════════════════════════════════════════════════════

def add_listing_photo(listing_id, filename, caption='', sort_order=0):
    """Add a photo to a listing."""
    with get_cursor(commit=True) as cur:
        cur.execute("""
            INSERT INTO listing_photos (listing_id, filename, caption, sort_order)
            VALUES (%s, %s, %s, %s)
        """, (listing_id, filename, caption, sort_order))
        return cur.lastrowid


def get_listing_photos(listing_id):
    """Get all photos for a listing, ordered by sort_order."""
    with get_cursor() as cur:
        cur.execute("""
            SELECT * FROM listing_photos
            WHERE listing_id = %s
            ORDER BY sort_order ASC, uploaded_at ASC
        """, (listing_id,))
        return cur.fetchall()


def delete_listing_photo(photo_id, listing_id):
    """Delete a photo. Returns the filename for file cleanup."""
    with get_cursor(commit=True) as cur:
        cur.execute("""
            SELECT filename FROM listing_photos
            WHERE id = %s AND listing_id = %s
        """, (photo_id, listing_id))
        photo = cur.fetchone()
        if photo:
            cur.execute("DELETE FROM listing_photos WHERE id = %s", (photo_id,))
            return photo['filename']
        return None


def count_listing_photos(listing_id):
    """Count photos for a listing."""
    with get_cursor() as cur:
        cur.execute("SELECT COUNT(*) AS cnt FROM listing_photos WHERE listing_id = %s",
                    (listing_id,))
        return cur.fetchone()['cnt']


# ════════════════════════════════════════════════════════════════
# VIEW COUNTER
# ════════════════════════════════════════════════════════════════

def increment_view_count(listing_id):
    """Increment the view count for a listing."""
    with get_cursor(commit=True) as cur:
        cur.execute("UPDATE host_listings SET view_count = view_count + 1 WHERE id = %s",
                    (listing_id,))


# ════════════════════════════════════════════════════════════════
# TRAVELLER SEARCH & BROWSE
# ════════════════════════════════════════════════════════════════

def get_published_listings(page=1, per_page=12, filters=None):
    """Get published listings with optional filters for the browse page."""
    filters = filters or {}
    where = ["hl.status = 'published'"]
    params = []

    if filters.get('district_id'):
        where.append("hl.district_id = %s")
        params.append(filters['district_id'])

    if filters.get('listing_type'):
        where.append("hl.listing_type = %s")
        params.append(filters['listing_type'])

    if filters.get('price_min') is not None:
        where.append("hl.price_per_night >= %s")
        params.append(filters['price_min'])

    if filters.get('price_max') is not None:
        where.append("hl.price_per_night <= %s")
        params.append(filters['price_max'])

    if filters.get('min_guests'):
        where.append("hl.max_guests >= %s")
        params.append(filters['min_guests'])

    if filters.get('verified_only'):
        where.append("hp.is_verified_badge = 1")

    if filters.get('query'):
        q = f"%{filters['query']}%"
        where.append("(hl.title LIKE %s OR hl.description LIKE %s OR d.name LIKE %s)")
        params.extend([q, q, q])

    where_clause = " AND ".join(where)

    with get_cursor() as cur:
        # Count total
        cur.execute(f"""
            SELECT COUNT(*) AS total
            FROM host_listings hl
            JOIN host_profiles hp ON hl.host_id = hp.id
            LEFT JOIN districts d ON hl.district_id = d.id
            WHERE {where_clause}
        """, params)
        total = cur.fetchone()['total']

        # Determine order clause
        order_by = "hl.is_featured DESC"
        sort_opt = filters.get('sort', 'newest')
        if sort_opt == 'price_asc':
            order_by += ", hl.price_per_night ASC, hl.created_at DESC"
        elif sort_opt == 'price_desc':
            order_by += ", hl.price_per_night DESC, hl.created_at DESC"
        elif sort_opt == 'rating':
            order_by += ", hp.avg_host_rating DESC, hl.created_at DESC"
        else:
            order_by += ", hl.created_at DESC"

        # Get page
        offset = (page - 1) * per_page
        cur.execute(f"""
            SELECT hl.*, hp.is_verified_badge, hp.avg_host_rating,
                   u.display_name AS host_name,
                   d.name AS district_name, d.slug AS district_slug
            FROM host_listings hl
            JOIN host_profiles hp ON hl.host_id = hp.id
            JOIN users u ON hp.user_id = u.id
            LEFT JOIN districts d ON hl.district_id = d.id
            WHERE {where_clause}
            ORDER BY {order_by}
            LIMIT %s OFFSET %s
        """, params + [per_page, offset])
        listings = cur.fetchall()

    return listings, total


# ════════════════════════════════════════════════════════════════
# ADMIN LISTING MANAGEMENT
# ════════════════════════════════════════════════════════════════

def admin_get_listings(status=None, listing_type=None, page=1, per_page=20):
    """Admin: get all listings with optional filters."""
    where = ["1=1"]
    params = []

    if status:
        where.append("hl.status = %s")
        params.append(status)
    if listing_type:
        where.append("hl.listing_type = %s")
        params.append(listing_type)

    where_clause = " AND ".join(where)

    with get_cursor() as cur:
        cur.execute(f"""
            SELECT COUNT(*) AS total FROM host_listings hl WHERE {where_clause}
        """, params)
        total = cur.fetchone()['total']

        offset = (page - 1) * per_page
        cur.execute(f"""
            SELECT hl.*,
                   u.display_name AS host_name, u.username AS host_username,
                   d.name AS district_name,
                   hp.is_verified_badge
            FROM host_listings hl
            JOIN host_profiles hp ON hl.host_id = hp.id
            JOIN users u ON hp.user_id = u.id
            LEFT JOIN districts d ON hl.district_id = d.id
            WHERE {where_clause}
            ORDER BY hl.updated_at DESC
            LIMIT %s OFFSET %s
        """, params + [per_page, offset])
        listings = cur.fetchall()

    return listings, total


def admin_count_listings():
    """Admin: count listings by status and type."""
    with get_cursor() as cur:
        cur.execute("""
            SELECT
                COUNT(*) AS total,
                SUM(status = 'draft') AS draft,
                SUM(status = 'submitted') AS submitted,
                SUM(status = 'under_review') AS under_review,
                SUM(status = 'published') AS published,
                SUM(status = 'rejected') AS rejected,
                SUM(status = 'suspended') AS suspended,
                SUM(status = 'archived') AS archived,
                SUM(listing_type = 'free_stay') AS free_stays,
                SUM(listing_type = 'paid_homestay') AS paid_stays
            FROM host_listings
        """)
        return cur.fetchone()


def admin_approve_listing(listing_id, admin_user='admin'):
    """Admin: approve a listing (submitted/under_review → published)."""
    with get_cursor(commit=True) as cur:
        cur.execute("""
            UPDATE host_listings SET status = 'published', rejection_reason = NULL
            WHERE id = %s AND status IN ('submitted', 'under_review')
        """, (listing_id,))
        if cur.rowcount:
            # Notify host
            cur.execute("""
                SELECT hp.user_id, hl.title
                FROM host_listings hl
                JOIN host_profiles hp ON hl.host_id = hp.id
                WHERE hl.id = %s
            """, (listing_id,))
            row = cur.fetchone()
            if row:
                cur.execute("""
                    INSERT INTO notifications (user_id, type, title, message, link)
                    VALUES (%s, 'listing_approved', 'Listing Approved! 🎉',
                            %s, %s)
                """, (row['user_id'],
                      f'Your listing "{row["title"]}" has been approved and is now live!',
                      f'/host/listings'))
            logger.info(f"Listing {listing_id} approved by {admin_user}")
            return True
        return False


def admin_reject_listing(listing_id, reason='', admin_user='admin'):
    """Admin: reject a listing."""
    with get_cursor(commit=True) as cur:
        cur.execute("""
            UPDATE host_listings SET status = 'rejected', rejection_reason = %s
            WHERE id = %s AND status IN ('submitted', 'under_review')
        """, (reason, listing_id))
        if cur.rowcount:
            cur.execute("""
                SELECT hp.user_id, hl.title
                FROM host_listings hl
                JOIN host_profiles hp ON hl.host_id = hp.id
                WHERE hl.id = %s
            """, (listing_id,))
            row = cur.fetchone()
            if row:
                cur.execute("""
                    INSERT INTO notifications (user_id, type, title, message, link)
                    VALUES (%s, 'listing_rejected', 'Listing Needs Changes',
                            %s, %s)
                """, (row['user_id'],
                      f'Your listing "{row["title"]}" needs updates: {reason}',
                      f'/host/listings'))
            logger.info(f"Listing {listing_id} rejected by {admin_user}: {reason}")
            return True
        return False


def admin_suspend_listing(listing_id, reason='', admin_user='admin'):
    """Admin: suspend a published listing."""
    with get_cursor(commit=True) as cur:
        cur.execute("""
            UPDATE host_listings SET status = 'suspended', rejection_reason = %s
            WHERE id = %s AND status = 'published'
        """, (reason, listing_id))
        if cur.rowcount:
            cur.execute("""
                SELECT hp.user_id, hl.title
                FROM host_listings hl
                JOIN host_profiles hp ON hl.host_id = hp.id
                WHERE hl.id = %s
            """, (listing_id,))
            row = cur.fetchone()
            if row:
                cur.execute("""
                    INSERT INTO notifications (user_id, type, title, message, link)
                    VALUES (%s, 'listing_suspended', 'Listing Suspended ⚠️',
                            %s, %s)
                """, (row['user_id'],
                      f'Your listing "{row["title"]}" was suspended: {reason}',
                      f'/host/listings'))
            logger.info(f"Listing {listing_id} suspended by {admin_user}: {reason}")
            return True
        return False


def admin_reinstate_listing(listing_id, admin_user='admin'):
    """Admin: reinstate a suspended listing back to published."""
    with get_cursor(commit=True) as cur:
        cur.execute("""
            UPDATE host_listings SET status = 'published', rejection_reason = NULL
            WHERE id = %s AND status = 'suspended'
        """, (listing_id,))
        if cur.rowcount:
            logger.info(f"Listing {listing_id} reinstated by {admin_user}")
            return True
        return False


# ════════════════════════════════════════════════════════════════
# AMENITIES CATALOG
# ════════════════════════════════════════════════════════════════

AMENITY_OPTIONS = [
    {'key': 'wifi', 'label': 'Wi-Fi', 'icon': '📶'},
    {'key': 'ac', 'label': 'Air Conditioning', 'icon': '❄️'},
    {'key': 'fan', 'label': 'Fan', 'icon': '🌀'},
    {'key': 'hot_water', 'label': 'Hot Water', 'icon': '🚿'},
    {'key': 'kitchen', 'label': 'Kitchen Access', 'icon': '🍳'},
    {'key': 'parking', 'label': 'Parking', 'icon': '🅿️'},
    {'key': 'tv', 'label': 'TV', 'icon': '📺'},
    {'key': 'washing_machine', 'label': 'Washing Machine', 'icon': '🧺'},
    {'key': 'meals', 'label': 'Meals Included', 'icon': '🍽️'},
    {'key': 'local_food', 'label': 'Local Food Available', 'icon': '🥘'},
    {'key': 'pickup', 'label': 'Pickup Service', 'icon': '🚗'},
    {'key': 'guide', 'label': 'Local Guide', 'icon': '🗺️'},
    {'key': 'first_aid', 'label': 'First Aid Kit', 'icon': '🩹'},
    {'key': 'power_backup', 'label': 'Power Backup', 'icon': '🔋'},
    {'key': 'balcony', 'label': 'Balcony / Terrace', 'icon': '🏞️'},
    {'key': 'garden', 'label': 'Garden / Courtyard', 'icon': '🌿'},
    {'key': 'pet_friendly', 'label': 'Pet Friendly', 'icon': '🐾'},
    {'key': 'wheelchair', 'label': 'Wheelchair Accessible', 'icon': '♿'},
]
