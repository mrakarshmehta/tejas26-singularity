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

    results = instant_search(q, limit=limit, filters=filters, seq_id=seq_id,
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



@api_bp.route('/places/nearby-radius', methods=['GET'])
def api_places_nearby_radius():
    """Discover places within a custom circular radius (km) with distance sorting."""
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    radius_km = request.args.get('radius', 25.0, type=float)
    category = request.args.get('category')

    if lat is None or lng is None:
        return jsonify({'status': 'error', 'message': 'lat and lng parameters are required'}), 400

    from models.places import calculate_haversine_distance, get_places_by_filter
    places = get_places_by_filter(category=category, limit=50)

    results = []
    for p in places:
        plat = p.get('latitude')
        plng = p.get('longitude')
        if plat and plng:
            dist = calculate_haversine_distance(lat, lng, plat, plng)
            if dist <= radius_km:
                p_copy = dict(p)
                p_copy['distance_km'] = dist
                results.append(p_copy)

    results.sort(key=lambda x: x['distance_km'])
    return jsonify({
        'status': 'success',
        'center': {'lat': lat, 'lng': lng},
        'radius_km': radius_km,
        'count': len(results),
        'places': results
    })


@api_bp.route('/circuits', methods=['GET'])
def api_get_circuits():
    """JSON API endpoint returning all curated Bihar thematic circuits."""
    from models.circuits import get_all_circuits, filter_circuits_by_theme
    theme = request.args.get('theme')
    circuits = filter_circuits_by_theme(theme) if theme else get_all_circuits()
    return jsonify({
        'status': 'success',
        'count': len(circuits),
        'circuits': circuits
    })


@api_bp.route('/circuits/<slug>', methods=['GET'])
def api_get_circuit_detail(slug):
    """JSON API endpoint returning specific circuit data, stops, and transit metrics."""
    from models.circuits import get_circuit_by_slug, calculate_circuit_metrics
    circuit = get_circuit_by_slug(slug)
    if not circuit:
        return jsonify({'status': 'error', 'message': f'Circuit not found: {slug}'}), 404
    metrics = calculate_circuit_metrics(slug)
    return jsonify({
        'status': 'success',
        'circuit': circuit,
        'metrics': metrics
    })


@api_bp.route('/places/<slug>/audio-guide', methods=['GET'])
def api_get_place_audio_guide(slug):
    """JSON API returning audio guide stream links and transcripts for multiple languages."""
    from models.places import get_place_audio_guide, PLACE_AUDIO_GUIDES_DB
    guide = get_place_audio_guide(slug)
    if not guide:
        return jsonify({
            'status': 'not_found',
            'message': f'No audio guide currently available for: {slug}',
            'available_places': list(PLACE_AUDIO_GUIDES_DB.keys())
        }), 404

    lang = request.args.get('lang', 'en')
    selected_track = guide['languages'].get(lang) or guide['languages'].get('en')

    return jsonify({
        'status': 'success',
        'title': guide['title'],
        'district': guide['district'],
        'duration_sec': guide['duration_sec'],
        'narrator': guide['narrator'],
        'selected_language': lang,
        'track': selected_track,
        'supported_languages': list(guide['languages'].keys())
    })


@api_bp.route('/festivals', methods=['GET'])
def api_get_festivals():
    """JSON API endpoint returning Bihar cultural festivals filtered by month or district."""
    from models.festivals import get_all_festivals, get_festivals_by_month, get_festivals_by_district
    month = request.args.get('month')
    district = request.args.get('district')

    if month:
        festivals = get_festivals_by_month(month)
    elif district:
        festivals = get_festivals_by_district(district)
    else:
        festivals = get_all_festivals()

    return jsonify({
        'status': 'success',
        'count': len(festivals),
        'festivals': festivals
    })


@api_bp.route('/crafts', methods=['GET'])
def api_get_crafts():
    """JSON API endpoint returning Bihar GI-tagged crafts and artisan directories."""
    from models.crafts import get_all_crafts, get_crafts_by_district
    district = request.args.get('district')
    crafts = get_crafts_by_district(district) if district else get_all_crafts()
    return jsonify({
        'status': 'success',
        'count': len(crafts),
        'crafts': crafts
    })


@api_bp.route('/crafts/<slug>', methods=['GET'])
def api_get_craft_detail(slug):
    """JSON API endpoint returning craft details and verified artisan workshops."""
    from models.crafts import get_craft_by_slug, get_artisan_centers_for_craft
    craft = get_craft_by_slug(slug)
    if not craft:
        return jsonify({'status': 'not_found', 'message': f'Craft not found: {slug}'}), 404
    centers = get_artisan_centers_for_craft(slug)
    return jsonify({
        'status': 'success',
        'craft': craft,
        'artisan_centers': centers
    })


@api_bp.route('/eco/pledge', methods=['POST'])
def api_submit_eco_pledge():
    """Sign the HiddenYatra Responsible Traveler Pledge."""
    from models.eco import validate_pledge_submission
    data = request.get_json(silent=True) or request.form
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip()
    state_origin = (data.get('state_origin') or 'India').strip()

    is_valid, msg = validate_pledge_submission(name, email, state_origin)
    if not is_valid:
        return jsonify({'status': 'error', 'message': msg}), 400

    return jsonify({
        'status': 'success',
        'message': f'Thank you {name}! You are now a certified Responsible Traveler for Bihar.',
        'badge': '🌿 Bihar Eco-Heritage Guardian',
        'certificate_code': f'HY-ECO-{abs(hash(email)) % 100000:05d}'
    })


@api_bp.route('/safety/emergency', methods=['GET'])
def api_get_emergency_contacts():
    """JSON API returning statewide helplines and district police/tourist desk contacts."""
    from models.safety import get_statewide_helplines, get_district_safety, get_all_district_safety
    district = request.args.get('district')
    statewide = get_statewide_helplines()

    if district:
        dist_info = get_district_safety(district)
        if not dist_info:
            return jsonify({
                'status': 'not_found',
                'message': f'Safety information not found for district: {district}'
            }), 404
        return jsonify({
            'status': 'success',
            'statewide_helplines': statewide,
            'district_safety': dist_info
        })

    return jsonify({
        'status': 'success',
        'statewide_helplines': statewide,
        'districts': get_all_district_safety()
    })


@api_bp.route('/safety/medical', methods=['GET'])
def api_get_medical_facilities():
    """JSON API returning 24/7 hospitals and trauma centers with optional district filter."""
    from models.safety import get_medical_facilities
    district = request.args.get('district')
    facilities = get_medical_facilities(district)
    return jsonify({
        'status': 'success',
        'count': len(facilities),
        'district': district or 'all',
        'facilities': facilities
    })


@api_bp.route('/safety/guidelines', methods=['GET'])
def api_get_safety_guidelines():
    """JSON API returning traveler safety tips and seasonal advisories."""
    from models.safety import get_safety_guidelines
    return jsonify({
        'status': 'success',
        'guidelines': get_safety_guidelines()
    })

@api_bp.route('/transport/hubs', methods=['GET'])
def api_get_transport_hubs():
    """JSON API returning airports, railway junctions, and bus terminals."""
    from models.transport import get_all_transport_hubs
    return jsonify({
        'status': 'success',
        'hubs': get_all_transport_hubs()
    })


@api_bp.route('/transport/routes', methods=['GET'])
def api_get_transit_routes():
    """JSON API returning inter-district transit times and distance matrices."""
    from models.transport import get_interdistrict_routes
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    routes = get_interdistrict_routes(origin, destination)
    return jsonify({
        'status': 'success',
        'count': len(routes),
        'routes': routes
    })


@api_bp.route('/transport/estimate-fare', methods=['GET', 'POST'])
def api_estimate_transport_fare():
    """JSON API calculating estimated transit fare by vehicle type and distance."""
    from models.transport import estimate_commute_fare
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form
        vehicle = data.get('vehicle_type', 'auto_reserved')
        distance = data.get('distance_km', 5.0)
        is_night = bool(data.get('is_night', False))
    else:
        vehicle = request.args.get('vehicle_type', 'auto_reserved')
        distance = request.args.get('distance_km', 5.0)
        is_night = request.args.get('is_night', '').lower() in ['1', 'true', 'yes']

    try:
        dist_float = float(distance)
    except (ValueError, TypeError):
        dist_float = 5.0

    estimate = estimate_commute_fare(
        vehicle_type=vehicle,
        distance_km=dist_float,
        is_night=is_night
    )
    return jsonify({
        'status': 'success',
        'fare_estimate': estimate
    })

@api_bp.route('/panoramas', methods=['GET'])
def api_get_panoramas():
    """JSON API returning all virtual 360 tour viewpoints with optional filters."""
    from models.panoramas import get_all_panoramas, get_panoramas_by_district, get_panoramas_by_category
    district = request.args.get('district')
    category = request.args.get('category')

    if district:
        panos = get_panoramas_by_district(district)
    elif category:
        panos = get_panoramas_by_category(category)
    else:
        panos = get_all_panoramas()

    return jsonify({
        'status': 'success',
        'count': len(panos),
        'panoramas': panos
    })


@api_bp.route('/panoramas/<slug>', methods=['GET'])
def api_get_panorama_detail(slug):
    """JSON API returning metadata, photo sphere image URL, and audio ties for a 360 viewpoint."""
    from models.panoramas import get_panorama_by_slug
    pano = get_panorama_by_slug(slug)
    if not pano:
        return jsonify({'status': 'not_found', 'message': f'Panorama viewpoint not found: {slug}'}), 404
    return jsonify({
        'status': 'success',
        'panorama': pano
    })


@api_bp.route('/panoramas/<slug>/hotspots', methods=['GET'])
def api_get_panorama_hotspots(slug):
    """JSON API returning interactive pitch/yaw coordinate hotspots for a 360 viewpoint."""
    from models.panoramas import get_panorama_hotspots, get_panorama_by_slug
    pano = get_panorama_by_slug(slug)
    if not pano:
        return jsonify({'status': 'not_found', 'message': f'Panorama not found: {slug}'}), 404
    hotspots = get_panorama_hotspots(slug)
    return jsonify({
        'status': 'success',
        'slug': slug,
        'count': len(hotspots),
        'hotspots': hotspots
    })

@api_bp.route('/gastronomy/dishes', methods=['GET'])
def api_get_dishes():
    """JSON API returning traditional Bihar culinary specialties and GI delicacies."""
    from models.gastronomy import get_all_dishes, get_dishes_by_district, get_dishes_by_dietary, get_gi_tagged_dishes
    district = request.args.get('district')
    dietary = request.args.get('dietary')
    gi_only = request.args.get('gi', '').lower() in ['1', 'true', 'yes']

    if gi_only:
        dishes = get_gi_tagged_dishes()
    elif district:
        dishes = get_dishes_by_district(district)
    elif dietary:
        dishes = get_dishes_by_dietary(dietary)
    else:
        dishes = get_all_dishes()

    return jsonify({
        'status': 'success',
        'count': len(dishes),
        'dishes': dishes
    })


@api_bp.route('/gastronomy/dishes/<slug>', methods=['GET'])
def api_get_dish_detail(slug):
    """JSON API returning ingredients, history, and verified eateries for a dish."""
    from models.gastronomy import get_dish_by_slug
    dish = get_dish_by_slug(slug)
    if not dish:
        return jsonify({'status': 'not_found', 'message': f'Dish not found: {slug}'}), 404
    return jsonify({
        'status': 'success',
        'dish': dish
    })


@api_bp.route('/gastronomy/trails', methods=['GET'])
def api_get_culinary_trails():
    """JSON API returning curated regional gastronomy trail itineraries."""
    from models.gastronomy import get_culinary_trails
    return jsonify({
        'status': 'success',
        'trails': get_culinary_trails()
    })

@api_bp.route('/wildlife/sanctuaries', methods=['GET'])
def api_get_sanctuaries():
    """JSON API returning Bihar national parks, tiger reserves, and bird sanctuaries."""
    from models.wildlife import get_all_sanctuaries, get_sanctuaries_by_district, get_ramsar_wetlands
    district = request.args.get('district')
    ramsar_only = request.args.get('ramsar', '').lower() in ['1', 'true', 'yes']

    if ramsar_only:
        sanctuaries = get_ramsar_wetlands()
    elif district:
        sanctuaries = get_sanctuaries_by_district(district)
    else:
        sanctuaries = get_all_sanctuaries()

    return jsonify({
        'status': 'success',
        'count': len(sanctuaries),
        'sanctuaries': sanctuaries
    })


@api_bp.route('/wildlife/sanctuaries/<slug>', methods=['GET'])
def api_get_sanctuary_detail(slug):
    """JSON API returning key fauna, safari options, and permit details for a sanctuary."""
    from models.wildlife import get_sanctuary_by_slug
    sanctuary = get_sanctuary_by_slug(slug)
    if not sanctuary:
        return jsonify({'status': 'not_found', 'message': f'Sanctuary not found: {slug}'}), 404
    return jsonify({
        'status': 'success',
        'sanctuary': sanctuary
    })


@api_bp.route('/wildlife/guidelines', methods=['GET'])
def api_get_safari_guidelines():
    """JSON API returning safari and forest conservation guidelines."""
    from models.wildlife import get_safari_guidelines
    return jsonify({
        'status': 'success',
        'guidelines': get_safari_guidelines()
    })


@api_bp.route('/wildlife/species', methods=['GET'])
def api_get_species_list():
    """JSON API returning tracked key wildlife and endangered species."""
    from models.wildlife import get_endangered_species_list
    return jsonify({
        'status': 'success',
        'species': get_endangered_species_list()
    })

@api_bp.route('/volunteer/programs', methods=['GET'])
def api_get_volunteer_programs():
    """JSON API returning active rural immersion and volunteer opportunities."""
    from models.volunteer import get_all_programs, get_programs_by_district
    district = request.args.get('district')
    programs = get_programs_by_district(district) if district else get_all_programs()
    return jsonify({
        'status': 'success',
        'count': len(programs),
        'programs': programs
    })


@api_bp.route('/volunteer/programs/<slug>', methods=['GET'])
def api_get_volunteer_program_detail(slug):
    """JSON API returning details, skills needed, and impact goals for an immersion program."""
    from models.volunteer import get_program_by_slug
    prog = get_program_by_slug(slug)
    if not prog:
        return jsonify({'status': 'not_found', 'message': f'Program not found: {slug}'}), 404
    return jsonify({
        'status': 'success',
        'program': prog
    })


@api_bp.route('/volunteer/apply', methods=['POST'])
def api_apply_volunteer_program():
    """JSON API to submit a volunteer registration application."""
    from models.volunteer import validate_volunteer_application, calculate_skill_match_score
    data = request.get_json(silent=True) or request.form
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip()
    phone = (data.get('phone') or '').strip()
    prog_slug = (data.get('program_slug') or '').strip()
    motivation = (data.get('motivation') or '').strip()
    skills_raw = data.get('skills', [])
    if isinstance(skills_raw, str):
        skills = [s.strip() for s in skills_raw.split(',') if s.strip()]
    else:
        skills = skills_raw

    is_valid, msg = validate_volunteer_application(name, email, phone, prog_slug, motivation, skills)
    if not is_valid:
        return jsonify({'status': 'error', 'message': msg}), 400

    match_score = calculate_skill_match_score(skills, prog_slug)
    app_id = f'HY-VOL-{abs(hash(email + prog_slug)) % 100000:05d}'

    return jsonify({
        'status': 'success',
        'message': f'Thank you {name}! Your immersion application has been received.',
        'application_id': app_id,
        'skill_match_score_pct': match_score,
        'program_slug': prog_slug
    })

@api_bp.route('/universal-search', methods=['GET'])
def api_universal_search():
    """Universal cross-domain search endpoint matching places, circuits, crafts, food, and wildlife."""
    from models.search_engine import search_cross_domain_heritage
    q = request.args.get('q', '').strip()
    limit = request.args.get('limit', 12, type=int)
    results = search_cross_domain_heritage(q, limit=limit)
    return jsonify({
        'status': 'success',
        'query': q,
        'count': len(results),
        'results': results
    })

@api_bp.route('/archaeology/sites', methods=['GET'])
def api_get_archaeological_sites():
    """JSON API returning ancient excavation sites, Ashokan pillars, and epigraphy."""
    from models.archaeology import get_all_archaeological_sites, get_sites_by_district, get_sites_by_period, get_ashokan_edicts
    district = request.args.get('district')
    period = request.args.get('period')
    ashokan_only = request.args.get('ashokan', '').lower() in ['1', 'true', 'yes']

    if ashokan_only:
        sites = get_ashokan_edicts()
    elif district:
        sites = get_sites_by_district(district)
    elif period:
        sites = get_sites_by_period(period)
    else:
        sites = get_all_archaeological_sites()

    return jsonify({
        'status': 'success',
        'count': len(sites),
        'sites': sites
    })


@api_bp.route('/archaeology/sites/<slug>', methods=['GET'])
def api_get_archaeological_site_detail(slug):
    """JSON API returning excavation highlights, script, and museum preservation for a site."""
    from models.archaeology import get_site_by_slug
    site = get_site_by_slug(slug)
    if not site:
        return jsonify({'status': 'not_found', 'message': f'Archaeological site not found: {slug}'}), 404
    return jsonify({
        'status': 'success',
        'site': site
    })


@api_bp.route('/archaeology/chronology', methods=['GET'])
def api_get_epigraphy_chronology():
    """JSON API returning chronological historical eras and primary scripts."""
    from models.archaeology import get_epigraphy_chronology
    return jsonify({
        'status': 'success',
        'chronology': get_epigraphy_chronology()
    })

@api_bp.route('/archaeology/coins', methods=['GET'])
def api_get_numismatic_hoards():
    """JSON API returning ancient punch-marked silver coins, Gupta gold dinars, and terracotta seals."""
    from models.archaeology import get_all_numismatic_hoards
    hoards = get_all_numismatic_hoards()
    return jsonify({
        'status': 'success',
        'count': len(hoards),
        'hoards': hoards
    })


@api_bp.route('/archaeology/coins/<slug>', methods=['GET'])
def api_get_numismatic_hoard_detail(slug):
    """JSON API returning symbols, weight standard, and museum location for a coin hoard."""
    from models.archaeology import get_coin_hoard_by_slug
    hoard = get_coin_hoard_by_slug(slug)
    if not hoard:
        return jsonify({'status': 'not_found', 'message': f'Coin hoard not found: {slug}'}), 404
    return jsonify({
        'status': 'success',
        'hoard': hoard
    })

@api_bp.route('/archaeology/inscriptions', methods=['GET'])
def api_get_epigraphical_inscriptions():
    """JSON API returning ancient rock edicts, Brahmi translations, and copper-plate royal charters."""
    from models.archaeology import get_all_epigraphical_inscriptions
    inscriptions = get_all_epigraphical_inscriptions()
    return jsonify({
        'status': 'success',
        'count': len(inscriptions),
        'inscriptions': inscriptions
    })


@api_bp.route('/archaeology/inscriptions/<slug>', methods=['GET'])
def api_get_epigraphical_inscription_detail(slug):
    """JSON API returning Prakrit/Sanskrit text, English translation, and historical significance."""
    from models.archaeology import get_inscription_by_slug
    ins = get_inscription_by_slug(slug)
    if not ins:
        return jsonify({'status': 'not_found', 'message': f'Inscription not found: {slug}'}), 404
    return jsonify({
        'status': 'success',
        'inscription': ins
    })

@api_bp.route('/weather/districts', methods=['GET'])
def api_get_all_district_weather():
    """JSON API returning district meteorological normals, AQI categories, and climate zones."""
    from models.weather import get_all_district_weather
    districts = get_all_district_weather()
    return jsonify({
        'status': 'success',
        'count': len(districts),
        'districts': districts
    })


@api_bp.route('/weather/districts/<slug>', methods=['GET'])
def api_get_district_weather_detail(slug):
    """JSON API returning microclimate, rainfall, summer/winter temperatures, and packing advice."""
    from models.weather import get_district_weather_by_slug
    weather = get_district_weather_by_slug(slug)
    if not weather:
        return jsonify({'status': 'not_found', 'message': f'Weather profile not found: {slug}'}), 404
    return jsonify({
        'status': 'success',
        'weather': weather
    })


@api_bp.route('/weather/packing-advice', methods=['GET'])
def api_get_packing_advice():
    """JSON API returning clothing and gear recommendations based on month and district microclimate."""
    from models.weather import get_seasonal_packing_advice
    district = request.args.get('district', 'patna')
    month = request.args.get('month')
    advice = get_seasonal_packing_advice(district, month)
    return jsonify({
        'status': 'success',
        'district': district,
        'advice': advice
    })

@api_bp.route('/weather/phenomena', methods=['GET'])
def api_get_seasonal_phenomena():
    """JSON API returning fog visibility indices, waterfall surges, and seasonal photography ratings."""
    from models.weather import get_all_seasonal_phenomena, get_phenomena_by_month
    month = request.args.get('month')
    phenomena = get_phenomena_by_month(month) if month else get_all_seasonal_phenomena()
    return jsonify({
        'status': 'success',
        'count': len(phenomena),
        'phenomena': phenomena
    })

@api_bp.route('/weather/alerts', methods=['GET'])
def api_get_weather_emergency_alerts():
    """JSON API returning lightning, flood, and fog emergency protocols and disaster helplines."""
    from models.weather import get_all_weather_emergency_alerts
    alerts = get_all_weather_emergency_alerts()
    return jsonify({
        'status': 'success',
        'count': len(alerts),
        'alerts': alerts
    })

@api_bp.route('/performing-arts', methods=['GET'])
def api_get_performing_arts():
    """JSON API returning traditional folk dances, theater forms, and music genres."""
    from models.performing_arts import get_all_performing_arts, get_arts_by_region
    region = request.args.get('region')
    arts = get_arts_by_region(region) if region else get_all_performing_arts()
    return jsonify({
        'status': 'success',
        'count': len(arts),
        'performing_arts': arts
    })


@api_bp.route('/performing-arts/<slug>', methods=['GET'])
def api_get_performing_art_detail(slug):
    """JSON API returning cultural backstory, instruments, and themes for an art form."""
    from models.performing_arts import get_art_by_slug
    art = get_art_by_slug(slug)
    if not art:
        return jsonify({'status': 'not_found', 'message': f'Art form not found: {slug}'}), 404
    return jsonify({
        'status': 'success',
        'art': art
    })


@api_bp.route('/performing-arts/instruments', methods=['GET'])
def api_get_folk_instruments():
    """JSON API returning traditional musical instruments used in Bihar folk culture."""
    from models.performing_arts import get_all_folk_instruments
    instruments = get_all_folk_instruments()
    return jsonify({
        'status': 'success',
        'count': len(instruments),
        'instruments': instruments
    })

@api_bp.route('/performing-arts/guilds', methods=['GET'])
def api_get_folk_guilds():
    """JSON API returning traditional folk performance troupes, repertories, and artist mandalis."""
    from models.performing_arts import get_all_folk_guilds
    guilds = get_all_folk_guilds()
    return jsonify({
        'status': 'success',
        'count': len(guilds),
        'guilds': guilds
    })


@api_bp.route('/performing-arts/guilds/<guild_id>', methods=['GET'])
def api_get_folk_guild_detail(guild_id):
    """JSON API returning troupe contact notes, lead exponents, and performance seasons."""
    from models.performing_arts import get_guild_by_id
    guild = get_guild_by_id(guild_id)
    if not guild:
        return jsonify({'status': 'not_found', 'message': f'Artist guild not found: {guild_id}'}), 404
    return jsonify({
        'status': 'success',
        'guild': guild
    })

@api_bp.route('/performing-arts/seasons', methods=['GET'])
def api_get_performance_seasons():
    """JSON API returning seasonal performance windows, festival contexts, and key genres."""
    from models.performing_arts import get_performance_seasons
    seasons = get_performance_seasons()
    return jsonify({
        'status': 'success',
        'count': len(seasons),
        'seasons': seasons
    })