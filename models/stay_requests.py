"""
HiddenYatra — Stay Requests & Booking Database Operations
Manages traveller booking requests, date availability, host acceptance/rejection,
cancellations, IDOR protection, conflict prevention, and notifications.
"""
import logging
from datetime import datetime, date, timedelta
from models.connection import get_cursor
from models.hosts import _notify

logger = logging.getLogger(__name__)


# ════════════════════════════════════════════════════════════════
# DATE & PARAMETER VALIDATION HELPERS
# ════════════════════════════════════════════════════════════════

def parse_date(d):
    """Safely parse string YYYY-MM-DD or return date object."""
    if isinstance(d, date):
        return d
    if isinstance(d, datetime):
        return d.date()
    if isinstance(d, str):
        try:
            return datetime.strptime(d.strip(), '%Y-%m-%d').date()
        except ValueError:
            return None
    return None


def validate_booking_parameters(listing, check_in, check_out, num_guests):
    """
    Validates check_in, check_out, stay nights, and guest counts.
    Returns (is_valid: bool, error_msg: str, nights: int, total_price: float)
    """
    d_in = parse_date(check_in)
    d_out = parse_date(check_out)

    if not d_in:
        return False, "Please select a valid check-in date.", 0, 0.0
    if not d_out:
        return False, "Please select a valid check-out date.", 0, 0.0

    today = date.today()
    if d_in < today:
        return False, "Check-in date cannot be in the past.", 0, 0.0

    if d_out <= d_in:
        return False, "Check-out date must be after check-in date.", 0, 0.0

    nights = (d_out - d_in).days
    if nights <= 0:
        return False, "Stay duration must be at least 1 night.", 0, 0.0

    min_nights = listing.get('min_stay_nights') or 1
    if nights < min_nights:
        return False, f"Minimum stay is {min_nights} night(s).", 0, 0.0

    max_nights = listing.get('max_stay_nights') or 0
    if max_nights > 0 and nights > max_nights:
        return False, f"Maximum stay allowed is {max_nights} night(s).", 0, 0.0

    max_guests = listing.get('max_guests') or 2
    try:
        guests = int(num_guests)
    except (ValueError, TypeError):
        guests = 1

    if guests < 1:
        return False, "Number of guests must be at least 1.", 0, 0.0
    if guests > max_guests:
        return False, f"This stay accommodates up to {max_guests} guest(s).", 0, 0.0

    # Calculate Total Price
    listing_type = listing.get('listing_type', 'paid_homestay')
    if listing_type == 'free_stay':
        total_price = 0.0
    else:
        price_per_night = float(listing.get('price_per_night', 0))
        total_price = round(price_per_night * nights, 2)

    return True, "", nights, total_price


def check_date_availability(listing_id, check_in, check_out, exclude_request_id=None):
    """
    Checks if a listing has overlapping ACCEPTED or CONFIRMED bookings
    or blocked dates in listing_availability.
    Returns (is_available: bool, message: str)
    """
    d_in = parse_date(check_in)
    d_out = parse_date(check_out)
    if not d_in or not d_out:
        return False, "Invalid dates provided."

    with get_cursor() as cur:
        # Check overlapping accepted / confirmed requests
        exclude_sql = "AND id != %s" if exclude_request_id else ""
        params = [listing_id, d_in, d_out]
        if exclude_request_id:
            params.append(exclude_request_id)

        cur.execute(f"""
            SELECT id, check_in_date, check_out_date, status
            FROM stay_requests
            WHERE listing_id = %s
              AND status IN ('accepted', 'confirmed')
              AND check_in_date < %s
              AND check_out_date > %s
              {exclude_sql}
            LIMIT 1
        """, params)
        overlap = cur.fetchone()
        if overlap:
            return False, f"These dates overlap with an already confirmed booking ({overlap['check_in_date']} to {overlap['check_out_date']})."

        # Check explicit blackout dates in listing_availability
        cur.execute("""
            SELECT date, notes FROM listing_availability
            WHERE listing_id = %s
              AND date >= %s
              AND date < %s
              AND is_available = 0
            LIMIT 1
        """, (listing_id, d_in, d_out))
        blocked = cur.fetchone()
        if blocked:
            return False, f"The date {blocked['date']} is marked unavailable by the host."

    return True, "Dates are available."


# ════════════════════════════════════════════════════════════════
# STAY REQUEST CREATION & RETRIEVAL
# ════════════════════════════════════════════════════════════════

