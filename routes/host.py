"""Host routes — Registration, dashboard, profile management."""
import os
import uuid
import logging
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, session, jsonify
)
from werkzeug.utils import secure_filename
from PIL import Image
from config import BASE_DIR, allowed_file, validate_image_file, check_file_size
from utils import csrf_required, login_required

logger = logging.getLogger(__name__)

host_bp = Blueprint('host', __name__)

HOST_UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads', 'hosts', 'profiles')
HOST_ID_UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads', 'hosts', 'id_docs')

# Ensure upload dirs exist
os.makedirs(HOST_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(HOST_ID_UPLOAD_FOLDER, exist_ok=True)


def _host_required(f):
    """Decorator: require user to be an approved host."""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please login to continue.', 'error')
            return redirect(url_for('auth.login'))
        from models.hosts import get_host_profile_by_user
        host = get_host_profile_by_user(session['user_id'])
        if not host or host['verification_status'] != 'approved':
            flash('You need an approved host profile to access this page.', 'error')
            return redirect(url_for('host.become_host'))
        return f(*args, **kwargs)
    return decorated


# ════════════════════════════════════════════════════════════════
# HOST REGISTRATION
# ════════════════════════════════════════════════════════════════

@host_bp.route('/host/become')
@login_required
def become_host():
    """Show host registration page."""
    from models.hosts import get_host_profile_by_user
    from models.database import get_all_districts_admin

    host = get_host_profile_by_user(session['user_id'])

    # If already a host, redirect to dashboard or show status
    if host and host['verification_status'] == 'approved':
        return redirect(url_for('host.dashboard'))

    districts = get_all_districts_admin()
    return render_template('host/become_host.html',
                           host=host,
                           districts=districts)


@host_bp.route('/host/register', methods=['POST'])
@login_required
@csrf_required
def register_host():
    """Process host registration form."""
    from models.hosts import create_host_profile, get_host_profile_by_user
    from models.database import log_admin_action

    user_id = session['user_id']

    # Check if already registered
    existing = get_host_profile_by_user(user_id)
    if existing and existing['verification_status'] not in ('rejected',):
        flash('You already have a host application.', 'info')
        return redirect(url_for('host.become_host'))

    # Validate required fields
    bio = request.form.get('bio', '').strip()
    languages = request.form.get('languages', 'Hindi').strip()
    address_line = request.form.get('address_line', '').strip()
    district_id = request.form.get('district_id', type=int)
    block_id = request.form.get('block_id', type=int) or None
    pin_code = request.form.get('pin_code', '').strip()
    id_type = request.form.get('id_type', '').strip()
    id_number = request.form.get('id_number', '').strip()
    emergency_name = request.form.get('emergency_name', '').strip()
    emergency_phone = request.form.get('emergency_phone', '').strip()
    latitude = request.form.get('latitude', type=float)
    longitude = request.form.get('longitude', type=float)

    errors = []
    if not bio or len(bio) < 20:
        errors.append('Please write a bio (at least 20 characters).')
    if not address_line:
        errors.append('Address is required.')
    if not district_id:
        errors.append('Please select your district.')
    if not pin_code or len(pin_code) != 6 or not pin_code.isdigit():
        errors.append('Valid 6-digit PIN code is required.')
    if not id_type:
        errors.append('Please select your ID type.')
    if not id_number or len(id_number) < 4:
        errors.append('Valid ID number is required.')
    if not emergency_name:
        errors.append('Emergency contact name is required.')
    if not emergency_phone or len(emergency_phone) < 10:
        errors.append('Valid emergency contact phone is required.')

    # Handle profile photo upload
    profile_photo = ''
    photo_file = request.files.get('profile_photo')
    if photo_file and photo_file.filename:
        if not allowed_file(photo_file.filename):
            errors.append('Profile photo must be JPG, PNG, or WebP.')
        elif not validate_image_file(photo_file):
            errors.append('Invalid image file.')
        elif not check_file_size(photo_file):
            errors.append('Profile photo must be under 5 MB.')
        else:
            ext = photo_file.filename.rsplit('.', 1)[1].lower()
            filename = f"host_{user_id}_{uuid.uuid4().hex[:8]}.{ext}"
            filepath = os.path.join(HOST_UPLOAD_FOLDER, filename)
            photo_file.save(filepath)
            # Resize to max 500x500
            try:
                img = Image.open(filepath)
                img.thumbnail((500, 500), Image.LANCZOS)
                img.save(filepath, quality=85, optimize=True)
            except Exception:
                pass
            profile_photo = filename

    if errors:
        for e in errors:
            flash(e, 'error')
        return redirect(url_for('host.become_host'))

    # If reapplying after rejection, delete old profile first
    if existing and existing['verification_status'] == 'rejected':
        from models.connection import get_cursor
        with get_cursor(commit=True) as cur:
            cur.execute("DELETE FROM host_profiles WHERE id = %s", (existing['id'],))

    host_id = create_host_profile(
        user_id=user_id,
        bio=bio,
        languages=languages,
        address_line=address_line,
        district_id=district_id,
        block_id=block_id,
        pin_code=pin_code,
        profile_photo=profile_photo,
        id_type=id_type,
        id_number=id_number,
        emergency_name=emergency_name,
        emergency_phone=emergency_phone,
        latitude=latitude,
        longitude=longitude
    )

    if host_id:
        log_admin_action(f'host_application_submitted', 'host_profile', host_id,
                         f'User {user_id} submitted host application', admin_user=f'user:{user_id}')
        flash('Your host application has been submitted! We will review it soon.', 'success')
    else:
        flash('Failed to submit application. Please try again.', 'error')

    return redirect(url_for('host.become_host'))


# ════════════════════════════════════════════════════════════════
# HOST DASHBOARD
# ════════════════════════════════════════════════════════════════

@host_bp.route('/host/dashboard')
@login_required
def dashboard():
    """Host dashboard — overview of listings, requests, stats."""
    from models.hosts import get_host_profile_by_user

    host = get_host_profile_by_user(session['user_id'])
    if not host:
        return redirect(url_for('host.become_host'))

    if host['verification_status'] != 'approved':
        return render_template('host/become_host.html', host=host, districts=[])

    # Get host stats
    from models.connection import get_cursor
    with get_cursor() as cur:
        cur.execute("""
            SELECT COUNT(*) AS total,
                   SUM(status = 'published') AS published,
                   SUM(status = 'draft') AS drafts,
                   SUM(status = 'submitted') AS submitted
            FROM host_listings WHERE host_id = %s
        """, (host['id'],))
        listing_stats = cur.fetchone()

        cur.execute("""
            SELECT COUNT(*) AS total,
                   SUM(status = 'pending') AS pending,
                   SUM(status = 'accepted') AS accepted,
                   SUM(status = 'completed') AS completed
            FROM stay_requests WHERE host_id = %s
        """, (host['id'],))
        request_stats = cur.fetchone()

    return render_template('host/dashboard.html',
                           host=host,
                           listing_stats=listing_stats,
                           request_stats=request_stats)


# ════════════════════════════════════════════════════════════════
# HOST PROFILE EDIT
# ════════════════════════════════════════════════════════════════

@host_bp.route('/host/profile/edit')
@login_required
def profile_edit():
    """Edit host profile page."""
    from models.hosts import get_host_profile_by_user
    from models.database import get_all_districts_admin

    host = get_host_profile_by_user(session['user_id'])
    if not host:
        return redirect(url_for('host.become_host'))

    districts = get_all_districts_admin()
    return render_template('host/profile_edit.html',
                           host=host, districts=districts)


@host_bp.route('/host/profile/update', methods=['POST'])
@login_required
@csrf_required
def profile_update():
    """Update host profile."""
    from models.hosts import get_host_profile_by_user, update_host_profile

    host = get_host_profile_by_user(session['user_id'])
    if not host:
        flash('Host profile not found.', 'error')
        return redirect(url_for('host.become_host'))

    updates = {}
    for field in ('bio', 'languages', 'address_line', 'pin_code',
                  'emergency_name', 'emergency_phone'):
        val = request.form.get(field, '').strip()
        if val:
            updates[field] = val

    district_id = request.form.get('district_id', type=int)
    if district_id:
        updates['district_id'] = district_id

    block_id = request.form.get('block_id', type=int)
    updates['block_id'] = block_id or None

    # Handle profile photo update
    photo_file = request.files.get('profile_photo')
    if photo_file and photo_file.filename:
        if allowed_file(photo_file.filename) and validate_image_file(photo_file) and check_file_size(photo_file):
            ext = photo_file.filename.rsplit('.', 1)[1].lower()
            filename = f"host_{session['user_id']}_{uuid.uuid4().hex[:8]}.{ext}"
            filepath = os.path.join(HOST_UPLOAD_FOLDER, filename)
            photo_file.save(filepath)
            try:
                img = Image.open(filepath)
                img.thumbnail((500, 500), Image.LANCZOS)
                img.save(filepath, quality=85, optimize=True)
            except Exception:
                pass
            updates['profile_photo'] = filename

    update_host_profile(host['id'], **updates)
    flash('Profile updated successfully.', 'success')
    return redirect(url_for('host.profile_edit'))


# ════════════════════════════════════════════════════════════════
# NOTIFICATIONS API
# ════════════════════════════════════════════════════════════════

@host_bp.route('/api/notifications')
@login_required
def api_notifications():
    """Get notifications for current user."""
    from models.hosts import get_notifications, count_unread_notifications
    user_id = session['user_id']
    notifs = get_notifications(user_id, limit=20)
    unread = count_unread_notifications(user_id)
    return jsonify({
        'notifications': [{
            'id': n['id'],
            'type': n['type'],
            'title': n['title'],
            'message': n['message'],
            'link': n['link'],
            'is_read': n['is_read'],
            'created_at': n['created_at'].isoformat() if n['created_at'] else None,
        } for n in notifs],
        'unread_count': unread
    })


@host_bp.route('/api/notifications/read', methods=['POST'])
@login_required
@csrf_required
def api_notifications_read():
    """Mark notifications as read."""
    from models.hosts import mark_notifications_read
    user_id = session['user_id']
    data = request.get_json(silent=True) or {}
    ids = data.get('ids')
    mark_notifications_read(user_id, ids)
    return jsonify({'ok': True})


# ════════════════════════════════════════════════════════════════
# PHASE 3.2: LISTING MANAGEMENT
# ════════════════════════════════════════════════════════════════

LISTING_UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads', 'hosts', 'listings')
os.makedirs(LISTING_UPLOAD_FOLDER, exist_ok=True)

MAX_LISTING_PHOTOS = 10


def _save_listing_image(file_obj, listing_id):
    """Save and resize a listing image. Returns filename."""
    if not file_obj or not allowed_file(file_obj.filename):
        return None
    if not check_file_size(file_obj, max_mb=5):
        return None

    from utils.image import compress_image_to_webp
    fname = compress_image_to_webp(file_obj, LISTING_UPLOAD_FOLDER, prefix=f"listing_{listing_id}", max_width=1400, quality=82)
    if fname:
        return fname

    ext = file_obj.filename.rsplit('.', 1)[-1].lower()
    filename = f"listing_{listing_id}_{uuid.uuid4().hex[:10]}.{ext}"
    filepath = os.path.join(LISTING_UPLOAD_FOLDER, filename)

    try:
        img = Image.open(file_obj)
        img = img.convert('RGB') if img.mode != 'RGB' else img
        # Resize to max 1200px wide
        if img.width > 1200:
            ratio = 1200 / img.width
            img = img.resize((1200, int(img.height * ratio)), Image.LANCZOS)
        img.save(filepath, quality=85, optimize=True)
        return filename
    except Exception as e:
        logger.error(f"Image save error: {e}")
        return None


@host_bp.route('/host/listings')
@login_required
@_host_required
def my_listings():
    """Host's listings management page."""
    from models.hosts import get_host_profile_by_user
    from models.listings import get_listings_by_host

    host = get_host_profile_by_user(session['user_id'])
    status_filter = request.args.get('status', '')
    listings = get_listings_by_host(
        host['id'],
        status=status_filter if status_filter else None
    )

    return render_template('host/my_listings.html',
                           host=host, listings=listings,
                           current_filter=status_filter)


@host_bp.route('/host/listing/new')
@login_required
@_host_required
def listing_new():
    """Create new listing form."""
    from models.hosts import get_host_profile_by_user
    from models.database import get_all_districts_admin
    from models.listings import AMENITY_OPTIONS

    host = get_host_profile_by_user(session['user_id'])
    districts = get_all_districts_admin()

    return render_template('host/listing_form.html',
                           host=host, listing=None,
                           districts=districts,
                           amenity_options=AMENITY_OPTIONS,
                           is_edit=False)


@host_bp.route('/host/listing/create', methods=['POST'])
@login_required
@_host_required
@csrf_required
def listing_create():
    """Create a new listing."""
    from models.hosts import get_host_profile_by_user
    from models.listings import create_listing

    host = get_host_profile_by_user(session['user_id'])

    listing_type = request.form.get('listing_type', 'paid_homestay')
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()

    if not title or len(title) < 5:
        flash('Listing title must be at least 5 characters.', 'error')
        return redirect(url_for('host.listing_new'))
    if not description or len(description) < 20:
        flash('Description must be at least 20 characters.', 'error')
        return redirect(url_for('host.listing_new'))

    # Parse numeric fields safely
    def _int(key, default=0):
        try:
            return int(request.form.get(key, default))
        except (ValueError, TypeError):
            return default

    def _float(key, default=0.0):
        try:
            return float(request.form.get(key, default))
        except (ValueError, TypeError):
            return default

    price = _float('price_per_night', 0) if listing_type != 'free_stay' else 0
    amenities = request.form.getlist('amenities')

    listing_id = create_listing(
        host_id=host['id'],
        listing_type=listing_type,
        title=title,
        description=description,
        district_id=_int('district_id') or None,
        address_text=request.form.get('address_text', '').strip(),
        address_full=request.form.get('address_full', '').strip(),
        price_per_night=price,
        max_guests=max(1, _int('max_guests', 2)),
        min_stay_nights=max(1, _int('min_stay_nights', 1)),
        max_stay_nights=max(0, _int('max_stay_nights', 0)),
        num_rooms=max(1, _int('num_rooms', 1)),
        num_beds=max(1, _int('num_beds', 1)),
        num_bathrooms=max(0, _int('num_bathrooms', 1)),
        property_type=request.form.get('property_type', 'room'),
        amenities=amenities if amenities else None,
        house_rules=request.form.get('house_rules', '').strip(),
        check_in_time=request.form.get('check_in_time', '14:00'),
        check_out_time=request.form.get('check_out_time', '11:00'),
        cancellation_policy=request.form.get('cancellation_policy', 'flexible'),
    )

    if listing_id:
        flash('✅ Listing created as draft! Add photos and submit for review.', 'success')
        return redirect(url_for('host.listing_edit', listing_id=listing_id))

    flash('Error creating listing. Please try again.', 'error')
    return redirect(url_for('host.listing_new'))


@host_bp.route('/host/listing/<int:listing_id>/edit')
@login_required
@_host_required
def listing_edit(listing_id):
    """Edit listing form."""
    from models.hosts import get_host_profile_by_user
    from models.listings import get_listing_by_id, get_listing_photos, AMENITY_OPTIONS
    from models.database import get_all_districts_admin

    host = get_host_profile_by_user(session['user_id'])
    listing = get_listing_by_id(listing_id)

    if not listing or listing['host_id'] != host['id']:
        flash('Listing not found.', 'error')
        return redirect(url_for('host.my_listings'))

    if listing['status'] not in ('draft', 'rejected'):
        flash('Only draft or rejected listings can be edited.', 'info')
        return redirect(url_for('host.my_listings'))

    photos = get_listing_photos(listing_id)
    districts = get_all_districts_admin()

    # Parse amenities from JSON
    amenities_selected = listing.get('amenities_list', [])

    return render_template('host/listing_form.html',
                           host=host, listing=listing,
                           photos=photos,
                           districts=districts,
                           amenity_options=AMENITY_OPTIONS,
                           amenities_selected=amenities_selected,
                           is_edit=True)


@host_bp.route('/host/listing/<int:listing_id>/update', methods=['POST'])
@login_required
@_host_required
@csrf_required
def listing_update(listing_id):
    """Update an existing listing."""
    from models.hosts import get_host_profile_by_user
    from models.listings import update_listing

    host = get_host_profile_by_user(session['user_id'])

    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()

    if not title or len(title) < 5:
        flash('Listing title must be at least 5 characters.', 'error')
        return redirect(url_for('host.listing_edit', listing_id=listing_id))

    def _int(key, default=0):
        try:
            return int(request.form.get(key, default))
        except (ValueError, TypeError):
            return default

    def _float(key, default=0.0):
        try:
            return float(request.form.get(key, default))
        except (ValueError, TypeError):
            return default

    listing_type = request.form.get('listing_type', 'paid_homestay')
    price = _float('price_per_night', 0) if listing_type != 'free_stay' else 0
    amenities = request.form.getlist('amenities')

    success = update_listing(
        listing_id=listing_id,
        host_id=host['id'],
        listing_type=listing_type,
        title=title,
        description=description,
        district_id=_int('district_id') or None,
        address_text=request.form.get('address_text', '').strip(),
        address_full=request.form.get('address_full', '').strip(),
        price_per_night=price,
        max_guests=max(1, _int('max_guests', 2)),
        min_stay_nights=max(1, _int('min_stay_nights', 1)),
        max_stay_nights=max(0, _int('max_stay_nights', 0)),
        num_rooms=max(1, _int('num_rooms', 1)),
        num_beds=max(1, _int('num_beds', 1)),
        num_bathrooms=max(0, _int('num_bathrooms', 1)),
        property_type=request.form.get('property_type', 'room'),
        amenities=amenities if amenities else None,
        house_rules=request.form.get('house_rules', '').strip(),
        check_in_time=request.form.get('check_in_time', '14:00'),
        check_out_time=request.form.get('check_out_time', '11:00'),
        cancellation_policy=request.form.get('cancellation_policy', 'flexible'),
    )

    if success:
        flash('✅ Listing updated.', 'success')
    else:
        flash('Could not update listing. It may not be in an editable state.', 'error')

    return redirect(url_for('host.listing_edit', listing_id=listing_id))


@host_bp.route('/host/listing/<int:listing_id>/submit', methods=['POST'])
@login_required
@_host_required
@csrf_required
def listing_submit(listing_id):
    """Submit listing for admin review."""
    from models.hosts import get_host_profile_by_user
    from models.listings import submit_listing, get_listing_by_id

    host = get_host_profile_by_user(session['user_id'])
    listing = get_listing_by_id(listing_id)

    if not listing or listing['host_id'] != host['id']:
        flash('Listing not found.', 'error')
        return redirect(url_for('host.my_listings'))

    # Validate required fields before submission
    errors = []
    if not listing['title'] or len(listing['title']) < 5:
        errors.append('Title must be at least 5 characters.')
    if not listing['description'] or len(listing['description']) < 20:
        errors.append('Description must be at least 20 characters.')
    if not listing['district_id']:
        errors.append('District is required.')
    if listing['listing_type'] == 'paid_homestay' and listing['price_per_night'] <= 0:
        errors.append('Price per night is required for paid homestays.')

    if errors:
        for e in errors:
            flash(e, 'error')
        return redirect(url_for('host.listing_edit', listing_id=listing_id))

    if submit_listing(listing_id, host['id']):
        flash('📋 Listing submitted for admin review!', 'success')
    else:
        flash('Could not submit. Only drafts and rejected listings can be submitted.', 'error')

    return redirect(url_for('host.my_listings'))


@host_bp.route('/host/listing/<int:listing_id>/archive', methods=['POST'])
@login_required
@_host_required
@csrf_required
def listing_archive(listing_id):
    """Archive (deactivate) a listing."""
    from models.hosts import get_host_profile_by_user
    from models.listings import archive_listing

    host = get_host_profile_by_user(session['user_id'])
    if archive_listing(listing_id, host['id']):
        flash('Listing archived.', 'info')
    else:
        flash('Could not archive listing.', 'error')
    return redirect(url_for('host.my_listings'))


@host_bp.route('/host/listing/<int:listing_id>/reactivate', methods=['POST'])
@login_required
@_host_required
@csrf_required
def listing_reactivate(listing_id):
    """Reactivate an archived listing."""
    from models.hosts import get_host_profile_by_user
    from models.listings import reactivate_listing

    host = get_host_profile_by_user(session['user_id'])
    if reactivate_listing(listing_id, host['id']):
        flash('Listing reactivated as draft.', 'success')
    else:
        flash('Could not reactivate listing.', 'error')
    return redirect(url_for('host.my_listings'))


# ── Photo Upload (AJAX) ──

@host_bp.route('/host/listing/<int:listing_id>/photos/upload', methods=['POST'])
@login_required
@_host_required
@csrf_required
def listing_photo_upload(listing_id):
    """Upload photos to a listing (AJAX)."""
    from models.hosts import get_host_profile_by_user
    from models.listings import (
        get_listing_by_id, add_listing_photo, count_listing_photos,
        set_cover_image
    )

    host = get_host_profile_by_user(session['user_id'])
    listing = get_listing_by_id(listing_id)

    if not listing or listing['host_id'] != host['id']:
        return jsonify({'error': 'Listing not found'}), 404

    current_count = count_listing_photos(listing_id)
    files = request.files.getlist('photos')
    uploaded = []

    for f in files:
        if current_count >= MAX_LISTING_PHOTOS:
            break
        filename = _save_listing_image(f, listing_id)
        if filename:
            photo_id = add_listing_photo(listing_id, filename, sort_order=current_count)
            # Auto-set first photo as cover
            if current_count == 0 and not listing['cover_image']:
                set_cover_image(listing_id, host['id'], filename)
            uploaded.append({
                'id': photo_id,
                'filename': filename,
                'url': url_for('static',
                               filename=f'uploads/hosts/listings/{filename}')
            })
            current_count += 1

    return jsonify({'uploaded': uploaded, 'total': current_count})


@host_bp.route('/host/listing/<int:listing_id>/photos/<int:photo_id>/delete', methods=['POST'])
@login_required
@_host_required
@csrf_required
def listing_photo_delete(listing_id, photo_id):
    """Delete a listing photo (AJAX)."""
    from models.hosts import get_host_profile_by_user
    from models.listings import get_listing_by_id, delete_listing_photo

    host = get_host_profile_by_user(session['user_id'])
    listing = get_listing_by_id(listing_id)

    if not listing or listing['host_id'] != host['id']:
        return jsonify({'error': 'Not found'}), 404

    filename = delete_listing_photo(photo_id, listing_id)
    if filename:
        # Remove file from disk
        filepath = os.path.join(LISTING_UPLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except OSError:
                pass
        return jsonify({'ok': True})

    return jsonify({'error': 'Photo not found'}), 404


# ════════════════════════════════════════════════════════════════
# HOST STAY REQUEST MANAGEMENT WORKFLOW
# ════════════════════════════════════════════════════════════════

@host_bp.route('/host/requests')
@login_required
@_host_required
def host_requests():
    """Host dashboard for managing incoming traveller stay requests."""
    from models.hosts import get_host_profile_by_user
    from models.stay_requests import get_host_requests, count_host_requests_by_status

    host = get_host_profile_by_user(session['user_id'])
    tab = request.args.get('tab', 'pending').strip().lower()
    status_filter = None
    if tab in ('pending', 'accepted', 'rejected', 'completed'):
        status_filter = tab
    elif tab == 'cancelled':
        status_filter = 'cancelled_by_traveller'

    page = request.args.get('page', 1, type=int)
    per_page = 15

    requests_list, total = get_host_requests(
        host_id=host['id'],
        status=status_filter,
        page=page,
        per_page=per_page
    )

    counts = count_host_requests_by_status(host['id'])
    total_pages = max(1, (total + per_page - 1) // per_page)

    return render_template(
        'host/requests.html',
        host=host,
        requests=requests_list,
        counts=counts,
        active_tab=tab,
        page=page,
        total=total,
        total_pages=total_pages
    )


@host_bp.route('/host/requests/<int:req_id>')
@login_required
@_host_required
def host_request_detail(req_id):
    """View detailed stay request card with guest information."""
    from models.hosts import get_host_profile_by_user
    from models.stay_requests import get_stay_request_by_id

    host = get_host_profile_by_user(session['user_id'])
    req = get_stay_request_by_id(req_id)
    if not req:
        abort(404)

    # IDOR Check: Must be the owning host
    if req['host_id'] != host['id'] and not session.get('admin_logged_in'):
        abort(403)

    return render_template('host/request_detail.html', req=req, host=host)


@host_bp.route('/host/requests/<int:req_id>/accept', methods=['POST'])
@login_required
@_host_required
@csrf_required
def host_accept_request(req_id):
    """Host accepts a pending stay request."""
    from models.hosts import get_host_profile_by_user
    from models.stay_requests import accept_stay_request

    host = get_host_profile_by_user(session['user_id'])
    host_msg = request.form.get('host_message', '').strip()

    success, err = accept_stay_request(req_id, host['id'], host_msg)
    if not success:
        flash(f'⚠️ {err}', 'error')
    else:
        flash('🎉 Stay request accepted! The guest has been notified and dates are reserved.', 'success')

    return redirect(request.referrer or url_for('host.host_requests'))


@host_bp.route('/host/requests/<int:req_id>/reject', methods=['POST'])
@login_required
@_host_required
@csrf_required
def host_reject_request(req_id):
    """Host rejects a pending stay request."""
    from models.hosts import get_host_profile_by_user
    from models.stay_requests import reject_stay_request

    host = get_host_profile_by_user(session['user_id'])
    reason = request.form.get('rejection_reason', '').strip()
    host_msg = request.form.get('host_message', '').strip()

    success, err = reject_stay_request(req_id, host['id'], reason, host_msg)
    if not success:
        flash(f'⚠️ {err}', 'error')
    else:
        flash('Stay request has been declined.', 'info')

    return redirect(request.referrer or url_for('host.host_requests'))


@host_bp.route('/host/requests/<int:req_id>/cancel', methods=['POST'])
@login_required
@_host_required
@csrf_required
def host_cancel_request(req_id):
    """Host cancels an already accepted stay request."""
    from models.hosts import get_host_profile_by_user
    from models.stay_requests import cancel_stay_request_by_host

    host = get_host_profile_by_user(session['user_id'])
    reason = request.form.get('cancellation_reason', '').strip()

    success, err = cancel_stay_request_by_host(req_id, host['id'], reason)
    if not success:
        flash(f'⚠️ {err}', 'error')
    else:
        flash('Reservation has been cancelled and dates have been freed.', 'info')

    return redirect(request.referrer or url_for('host.host_requests'))
