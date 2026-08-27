"""Itinerary routes — build multi-day trip plans."""
import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify

from models.itineraries import calculate_itinerary_budget, get_pacing_config
from models.database import (
    save_itinerary, create_itinerary, get_itineraries, get_itinerary_by_id,
    get_itinerary_items, add_itinerary_item, remove_itinerary_item,
    delete_itinerary, get_place_by_id, search_places
)
from utils import csrf_required, get_session_id as _get_session_id

logger = logging.getLogger(__name__)
itinerary_bp = Blueprint('itinerary', __name__)


@itinerary_bp.route('/itinerary')
def itinerary_page():
    sid = _get_session_id()
    itineraries = get_itineraries(sid)
    return render_template('itinerary.html', itineraries=itineraries)


@itinerary_bp.route('/itinerary/create', methods=['POST'])
@csrf_required
def create_trip():
    sid = _get_session_id()
    name = request.form.get('name', '').strip() or 'My Trip'
    uid = session.get('user_id')
    iid = save_itinerary(session_id=sid, user_id=uid, title=name, days=2, companion='solo', budget='medium', items_data=[])
    flash(f'🗺️ Trip "{name}" created!', 'success')
    return redirect(url_for('itinerary.itinerary_page'))


@itinerary_bp.route('/itinerary/<int:itinerary_id>')
def view_trip(itinerary_id):
    sid = _get_session_id()
    trip = get_itinerary_by_id(itinerary_id, sid)
    if not trip:
        flash('Trip not found.', 'error')
        return redirect(url_for('itinerary.itinerary_page'))
    items = get_itinerary_items(itinerary_id)
    # Group items by day
    days = {}
    for item in items:
        day = item['day_number']
        if day not in days:
            days[day] = []
        days[day].append(item)
    return render_template('itinerary_detail.html', trip=trip, days=days, items=items)


@itinerary_bp.route('/itinerary/<int:itinerary_id>/add', methods=['POST'])
@csrf_required
def add_place_to_trip(itinerary_id):
    sid = _get_session_id()
    trip = get_itinerary_by_id(itinerary_id, sid)
    if not trip:
        return jsonify({'error': 'Trip not found'}), 404

    place_id = request.form.get('place_id', type=int)
    day_number = request.form.get('day_number', 1, type=int)
    notes = request.form.get('notes', '').strip()

    if place_id:
        add_itinerary_item(itinerary_id, place_id, day_number, notes)
        flash('Place added to your trip! 🎉', 'success')

    return redirect(url_for('itinerary.view_trip', itinerary_id=itinerary_id))


@itinerary_bp.route('/itinerary/<int:itinerary_id>/remove/<int:item_id>', methods=['POST'])
@csrf_required
def remove_place_from_trip(itinerary_id, item_id):
    sid = _get_session_id()
    trip = get_itinerary_by_id(itinerary_id, sid)
    if not trip:
        flash('Trip not found or access denied.', 'error')
        return redirect(url_for('itinerary.itinerary_page'))
    # Verify item belongs to this itinerary
    items = get_itinerary_items(itinerary_id)
    item_ids = {item['id'] for item in items}
    if item_id not in item_ids:
        flash('Item not found in this trip.', 'error')
        return redirect(url_for('itinerary.view_trip', itinerary_id=itinerary_id))
    remove_itinerary_item(item_id)
    return redirect(url_for('itinerary.view_trip', itinerary_id=itinerary_id))


@itinerary_bp.route('/itinerary/<int:itinerary_id>/delete', methods=['POST'])
@csrf_required
def delete_trip(itinerary_id):
    sid = _get_session_id()
    delete_itinerary(itinerary_id, sid)
    flash('Trip deleted.', 'info')
    return redirect(url_for('itinerary.itinerary_page'))