def create_stay_request(listing_id, traveller_id, check_in, check_out, num_guests, message=''):
    """
    Submits a new stay request for a listing.
    Returns (success: bool, result_or_error: dict|str)
    """
    from models.listings import get_listing_by_id
    from models.hosts import get_host_profile_by_id

    listing = get_listing_by_id(listing_id)
    if not listing:
        return False, "Stay listing not found."

    if listing.get('status') != 'published':
        return False, "This stay is currently not accepting requests."

    host = get_host_profile_by_id(listing['host_id'])
    if not host:
        return False, "Host profile not found."

    # Prevent self-booking
    if host.get('user_id') == traveller_id:
        return False, "Hosts cannot book their own listings."

    is_valid, err, nights, total_price = validate_booking_parameters(listing, check_in, check_out, num_guests)
    if not is_valid:
        return False, err

    d_in = parse_date(check_in)
    d_out = parse_date(check_out)

    # Check date availability (no overlapping accepted bookings)
    is_avail, avail_msg = check_date_availability(listing_id, d_in, d_out)
    if not is_avail:
        return False, avail_msg

    with get_cursor(commit=True) as cur:
        cur.execute("""
            INSERT INTO stay_requests
                (listing_id, traveller_id, host_id,
                 check_in_date, check_out_date, num_guests,
                 total_price, message, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pending')
        """, (listing_id, traveller_id, listing['host_id'],
              d_in, d_out, int(num_guests),
              total_price, message.strip()))
        request_id = cur.lastrowid

        # Notify Host
        host_user_id = host['user_id']
        stay_type_lbl = "Free Stay" if listing.get('listing_type') == 'free_stay' else f"Stay (₹{int(total_price)})"
        _notify(
            cur,
            user_id=host_user_id,
            notif_type='stay_request_received',
            title='New Stay Request Received! 📩',
            message=f"A traveller requested {listing['title']} for {nights} night(s) ({d_in} to {d_out}). Type: {stay_type_lbl}.",
            link=f'/host/requests'
        )

        logger.info(f"Created stay_request {request_id} for listing {listing_id} by traveller {traveller_id}")
        return True, {'request_id': request_id, 'total_price': total_price, 'nights': nights}


def get_stay_request_by_id(request_id):
    """
    Get full stay request details joined with listing, host, and traveller info.
    """
    with get_cursor() as cur:
        cur.execute("""
            SELECT sr.*,
                   hl.title AS listing_title, hl.slug AS listing_slug,
                   hl.listing_type, hl.price_per_night, hl.cover_image,
                   hl.address_text, hl.address_full, hl.check_in_time, hl.check_out_time,
                   hl.house_rules, hl.cancellation_policy,
                   d.name AS district_name,
                   -- Host user details
                   hu.id AS host_user_id, hu.username AS host_username,
                   hu.display_name AS host_display_name, hu.full_name AS host_full_name,
                   hu.email AS host_email, hu.phone AS host_phone,
                   hp.profile_photo AS host_photo, hp.is_verified_badge AS host_verified,
                   -- Traveller user details
                   tu.username AS traveller_username, tu.display_name AS traveller_display_name,
                   tu.full_name AS traveller_full_name, tu.email AS traveller_email,
                   tu.phone AS traveller_phone, tu.avatar_emoji AS traveller_avatar
            FROM stay_requests sr
            JOIN host_listings hl ON hl.id = sr.listing_id
            LEFT JOIN districts d ON d.id = hl.district_id
            JOIN host_profiles hp ON hp.id = sr.host_id
            JOIN users hu ON hu.id = hp.user_id
            JOIN users tu ON tu.id = sr.traveller_id
            WHERE sr.id = %s
        """, (request_id,))
        row = cur.fetchone()
        if row:
            d_in = row['check_in_date']
            d_out = row['check_out_date']
            if d_in and d_out:
                row['nights'] = (d_out - d_in).days
            else:
                row['nights'] = 1
        return row


