"""
HiddenYatra — Stays & Homestays Traveller Discovery Routes
Provides public browsing, filtering, search, and detail views for host listings.
"""
import logging
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, abort

from models.listings import (
    get_published_listings, get_listing_by_slug, get_listing_by_id,
    increment_view_count, get_listing_photos, AMENITY_OPTIONS
)
from models.database import get_all_districts_admin

logger = logging.getLogger(__name__)

stays_bp = Blueprint('stays', __name__)


@stays_bp.route('/stays')
def browse_stays():
    """Public browse & search page for homestays & local stays."""
    page = request.args.get('page', 1, type=int)
    per_page = 12

    # Filter parameters
    district_id = request.args.get('district_id', type=int)
    listing_type = request.args.get('type', '').strip()
    max_price = request.args.get('max_price', type=float)
    min_guests = request.args.get('guests', type=int)
    verified_only = request.args.get('verified', '') in ('1', 'true', 'yes')
    amenity_filter = request.args.get('amenity', '').strip() or None
    query = request.args.get('q', '').strip()
    sort = request.args.get('sort', 'newest').strip()

    filters = {
        'district_id': district_id,
        'listing_type': listing_type if listing_type in ('paid_homestay', 'free_stay') else None,
        'price_max': max_price if max_price and max_price > 0 else None,
        'min_guests': min_guests if min_guests and min_guests > 0 else None,
        'verified_only': verified_only,
        'amenity': amenity_filter,
        'query': query if query else None,
        'sort': sort,
    }

    listings, total = get_published_listings(page=page, per_page=per_page, filters=filters)
    total_pages = max(1, (total + per_page - 1) // per_page)

    districts = get_all_districts_admin()

    return render_template(
        'stays/browse.html',
        listings=listings,
        total=total,
        page=page,
        total_pages=total_pages,
        districts=districts,
        filters=filters,
        amenity_catalog={(a.get('key') or a.get('code')): a for a in AMENITY_OPTIONS}
    )


@stays_bp.route('/stay/<slug>')
def stay_detail_slug(slug):
    """Stay detail page by slug."""
    listing = get_listing_by_slug(slug)

    # Fallback to ID lookup if slug is numeric
    if not listing and slug.isdigit():
        listing = get_listing_by_id(int(slug))

    if not listing:
        abort(404)

    # Check publication status or preview mode for host
    if listing['status'] != 'published':
        user_id = session.get('user_id')
        from models.hosts import get_host_profile_by_user
        host = get_host_profile_by_user(user_id) if user_id else None
        if not host or host['id'] != listing['host_id']:
            abort(404)
        flash('⚠️ You are viewing a private preview of your unpublished listing.', 'info')

    # Increment view count
    increment_view_count(listing['id'])

    photos = get_listing_photos(listing['id'])

    # Build amenity display dict
    amenity_dict = {(a.get('key') or a.get('code')): a for a in AMENITY_OPTIONS}
    listing_amenities = []
    for code in listing.get('amenities_list', []):
        if code in amenity_dict:
            listing_amenities.append(amenity_dict[code])
        else:
            listing_amenities.append({'key': code, 'label': code.replace('_', ' ').title(), 'icon': '✨'})

    return render_template(
        'stays/detail.html',
        listing=listing,
        photos=photos,
        amenities=listing_amenities
    )


# ════════════════════════════════════════════════════════════════
# TRAVELLER STAY REQUEST WORKFLOW
# ════════════════════════════════════════════════════════════════

@stays_bp.route('/stay/<slug>/request', methods=['POST'])
@stays_bp.route('/stay/<int:listing_id>/request', methods=['POST'])
def submit_stay_request(slug=None, listing_id=None):
    """Submit a stay booking request (requires login & CSRF)."""
    if not session.get('user_id'):
        flash('Please login to request a stay.', 'info')
        return redirect(url_for('auth.login', next=request.referrer or url_for('stays.browse_stays')))

    # Manual CSRF verification
    token = request.headers.get('X-CSRF-Token') or request.form.get('_csrf_token', '')
    if not token or token != session.get('_csrf_token'):
        flash('Invalid security token. Please try again.', 'error')
        return redirect(request.referrer or url_for('stays.browse_stays'))

    # Lookup listing
    listing = None
    if listing_id:
        listing = get_listing_by_id(listing_id)
    elif slug:
        listing = get_listing_by_slug(slug)
        if not listing and slug.isdigit():
            listing = get_listing_by_id(int(slug))

    if not listing:
        abort(404)

    check_in = request.form.get('check_in_date') or request.form.get('checkin', '').strip()
    check_out = request.form.get('check_out_date') or request.form.get('checkout', '').strip()
    num_guests = request.form.get('num_guests') or request.form.get('guests_count', 1)
    message = request.form.get('message', '').strip()

    from models.stay_requests import create_stay_request
    success, res = create_stay_request(
        listing_id=listing['id'],
        traveller_id=session['user_id'],
        check_in=check_in,
        check_out=check_out,
        num_guests=num_guests,
        message=message
    )

    if not success:
        flash(f'⚠️ {res}', 'error')
        return redirect(url_for('stays.stay_detail_slug', slug=listing['slug']))

    stay_type_str = "Free Cultural Stay" if listing['listing_type'] == 'free_stay' else f"Stay (Total: ₹{int(res['total_price'])})"
    flash(f"🎉 Your request for {listing['title']} has been sent to the host! ({stay_type_str})", 'success')
    return redirect(url_for('stays.my_stays'))


@stays_bp.route('/my-stays')
@stays_bp.route('/my-bookings')
def my_stays():
    """Traveller dashboard showing their requested and confirmed stays."""
    if not session.get('user_id'):
        flash('Please login to view your stays.', 'info')
        return redirect(url_for('auth.login', next=url_for('stays.my_stays')))

    tab = request.args.get('tab', 'all').strip().lower()
    status_filter = None
    if tab in ('pending', 'accepted', 'rejected', 'completed'):
        status_filter = tab
    elif tab == 'cancelled':
        status_filter = 'cancelled_by_traveller'

    page = request.args.get('page', 1, type=int)
    per_page = 15

    from models.stay_requests import get_traveller_requests
    requests_list, total = get_traveller_requests(
        traveller_id=session['user_id'],
        status=status_filter,
        page=page,
        per_page=per_page
    )

    total_pages = max(1, (total + per_page - 1) // per_page)

    return render_template(
        'user/my_stays.html',
        requests=requests_list,
        total=total,
        page=page,
        total_pages=total_pages,
        active_tab=tab
    )


@stays_bp.route('/my-stays/<int:req_id>')
def stay_request_detail(req_id):
    """View details of a specific stay request."""
    if not session.get('user_id'):
        flash('Please login to continue.', 'info')
        return redirect(url_for('auth.login'))

    from models.stay_requests import get_stay_request_by_id
    req = get_stay_request_by_id(req_id)
    if not req:
        abort(404)

    # IDOR Check: Must be the traveller OR admin
    if req['traveller_id'] != session['user_id'] and not session.get('admin_logged_in'):
        abort(403)

    return render_template('user/stay_request_detail.html', req=req)


@stays_bp.route('/my-stays/<int:req_id>/cancel', methods=['POST'])
def cancel_my_stay(req_id):
    """Traveller cancels their own stay request."""
    if not session.get('user_id'):
        flash('Please login to continue.', 'info')
        return redirect(url_for('auth.login'))

    token = request.headers.get('X-CSRF-Token') or request.form.get('_csrf_token', '')
    if not token or token != session.get('_csrf_token'):
        flash('Invalid security token.', 'error')
        return redirect(url_for('stays.my_stays'))

    reason = request.form.get('cancellation_reason', '').strip()

    from models.stay_requests import cancel_stay_request_by_traveller
    success, err = cancel_stay_request_by_traveller(req_id, session['user_id'], reason)
    if not success:
        flash(f'⚠️ {err}', 'error')
    else:
        flash('Your stay request has been cancelled.', 'info')

    return redirect(url_for('stays.my_stays'))


@stays_bp.route('/api/stay/<int:listing_id>/check-availability')
def api_check_stay_availability(listing_id):
    """Real-time availability and price check for stay request form."""
    listing = get_listing_by_id(listing_id)
    if not listing:
        return {'available': False, 'message': 'Listing not found'}, 404

    check_in = request.args.get('check_in', '').strip()
    check_out = request.args.get('check_out', '').strip()
    guests = request.args.get('guests', 1, type=int)

    from models.stay_requests import validate_booking_parameters, check_date_availability
    is_valid, err, nights, total_price = validate_booking_parameters(listing, check_in, check_out, guests)
    if not is_valid:
        return {'available': False, 'message': err}

    is_avail, avail_msg = check_date_availability(listing_id, check_in, check_out)
    return {
        'available': is_avail,
        'message': avail_msg if not is_avail else 'Available for booking!',
        'nights': nights,
        'price_per_night': float(listing.get('price_per_night', 0)),
        'total_price': total_price,
        'listing_type': listing.get('listing_type')
    }