@itinerary_bp.route('/api/itinerary/search')
def api_search_places():
    """Search places for adding to itinerary or browsing destinations."""
    q = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip().lower()

    if not q:
        try:
            from models.database import get_cursor
            with get_cursor() as cur:
                if category and category != 'all':
                    cur.execute("""
                        SELECT p.id, p.name, p.slug, p.category, p.cover_image, p.description,
                               d.name AS district_name, s.name AS state_name
                        FROM places p
                        JOIN states s ON s.id = p.state_id
                        LEFT JOIN districts d ON d.id = p.district_id
                        WHERE p.deleted_at IS NULL AND p.category = %s
                        ORDER BY p.is_featured DESC, p.view_count DESC
                        LIMIT 30
                    """, (category,))
                else:
                    cur.execute("""
                        SELECT p.id, p.name, p.slug, p.category, p.cover_image, p.description,
                               d.name AS district_name, s.name AS state_name
                        FROM places p
                        JOIN states s ON s.id = p.state_id
                        LEFT JOIN districts d ON d.id = p.district_id
                        WHERE p.deleted_at IS NULL
                        ORDER BY p.is_featured DESC, p.view_count DESC
                        LIMIT 30
                    """)
                results = cur.fetchall()
        except Exception:
            results = []
    else:
        try:
            results = search_places(q, limit=30)
            if category and category != 'all':
                results = [p for p in results if p.get('category') == category]
        except Exception:
            results = []

    return jsonify([{
        'id': p['id'],
        'name': p['name'],
        'slug': p['slug'],
        'state_name': p.get('state_name', 'Bihar'),
        'district_name': p.get('district_name') or p.get('state_name', 'Bihar'),
        'category': p.get('category', 'tourist_spot'),
        'cover_image': p.get('cover_image') or '',
        'description': (p.get('description') or '')[:120]
    } for p in results])


# ── Scoring weights — externalized for tuning without code changes ──
SCORING_WEIGHTS = {
    'interest_match': 6.0,
    'family_friendly': 4.0,
    'family_category': 2.5,
    'companion_category': 3.5,
    'hidden_gem': 2.0,
    'popularity_divisor': 40.0,
    'popularity_cap': 200,
}


