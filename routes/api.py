"""API routes — autocomplete, smart search, visited toggle, instant search, nearby, analytics."""
import time
from flask import Blueprint, request, jsonify, session
from models.database import (
    search_places, smart_search, nl_search,
    mark_visited, unmark_visited, is_visited,
    get_trending_places,
    get_nearby_services_with_distance, get_place_by_id,
    get_service_type_icon, get_service_group, SERVICE_GROUP_ORDER,
    get_smart_nearby_discovery, get_10_nearby_essentials, get_nearby_api_data,
    instant_search, get_search_suggestions,
    nearby_search, get_filter_options, get_search_analytics
)
from utils import csrf_required, get_session_id as _get_session_id

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/nearby')
def api_nearby():
    """GET /api/nearby endpoint.
    Params: lat (float), lng (float), radius (float, default 5.0), category (str, optional).
    Returns nearby essential services sorted nearest first with Overpass API primary & local DB fallback.
    """
    lat = request.args.get('lat', default=25.5941, type=float)
    lng = request.args.get('lng', default=85.1376, type=float)
    radius = request.args.get('radius', default=5.0, type=float)
    category = request.args.get('category', '').strip().lower() or None

    results = get_nearby_api_data(lat, lng, radius_km=radius, category=category)

    return jsonify({
        'status': 'success',
        'latitude': lat,
        'longitude': lng,
        'radius_km': radius,
        'category': category,
        'count': len(results),
        'results': results
    })


@api_bp.route('/smart-nearby')
def api_smart_nearby():
    """Google Maps-style Smart Nearby Discovery API.
    Returns matching places & services sorted by distance with travel metrics & 10 nearby essentials.
    """
    lat = request.args.get('lat', default=25.5941, type=float) # Patna default if unlocated
    lng = request.args.get('lng', default=85.1376, type=float)
    category = request.args.get('category', '').strip() or None
    q = request.args.get('q', '').strip() or None
    limit = request.args.get('limit', default=50, type=int)

    bounds_raw = request.args.get('bounds', '').strip()
    bounds = None
    if bounds_raw:
        try:
            parts = [float(x) for x in bounds_raw.split(',')]
            if len(parts) == 4:
                bounds = parts
        except ValueError:
            bounds = None

    sid = _get_session_id()
    results = get_smart_nearby_discovery(lat, lng, category=category, query=q, bounds=bounds, session_id=sid, limit=limit)

    return jsonify({
        'status': 'success',
        'query': q,
        'category': category,
        'user_location': {'lat': lat, 'lng': lng},
        'count': len(results),
        'results': results
    })


@api_bp.route('/place/<int:place_id>/nearby-essentials')
def api_place_nearby_essentials(place_id):
    """Retrieve 10 nearby essential services (Hotel, Hospital, Petrol Pump, Pharmacy, etc.) for a place."""
    place = get_place_by_id(place_id)
    if not place or not place.get('latitude') or not place.get('longitude'):
        return jsonify({'error': 'Place or location coordinates not found'}), 404

    lat = float(place['latitude'])
    lng = float(place['longitude'])
    essentials = get_10_nearby_essentials(lat, lng, district_id=place.get('district_id'), place_id=place_id)

    return jsonify({
        'status': 'success',
        'place_id': place_id,
        'place_name': place['name'],
        'location': {'lat': lat, 'lng': lng},
        'count': len(essentials),
        'essentials': essentials
    })


@api_bp.route('/search/instant')
def api_instant_search():
    """Production-grade instant search with fuzzy matching, NL parsing, synonyms,
    Hindi/Roman Hindi support, phonetic matching, smart filters, and nearby search."""
    t0 = time.perf_counter()
    q = request.args.get('q', '').strip()
    limit = min(request.args.get('limit', 12, type=int), 50)  # Cap at 50

    if not q:
        suggestions = get_search_suggestions(limit=6)
        filters_opts = get_filter_options()
        return jsonify({
            'results': [], 'suggestions': suggestions,
            'query': '', 'did_you_mean': None,
            'filters': filters_opts,
            'ms': round((time.perf_counter() - t0) * 1000, 1)
        })

    # Build filters from query params
    filters = {}
    cat = request.args.get('category', '').strip()
    if cat:
        filters['category'] = cat
    dist = request.args.get('district', '').strip()
    if dist:
        filters['district'] = dist
    if request.args.get('family_friendly') == '1':
        filters['family_friendly'] = True
    if request.args.get('free_entry') == '1':
        filters['free_entry'] = True
    if request.args.get('has_parking') == '1':
        filters['has_parking'] = True
    radius = request.args.get('radius_km', type=int)
    if radius:
        filters['radius_km'] = radius

    # User geolocation
    user_lat = request.args.get('lat', type=float)
    user_lng = request.args.get('lng', type=float)

    results = instant_search(q, limit=limit, filters=filters,
                             user_lat=user_lat, user_lng=user_lng)

    # Determine "did you mean" — if query is a typo of top result name or district
    did_you_mean = None
    if results and q:
        from models.search_engine import levenshtein_distance, normalize_compact
        q_c = normalize_compact(q)
        # Check top result name
        top_name = results[0].get('name', '')
        top_name_c = normalize_compact(top_name)
        if 0 < levenshtein_distance(q_c, top_name_c) <= 2 and len(q_c) >= 3:
            did_you_mean = top_name
        else:
            # Check top result district
            top_dist = results[0].get('district_name', '')
            if top_dist:
                top_dist_c = normalize_compact(top_dist)
                if 0 < levenshtein_distance(q_c, top_dist_c) <= 2 and len(q_c) >= 3:
                    did_you_mean = top_dist

    return jsonify({
        'results': results, 'suggestions': [],
        'query': q, 'did_you_mean': did_you_mean,
        'ms': round((time.perf_counter() - t0) * 1000, 1)
    })