def get_traveller_requests(traveller_id, status=None, page=1, per_page=20):
    """
    Fetch all stay requests created by a specific traveller with pagination.
    """
    offset = (page - 1) * per_page
    where = "WHERE sr.traveller_id = %s"
    params = [traveller_id]
    if status:
        where += " AND sr.status = %s"
        params.append(status)

    with get_cursor() as cur:
        cur.execute(f"""
            SELECT sr.*,
                   hl.title AS listing_title, hl.slug AS listing_slug,
                   hl.listing_type, hl.cover_image, hl.address_text,
                   d.name AS district_name,
                   hu.display_name AS host_display_name, hu.full_name AS host_full_name,
                   hu.phone AS host_phone, hu.email AS host_email,
                   hp.is_verified_badge AS host_verified
            FROM stay_requests sr
            JOIN host_listings hl ON hl.id = sr.listing_id
            LEFT JOIN districts d ON d.id = hl.district_id
            JOIN host_profiles hp ON hp.id = sr.host_id
            JOIN users hu ON hu.id = hp.user_id
            {where}
            ORDER BY sr.created_at DESC
            LIMIT %s OFFSET %s
        """, params + [per_page, offset])
        rows = cur.fetchall()
        for r in rows:
            if r.get('check_in_date') and r.get('check_out_date'):
                r['nights'] = (r['check_out_date'] - r['check_in_date']).days
            else:
                r['nights'] = 1

        cur.execute(f"SELECT COUNT(*) AS cnt FROM stay_requests sr {where}", params)
        total = cur.fetchone()['cnt']
        return rows, total


def get_host_requests(host_id, status=None, page=1, per_page=20):
    """
    Fetch all incoming stay requests for a host's listings with pagination.
    """
    offset = (page - 1) * per_page
    where = "WHERE sr.host_id = %s"
    params = [host_id]
    if status:
        where += " AND sr.status = %s"
        params.append(status)

    with get_cursor() as cur:
        cur.execute(f"""
            SELECT sr.*,
                   hl.title AS listing_title, hl.slug AS listing_slug,
                   hl.listing_type, hl.cover_image, hl.price_per_night,
                   tu.display_name AS traveller_display_name,
                   tu.full_name AS traveller_full_name,
                   tu.avatar_emoji AS traveller_avatar,
                   tu.phone AS traveller_phone, tu.email AS traveller_email
            FROM stay_requests sr
            JOIN host_listings hl ON hl.id = sr.listing_id
            JOIN users tu ON tu.id = sr.traveller_id
            {where}
            ORDER BY sr.created_at DESC
            LIMIT %s OFFSET %s
        """, params + [per_page, offset])
        rows = cur.fetchall()
        for r in rows:
            if r.get('check_in_date') and r.get('check_out_date'):
                r['nights'] = (r['check_out_date'] - r['check_in_date']).days
            else:
                r['nights'] = 1

        cur.execute(f"SELECT COUNT(*) AS cnt FROM stay_requests sr {where}", params)
        total = cur.fetchone()['cnt']
        return rows, total


def count_host_requests_by_status(host_id):
    """Return dict of counts grouped by status for host."""
    with get_cursor() as cur:
        cur.execute("""
            SELECT status, COUNT(*) AS cnt
            FROM stay_requests
            WHERE host_id = %s
            GROUP BY status
        """, (host_id,))
        result = {r['status']: r['cnt'] for r in cur.fetchall()}
        result['pending'] = result.get('pending', 0)
        result['accepted'] = result.get('accepted', 0)
        result['total'] = sum(result.values())
        return result


# ════════════════════════════════════════════════════════════════
# HOST ACTIONS (ACCEPT, REJECT, CANCEL)
# ════════════════════════════════════════════════════════════════

def accept_stay_request(request_id, host_id, host_message=''):
    """
    Host accepts a pending stay request.
    Verifies IDOR, validates overlapping bookings, updates status to 'accepted',
    and blocks dates in listing_availability.
    Returns (success: bool, error_msg: str)
    """
    req = get_stay_request_by_id(request_id)
    if not req:
        return False, "Stay request not found."

    # IDOR Check: Must belong to this host
    if req['host_id'] != host_id:
        return False, "Unauthorized: You do not own this listing."

    if req['status'] != 'pending':
        return False, f"Cannot accept request with status '{req['status']}'."

    # Overlap Check
    d_in = req['check_in_date']
    d_out = req['check_out_date']
    is_avail, avail_msg = check_date_availability(req['listing_id'], d_in, d_out, exclude_request_id=request_id)
    if not is_avail:
        return False, f"Cannot accept: {avail_msg}"

    with get_cursor(commit=True) as cur:
        cur.execute("""
            UPDATE stay_requests
            SET status = 'accepted',
                host_response = %s,
                responded_at = NOW()
            WHERE id = %s
        """, (host_message.strip(), request_id))

        # Block dates in listing_availability
        curr_d = d_in
        while curr_d < d_out:
            cur.execute("""
                INSERT INTO listing_availability (listing_id, date, is_available, notes)
                VALUES (%s, %s, 0, %s)
                ON DUPLICATE KEY UPDATE is_available = 0, notes = VALUES(notes)
            """, (req['listing_id'], curr_d, f"Booked by Stay Request #{request_id}"))
            curr_d += timedelta(days=1)

        # Notify Traveller
        _notify(
            cur,
            user_id=req['traveller_id'],
            notif_type='stay_request_accepted',
            title='Stay Request Accepted! 🎉',
            message=f"Your host accepted your request for {req['listing_title']} ({d_in} to {d_out}). Contact details are now available.",
            link=f'/my-stays'
        )

        logger.info(f"Host {host_id} accepted stay_request {request_id}")
        return True, ""