@itinerary_bp.route('/api/itinerary/generate', methods=['POST'])
@csrf_required
def api_generate_trip():
    """AI Trip Planner — generates an optimized, realistic multi-day itinerary.
    Uses Haversine spatial clustering, companion scoring, and district food/hotel matching.
    """
    import math
    from models.database import get_cursor, get_district_foods, get_accommodations_by_place

    data = request.get_json() or {}
    days = min(max(int(data.get('days', 3)), 1), 30)
    interests = data.get('interests', [])
    companion = data.get('companion', 'solo')  # solo, couple, family, group
    travelers = min(max(int(data.get('travelers', 1)), 1), 20)

    # Optional pinned place_ids selected by user
    raw_pids = data.get('place_ids', [])
    place_ids = []
    if isinstance(raw_pids, (list, tuple)):
        for pid in raw_pids:
            try:
                place_ids.append(int(pid))
            except (ValueError, TypeError):
                pass

    # ── Budget: accept numeric amount + type, with backward compatibility ──
    budget_amount = data.get('budget_amount')
    budget_type = data.get('budget_type', 'per_day')  # per_day or total

    if budget_amount is not None:
        budget_amount = max(int(budget_amount), 500)
        if budget_type == 'total':
            budget_per_day = budget_amount // max(days, 1)
        else:
            budget_per_day = budget_amount
    else:
        # Backward compatibility with old low/medium/high
        old_budget = data.get('budget', 'medium')
        budget_per_day = {'low': 1500, 'medium': 3500, 'high': 7500}.get(old_budget, 3500)

    # Fetch all active places with coordinates and district info
    with get_cursor() as cur:
        cur.execute("""
            SELECT p.id, p.name, p.slug, p.category, p.latitude, p.longitude,
                   p.description, p.cover_image, p.view_count, p.family_friendly, p.is_hidden_gem,
                   p.best_season, p.best_time_to_visit, p.district_id,
                   d.name AS district_name, s.name AS state_name
            FROM places p
            JOIN districts d ON p.district_id = d.id
            JOIN states s ON d.state_id = s.id
            WHERE p.deleted_at IS NULL
              AND p.latitude IS NOT NULL AND p.longitude IS NOT NULL
            ORDER BY p.view_count DESC
        """)
        all_places = cur.fetchall()

    if not all_places:
        return jsonify({'error': 'No places available for itinerary generation'}), 404

    W = SCORING_WEIGHTS  # alias for readability

    # Companion-mode filtering & scoring
    scored = []
    for p in all_places:
        score = 1.0
        cat = p.get('category', 'tourist_spot')

        # User interests bonus
        if interests and cat in interests:
            score += W['interest_match']

        # Companion mode bonuses
        if companion == 'family':
            if p.get('family_friendly'): score += W['family_friendly']
            if cat in ['park', 'temple', 'tourist_spot', 'historical']: score += W['family_category']
        elif companion == 'couple':
            if cat in ['hill_station', 'waterfall', 'lake', 'nature', 'historical', 'hidden_gem']: score += W['companion_category']
        elif companion == 'solo':
            if cat in ['fort', 'wildlife', 'hidden_gem', 'waterfall', 'nature']: score += W['companion_category']
        elif companion == 'group':
            if cat in ['fort', 'waterfall', 'lake', 'tourist_spot', 'hidden_gem']: score += W['companion_category']

        # Hidden gem bonus
        if p.get('is_hidden_gem'):
            score += W['hidden_gem']

        # Popularity score weight
        score += min((p.get('view_count') or 0), W['popularity_cap']) / W['popularity_divisor']
        scored.append((score, p))

    scored.sort(key=lambda x: -x[0])
    candidate_pool = [s[1] for s in scored]

    # Haversine Distance Helper (km)
    def haversine(lat1, lng1, lat2, lng2):
        R = 6371
        dlat = math.radians(float(lat2) - float(lat1))
        dlng = math.radians(float(lng2) - float(lng1))
        a = (math.sin(dlat/2)**2 +
             math.cos(math.radians(float(lat1))) *
             math.cos(math.radians(float(lat2))) *
             math.sin(dlng/2)**2)
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) if a < 1 else 0

    # Cluster-based Day Assignment
    places_per_day = 3
    used_ids = set()
    day_plans = []

    # Map place_id to place dict if provided
    pinned_places = [p for p in all_places if p['id'] in place_ids] if place_ids else []
    pinned_queue = list(pinned_places)

    for day in range(1, days + 1):
        day_places = []
        
        # Priority 1: Pick an unvisited pinned place as Day Anchor
        anchor = None
        while pinned_queue:
            cand = pinned_queue.pop(0)
            if cand['id'] not in used_ids:
                anchor = cand
                break

        # If no unvisited pinned place available, pick highest-scoring unvisited candidate
        if not anchor:
            for p in candidate_pool:
                if p['id'] not in used_ids:
                    anchor = p
                    break

        if not anchor:
            break

        day_places.append(anchor)
        used_ids.add(anchor['id'])

        # Find closest unvisited places within 50km radius of the Day Anchor
        while len(day_places) < places_per_day:
            last = day_places[-1]

            # First check if there are any remaining pinned places within reasonable distance (< 75km)
            nearby_pinned = [
                p for p in pinned_queue
                if p['id'] not in used_ids and haversine(last['latitude'], last['longitude'], p['latitude'], p['longitude']) <= 75.0
            ]
            if nearby_pinned:
                best_pinned = min(nearby_pinned, key=lambda p: haversine(last['latitude'], last['longitude'], p['latitude'], p['longitude']))
                day_places.append(best_pinned)
                used_ids.add(best_pinned['id'])
                if best_pinned in pinned_queue:
                    pinned_queue.remove(best_pinned)
                continue

            candidates = []

            for p in candidate_pool:
                if p['id'] in used_ids:
                    continue
                # Calculate distance from current last place in day
                dist_from_last = haversine(last['latitude'], last['longitude'], p['latitude'], p['longitude'])
                # Calculate distance from day anchor
                dist_from_anchor = haversine(anchor['latitude'], anchor['longitude'], p['latitude'], p['longitude'])

                if dist_from_anchor <= 50.0:  # Max 50km cluster radius
                    candidates.append((dist_from_last, p))

            if candidates:
                candidates.sort(key=lambda x: x[0])  # Sort by proximity to last place
                best_place = candidates[0][1]
                day_places.append(best_place)
                used_ids.add(best_place['id'])
            else:
                # If no place within 50km, pick next closest place overall
                next_best = None
                min_dist = float('inf')
                for p in candidate_pool:
                    if p['id'] not in used_ids:
                        d = haversine(last['latitude'], last['longitude'], p['latitude'], p['longitude'])
                        if d < min_dist:
                            min_dist = d
                            next_best = p
                if next_best:
                    day_places.append(next_best)
                    used_ids.add(next_best['id'])
                else:
                    break

        day_plans.append(day_places)

    # Budget & Pricing Engine — uses user's per-day budget and travelers count
    # Split per-day budget into proportional categories
    transport_ratio = 0.20
    food_ratio = 0.25
    stay_ratio = 0.45
    entry_ratio = 0.10

    total_budget = {
        'transport': int(budget_per_day * transport_ratio * days * travelers),
        'food': int(budget_per_day * food_ratio * days * travelers),
        'accommodation': int(budget_per_day * stay_ratio * max(days - 1, 1) * max(travelers / 2, 1)),
        'entry_fees': int(budget_per_day * entry_ratio * sum(len(d) for d in day_plans) * travelers),
    }
    total_budget['total'] = sum(total_budget.values())

    companion_labels = {
        'solo': 'Solo Explorer 👤',
        'couple': 'Couple Getaway 👩‍❤️‍👨',
        'family': 'Family Trip 👨‍👩‍👧‍👦',
        'group': 'Group Trip 👥'
    }

    result = {
        'trip_name': f"{days}-Day Bihar {companion_labels.get(companion, 'Explorer')} Itinerary",
        'days': days,
        'travelers': travelers,
        'budget_per_day': budget_per_day,
        'companion': companion,
        'estimated_cost': total_budget,
        'itinerary': []
    }

    # Time slot templates
    time_slots = [
        {'time': '09:00 AM', 'phase': 'Morning Exploration'},
        {'time': '01:00 PM', 'phase': 'Afternoon Visit & Lunch'},
        {'time': '04:30 PM', 'phase': 'Evening Sightseeing'}
    ]

    for day_num, day_places in enumerate(day_plans, 1):
        districts = list(dict.fromkeys(p.get('district_name', '') for p in day_places if p.get('district_name')))
        district_text = ', '.join(districts) if districts else 'Bihar'

        day_data = {
            'day': day_num,
            'title': f"Day {day_num} — {district_text}",
            'pacing_note': f"Cluster tour in {district_text} • Short travel time between locations",
            'places': [],
            'recommended_foods': [],
            'recommended_hotels': []
        }

        if day_places:
            # Fetch local foods for visited districts
            district_ids = list(dict.fromkeys(p.get('district_id') for p in day_places if p.get('district_id')))
            foods = []
            for did in district_ids:
                df = get_district_foods(did)
                if df: foods.extend(df[:2])

            # Fallback if no specific district foods
            if not foods:
                foods = [
                    {'name': 'Litti Chokha', 'description': 'Traditional roasted wheat balls stuffed with sattu, served with spiced brinjal and mashed potato.'},
                    {'name': 'Khaja', 'description': 'Crispy layered sweet delicacy from Silao, GI-tagged authentic Bihari treat.'},
                    {'name': 'Tilkut', 'description': 'Sesame seed and jaggery brittle specialty from Gaya.'}
                ]

            seen_food_names = set()
            unique_foods = []
            for f in foods:
                if f.get('name') and f['name'] not in seen_food_names:
                    seen_food_names.add(f['name'])
                    unique_foods.append(f)

            day_data['recommended_foods'] = [{'name': f['name'], 'description': (f.get('description') or '')[:90]} for f in unique_foods[:3]]

            # Fetch hotels/stays for main day place
            main_p = day_places[0]
            hotels = get_accommodations_by_place(main_p['id']) if main_p else []
            if not hotels:
                # Honest fallback — don't fabricate hotel names
                stay_est = int(budget_per_day * stay_ratio)
                hotels = [
                    {'name': f"Explore local stays in {district_text}", 'price_range': f"~₹{stay_est}/night (estimated)", 'rating': None},
                ]
            stay_est_fallback = int(budget_per_day * stay_ratio)
            day_data['recommended_hotels'] = [{'name': h['name'], 'price_range': h.get('price_range', f"₹{stay_est_fallback}/night"), 'rating': h.get('rating')} for h in hotels[:2]]

        for order, place in enumerate(day_places):
            slot = time_slots[order] if order < len(time_slots) else {'time': '06:00 PM', 'phase': 'Evening Visit'}
            day_data['places'].append({
                'id': place['id'],
                'name': place['name'],
                'slug': place['slug'],
                'category': place['category'],
                'district': place.get('district_name', ''),
                'description': (place.get('description', '') or '')[:180],
                'cover_image': place.get('cover_image', ''),
                'time': slot['time'],
                'phase': slot['phase'],
                'latitude': float(place['latitude']) if place['latitude'] else None,
                'longitude': float(place['longitude']) if place['longitude'] else None,
            })

        result['itinerary'].append(day_data)

    return jsonify(result)