@api_bp.route('/search/nearby')
def api_nearby_search():
    """Nearby search endpoint — returns places sorted by distance."""
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    if not lat or not lng:
        return jsonify({'error': 'lat and lng required'}), 400
    radius = min(request.args.get('radius_km', 25, type=int), 100)
    category = request.args.get('category', '').strip() or None
    limit = min(request.args.get('limit', 20, type=int), 50)
    results = nearby_search(lat, lng, radius_km=radius, limit=limit, category=category)
    return jsonify({'results': results, 'lat': lat, 'lng': lng, 'radius_km': radius})


@api_bp.route('/search/filters')
def api_search_filters():
    """Return available filter options for the search UI."""
    return jsonify(get_filter_options())


@api_bp.route('/search/analytics')
def api_search_analytics():
    """Search analytics for admin — trending queries, failed searches, stats."""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 403
    analytics = get_search_analytics()
    return jsonify(analytics.get_stats())


@api_bp.route('/autocomplete')
def autocomplete():
    """Backward-compatible autocomplete — delegates to instant search."""
    q = request.args.get('q', '').strip()
    if len(q) < 1:
        return jsonify([])
    results = instant_search(q, limit=8)
    return jsonify([{
        'id': r['id'], 'name': r['name'], 'slug': r.get('slug', ''),
        'state_name': r.get('state_name', ''),
        'district_name': r.get('district_name', ''),
        'category': r.get('category', ''),
        'url': r.get('url', ''),
        'type': r.get('type', 'place'),
    } for r in results])


@api_bp.route('/smart-search')
def api_smart_search():
    """Smart search: 'I am going to Patna'."""
    q = request.args.get('q', '').strip()
    if len(q) < 2:
        return jsonify({'query': '', 'places': [], 'foods': [], 'hotels': []})
    return jsonify(smart_search(q))


@api_bp.route('/search/nl')
def api_nl_search():
    """Natural language search endpoint with intent detection."""
    q = request.args.get('q', '').strip()
    if len(q) < 2:
        return jsonify({'original_query': q, 'parsed_intents': {}, 'places': []})
    return jsonify(nl_search(q))



@api_bp.route('/visited/<int:place_id>', methods=['POST'])
@csrf_required
def toggle_visited(place_id):
    """Toggle visited status for a place."""
    sid = _get_session_id()
    if is_visited(sid, place_id):
        unmark_visited(sid, place_id)
        return jsonify({'status': 'unmarked'})
    else:
        mark_visited(sid, place_id)
        return jsonify({'status': 'marked'})


@api_bp.route('/visited/<int:place_id>')
def check_visited(place_id):
    """Check if a place is visited."""
    sid = _get_session_id()
    return jsonify({'visited': is_visited(sid, place_id)})


@api_bp.route('/trending')
def api_trending():
    """Get trending places."""
    places = get_trending_places(limit=8)
    return jsonify([{
        'id': p['id'], 'name': p['name'], 'slug': p['slug'],
        'state_name': p['state_name'], 'category': p['category'],
        'cover_image': p.get('cover_image', '')
    } for p in places])


@api_bp.route('/nearby-services/<int:place_id>')
def api_nearby_services(place_id):
    """Get nearby services with distance from user location."""
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    if lat is None or lng is None:
        return jsonify({'error': 'lat and lng required'}), 400

    place = get_place_by_id(place_id)
    if not place:
        return jsonify({'error': 'Place not found'}), 404

    services = get_nearby_services_with_distance(
        lat, lng,
        district_id=place.get('district_id'),
        place_id=place_id,
        limit=30
    )

    # Group by service category
    grouped = {}
    for g in SERVICE_GROUP_ORDER:
        grouped[g] = []

    for s in services:
        group = get_service_group(s['service_type'])
        if group not in grouped:
            grouped[group] = []
        grouped[group].append({
            'id': s['id'],
            'name': s['name'],
            'service_type': s['service_type'],
            'icon': get_service_type_icon(s['service_type']),
            'address': s.get('address', ''),
            'phone': s.get('phone', ''),
            'latitude': s.get('latitude'),
            'longitude': s.get('longitude'),
            'distance_km': s.get('distance_km'),
        })

    # Remove empty groups
    grouped = {k: v for k, v in grouped.items() if v}

    return jsonify({'services': grouped})