def reject_stay_request(request_id, host_id, rejection_reason='', host_message=''):
    """
    Host rejects a pending stay request.
    Verifies IDOR and records rejection reason.
    Returns (success: bool, error_msg: str)
    """
    req = get_stay_request_by_id(request_id)
    if not req:
        return False, "Stay request not found."

    # IDOR Check
    if req['host_id'] != host_id:
        return False, "Unauthorized: You do not own this listing."

    if req['status'] != 'pending':
        return False, f"Cannot reject request with status '{req['status']}'."

    with get_cursor(commit=True) as cur:
        cur.execute("""
            UPDATE stay_requests
            SET status = 'rejected',
                host_response = %s,
                cancellation_reason = %s,
                responded_at = NOW()
            WHERE id = %s
        """, (host_message.strip(), rejection_reason.strip(), request_id))

        # Notify Traveller
        _notify(
            cur,
            user_id=req['traveller_id'],
            notif_type='stay_request_rejected',
            title='Stay Request Update',
            message=f"Your request for {req['listing_title']} ({req['check_in_date']} to {req['check_out_date']}) was declined by the host.",
            link=f'/my-stays'
        )

        logger.info(f"Host {host_id} rejected stay_request {request_id}")
        return True, ""


def cancel_stay_request_by_host(request_id, host_id, cancellation_reason=''):
    """
    Host cancels an already accepted stay request.
    Releases blocked calendar dates.
    Returns (success: bool, error_msg: str)
    """
    req = get_stay_request_by_id(request_id)
    if not req:
        return False, "Stay request not found."

    # IDOR Check
    if req['host_id'] != host_id:
        return False, "Unauthorized: You do not own this listing."

    if req['status'] not in ('accepted', 'confirmed'):
        return False, f"Cannot cancel request with status '{req['status']}'."

    with get_cursor(commit=True) as cur:
        cur.execute("""
            UPDATE stay_requests
            SET status = 'cancelled_by_host',
                cancellation_reason = %s,
                cancelled_at = NOW()
            WHERE id = %s
        """, (cancellation_reason.strip(), request_id))

        # Release blocked calendar dates
        d_in = req['check_in_date']
        d_out = req['check_out_date']
        cur.execute("""
            DELETE FROM listing_availability
            WHERE listing_id = %s
              AND date >= %s
              AND date < %s
              AND notes LIKE %s
        """, (req['listing_id'], d_in, d_out, f"%#{request_id}%"))

        # Notify Traveller
        _notify(
            cur,
            user_id=req['traveller_id'],
            notif_type='stay_cancelled_by_host',
            title='Stay Reservation Cancelled by Host ⚠️',
            message=f"The host cancelled your booking for {req['listing_title']} ({d_in} to {d_out}). Reason: {cancellation_reason or 'None provided'}.",
            link=f'/my-stays'
        )

        logger.info(f"Host {host_id} cancelled stay_request {request_id}")
        return True, ""


# ════════════════════════════════════════════════════════════════
# TRAVELLER ACTIONS (CANCEL)
# ════════════════════════════════════════════════════════════════