@itinerary_bp.route('/api/itinerary/save-generated', methods=['POST'])
@csrf_required
def api_save_generated():
    """Save an AI-generated itinerary to the user's trips."""
    sid = _get_session_id()
    data = request.get_json() or {}
    trip_name = data.get('name', 'AI Generated Trip')
    itinerary_data = data.get('itinerary', [])

    iid = create_itinerary(sid, trip_name)

    for day in itinerary_data:
        day_num = day.get('day', 1)
        for order, place in enumerate(day.get('places', [])):
            place_id = place.get('id')
            if place_id:
                add_itinerary_item(iid, place_id, day_num, place.get('time', ''))

    return jsonify({'id': iid, 'redirect': url_for('itinerary.view_trip', itinerary_id=iid)})



@itinerary_bp.route('/api/budget-estimate', methods=['GET'])
def api_budget_estimate():
    """API endpoint to calculate estimated trip budget."""
    days = request.args.get('days', 3, type=int)
    companion = request.args.get('companion', 'solo')
    budget_tier = request.args.get('tier', 'moderate')
    pace = request.args.get('pace', 'balanced')

    estimate = calculate_itinerary_budget(days=days, companion_type=companion, budget_tier=budget_tier)
    pacing = get_pacing_config(pace)
    return jsonify({
        'status': 'success',
        'budget': estimate,
        'pacing': pacing
    })


@itinerary_bp.route('/<int:itinerary_id>/export/json', methods=['GET'])
def export_itinerary_json(itinerary_id):
    """Export itinerary details as a formatted JSON document."""
    itin = get_itinerary_by_id(itinerary_id)
    if not itin:
        return jsonify({'error': 'Itinerary not found'}), 404
    items = get_itinerary_items(itinerary_id)
    return jsonify({
        'status': 'success',
        'itinerary': itin,
        'items': items,
        'export_format': 'json',
        'generator': 'HiddenYatra AI Trip Planner'
    })


@itinerary_bp.route('/api/cultural-highlights', methods=['GET'])
def api_cultural_highlights():
    """API endpoint to get festivals and thematic circuits matching travel parameters."""
    from models.itineraries import get_itinerary_cultural_highlights
    month = request.args.get('month')
    districts = request.args.getlist('district') or request.args.get('districts', '').split(',')
    districts = [d.strip() for d in districts if d.strip()]

    highlights = get_itinerary_cultural_highlights(travel_month=month, districts=districts)
    return jsonify({
        'status': 'success',
        'highlights': highlights
    })