def cancel_stay_request_by_traveller(request_id, traveller_id, cancellation_reason=''):
    """
    Traveller cancels their own stay request (pending or accepted).
    Releases blocked dates if it was accepted.
    Returns (success: bool, error_msg: str)
    """
    req = get_stay_request_by_id(request_id)
    if not req:
        return False, "Stay request not found."

    # IDOR Check
    if req['traveller_id'] != traveller_id:
        return False, "Unauthorized: You do not own this stay request."

    if req['status'] not in ('pending', 'accepted', 'confirmed'):
        return False, f"Cannot cancel request with status '{req['status']}'."

    was_accepted = req['status'] in ('accepted', 'confirmed')

    with get_cursor(commit=True) as cur:
        cur.execute("""
            UPDATE stay_requests
            SET status = 'cancelled_by_traveller',
                cancellation_reason = %s,
                cancelled_at = NOW()
            WHERE id = %s
        """, (cancellation_reason.strip(), request_id))

        # If it was accepted, release availability dates
        if was_accepted:
            d_in = req['check_in_date']
            d_out = req['check_out_date']
            cur.execute("""
                DELETE FROM listing_availability
                WHERE listing_id = %s
                  AND date >= %s
                  AND date < %s
                  AND notes LIKE %s
            """, (req['listing_id'], d_in, d_out, f"%#{request_id}%"))

        # Notify Host
        _notify(
            cur,
            user_id=req['host_user_id'],
            notif_type='stay_request_cancelled',
            title='Stay Request Cancelled by Guest',
            message=f"Guest {req['traveller_display_name']} cancelled their request for {req['listing_title']} ({req['check_in_date']} to {req['check_out_date']}).",
            link=f'/host/requests'
        )

        logger.info(f"Traveller {traveller_id} cancelled stay_request {request_id}")
        return True, ""


# ════════════════════════════════════════════════════════════════
# ADMIN MANAGEMENT
# ════════════════════════════════════════════════════════════════

def get_all_stay_requests_admin(status=None, listing_id=None, page=1, per_page=20):
    """
    Admin overview of all stay requests on HiddenYatra with pagination.
    """
    offset = (page - 1) * per_page
    where_clauses = []
    params = []

    if status:
        where_clauses.append("sr.status = %s")
        params.append(status)
    if listing_id:
        where_clauses.append("sr.listing_id = %s")
        params.append(listing_id)

    where = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""

    with get_cursor() as cur:
        cur.execute(f"""
            SELECT sr.*,
                   hl.title AS listing_title, hl.slug AS listing_slug, hl.listing_type,
                   d.name AS district_name,
                   hu.display_name AS host_display_name, hu.email AS host_email,
                   tu.display_name AS traveller_display_name, tu.email AS traveller_email
            FROM stay_requests sr
            JOIN host_listings hl ON hl.id = sr.listing_id
            LEFT JOIN districts d ON d.id = hl.district_id
            JOIN host_profiles hp ON hp.id = sr.host_id
            JOIN users hu ON hu.id = hp.user_id
            JOIN users tu ON tu.id = sr.traveller_id
            {where}
            ORDER BY sr.created_at DESC
            LIMIT %s OFFSET %s
        """, params + [per_page, offset])
        rows = cur.fetchall()
        for r in rows:
            if r.get('check_in_date') and r.get('check_out_date'):
                r['nights'] = (r['check_out_date'] - r['check_in_date']).days
            else:
                r['nights'] = 1

        cur.execute(f"SELECT COUNT(*) AS cnt FROM stay_requests sr {where}", params)
        total = cur.fetchone()['cnt']
        return rows, total


def admin_cancel_stay_request(request_id, reason='', admin_user='admin'):
    """
    Admin moderation cancellation of a stay request.
    """
    req = get_stay_request_by_id(request_id)
    if not req:
        return False, "Stay request not found."

    with get_cursor(commit=True) as cur:
        cur.execute("""
            UPDATE stay_requests
            SET status = 'cancelled_by_host',
                cancellation_reason = %s,
                cancelled_at = NOW()
            WHERE id = %s
        """, (f"[Admin: {admin_user}] {reason}".strip(), request_id))

        # Release blocked dates
        d_in = req['check_in_date']
        d_out = req['check_out_date']
        cur.execute("""
            DELETE FROM listing_availability
            WHERE listing_id = %s
              AND date >= %s
              AND date < %s
              AND notes LIKE %s
        """, (req['listing_id'], d_in, d_out, f"%#{request_id}%"))

        # Notify both parties
        _notify(cur, req['traveller_id'], 'stay_cancelled_admin',
                'Stay Reservation Cancelled by Admin',
                f"Your booking for {req['listing_title']} was cancelled by moderation. Reason: {reason}",
                '/my-stays')
        _notify(cur, req['host_user_id'], 'stay_cancelled_admin',
                'Stay Reservation Cancelled by Admin',
                f"Booking #{request_id} for {req['listing_title']} was cancelled by moderation. Reason: {reason}",
                '/host/requests')
        return True, ""
