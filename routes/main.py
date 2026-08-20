"""Public page routes — home, browse, search, district, block, explore map, food & culture."""
from flask import Blueprint, render_template, request
from models.database import (
    get_places_by_filter,
    get_all_states, get_state_by_slug, get_featured_places,
    get_recent_places, get_places_by_state, get_districts_by_state,
    get_blocks_by_district, get_blocks_grouped_by_district,
    get_district_by_slug, get_block_by_slug,
    get_places_by_district, get_places_by_block, count_places_in_block,
    search_places, search_all, smart_search, get_stats, get_places_for_map,
    get_trending_places, get_district_foods, get_all_district_foods_by_state,
    get_hero_media_active, get_hero_settings,
    get_districts_for_homepage, get_featured_districts,
    get_trending_for_homepage, get_homepage_sections,
    count_places_in_district, instant_search,
    PLACE_CATEGORIES
)

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Home page — Bihar-focused with hero, districts, trending, food preview."""
    featured = get_featured_places(limit=8)
    states = get_all_states()
    stats = get_stats()

    # Dynamic districts from admin ordering
    districts = get_districts_for_homepage(limit=12)
    featured_districts = get_featured_districts()

    # Dynamic trending: admin-managed if available, fallback to auto
    trending = get_trending_for_homepage(limit=8)
    if not trending:
        trending = get_trending_places(limit=8)

    # Hero media from admin
    hero_media = get_hero_media_active()
    hero_settings = get_hero_settings()

    # Homepage section settings
    hp_sections = get_homepage_sections()
    sections = {s['section_key']: s for s in hp_sections}

    # Get Bihar state
    bihar = get_state_by_slug('bihar')

    return render_template('index.html',
                           featured=featured,
                           trending=trending,
                           states=states,
                           stats=stats,
                           districts=districts,
                           featured_districts=featured_districts,
                           bihar=bihar,
                           categories=PLACE_CATEGORIES,
                           hero_media=hero_media,
                           hero_settings=hero_settings,
                           sections=sections)


@main_bp.route('/browse')
def browse():
    """Browse all states."""
    states = get_all_states()
    return render_template('browse.html', states=states)


@main_bp.route('/state/<slug>')
def state_detail(slug):
    """State detail page with hierarchical district/block display."""
    state = get_state_by_slug(slug)
    if not state:
        return render_template('404.html'), 404

    places = get_places_by_state(state['id'])
    districts = get_districts_by_state(state['id'])

    # Enrich districts with blocks data (single batch query instead of N+1)
    blocks_map = get_blocks_grouped_by_district(state['id'])
    for district in districts:
        district['blocks'] = blocks_map.get(district['id'], [])

    # Group places by category
    category_filter = request.args.get('category', '')
    if category_filter:
        places = [p for p in places if p['category'] == category_filter]

    stats = get_stats()

    return render_template('state.html',
                           state=state,
                           places=places,
                           districts=districts,
                           categories=PLACE_CATEGORIES,
                           current_category=category_filter,
                           stats=stats)


@main_bp.route('/state/<state_slug>/<district_slug>')
def district_detail(state_slug, district_slug):
    """District detail page showing blocks, places, foods."""
    state = get_state_by_slug(state_slug)
    if not state:
        return render_template('404.html'), 404

    district = get_district_by_slug(state['id'], district_slug)
    if not district:
        return render_template('404.html'), 404

    page = request.args.get('page', 1, type=int)
    sort_by = request.args.get('sort', 'popular')
    per_page = 100
    offset = (page - 1) * per_page
    total = count_places_in_district(district['id'])
    blocks = get_blocks_by_district(district['id'])
    places = get_places_by_district(district['id'], limit=per_page, offset=offset, sort_by=sort_by)
    foods = get_district_foods(district['id'])

    # Related districts (same state, excluding current)
    all_districts = get_districts_by_state(state['id'])
    related_districts = [d for d in all_districts if d['id'] != district['id']]

    category_counts = {
        'total': total,
        'temples': sum(1 for p in places if p.get('category') in ['temple']),
        'hills': sum(1 for p in places if p.get('category') in ['mountain', 'hill']),
        'waterfalls': sum(1 for p in places if p.get('category') in ['waterfall', 'lake']),
        'historical': sum(1 for p in places if p.get('category') in ['historical']),
        'religious': sum(1 for p in places if p.get('category') in ['temple', 'cultural', 'religious']),
    }

    return render_template('district.html',
                           state=state,
                           district=district,
                           blocks=blocks,
                           places=places,
                           foods=foods,
                           related_districts=related_districts,
                           category_counts=category_counts,
                           page=page,
                           per_page=per_page,
                           total=total,
                           sort_by=sort_by)


@main_bp.route('/state/<state_slug>/<district_slug>/<block_slug>')
def block_detail(state_slug, district_slug, block_slug):
    """Block detail page showing places within the block."""
    state = get_state_by_slug(state_slug)
    if not state:
        return render_template('404.html'), 404

    district = get_district_by_slug(state['id'], district_slug)
    if not district:
        return render_template('404.html'), 404

    block = get_block_by_slug(district['id'], block_slug)
    if not block:
        return render_template('404.html'), 404

    page = request.args.get('page', 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page
    places = get_places_by_block(block['id'], limit=per_page, offset=offset)
    total = count_places_in_block(block['id'])

    return render_template('block.html',
                           state=state,
                           district=district,
                           block=block,
                           places=places,
                           page=page,
                           per_page=per_page,
                           total=total)


@main_bp.route('/search')
def search():
    """Enhanced search results page with hierarchical results and fuzzy 'did you mean' support."""
    query = request.args.get('q', '').strip()
    results = {'states': [], 'districts': [], 'blocks': [], 'places': [], 'foods': []}
    smart = None
    did_you_mean = None
    if query:
        results = search_all(query, limit=30)
        smart_raw = smart_search(query, limit=10)
        # smart_search returns a dict like {'query': ..., 'places': [...], 'foods': [...], 'hotels': [...]}
        # Extract just the places list for the template's place_card rendering
        if smart_raw and isinstance(smart_raw, dict):
            smart = smart_raw.get('places', [])
        elif isinstance(smart_raw, list):
            smart = smart_raw

        # Get fuzzy "did you mean" from instant search
        instant_results = instant_search(query, limit=3)
        if instant_results and instant_results[0].get('match_type') == 'fuzzy':
            did_you_mean = instant_results[0]['name']

    return render_template('search.html', query=query, results=results, smart=smart, did_you_mean=did_you_mean)


@main_bp.route('/explore')
def explore_map():
    """Full-screen interactive map with all places."""
    from config import GOOGLE_MAPS_API_KEY, GOOGLE_MAPS_MAP_ID, MAP_ENGINE
    states = get_all_states()
    bihar = get_state_by_slug('bihar')
    districts = []
    if bihar:
        districts = get_districts_by_state(bihar['id'])
    places = get_places_for_map()
    return render_template('explore_map.html',
                           states=states,
                           districts=districts,
                           categories=PLACE_CATEGORIES,
                           places=places,
                           map_engine=MAP_ENGINE,
                           skip_base_leaflet=(MAP_ENGINE == 'google'),
                           google_maps_api_key=GOOGLE_MAPS_API_KEY if MAP_ENGINE == 'google' else '',
                           google_maps_map_id=GOOGLE_MAPS_MAP_ID if MAP_ENGINE == 'google' else '')


@main_bp.route('/food-culture')
def food_culture():
    """Food & Culture page — Bihar focused."""
    bihar = get_state_by_slug('bihar')
    foods = []
    districts = []
    if bihar:
        foods = get_all_district_foods_by_state(bihar['id'])
        districts = get_districts_by_state(bihar['id'])
    return render_template('food_culture.html',
                           bihar=bihar,
                           foods=foods,
                           districts=districts)


@main_bp.route('/offline')
def offline_fallback():
    """Render the offline PWA fallback page."""
    return render_template('offline.html'), 200


@main_bp.route('/circuits')
def circuits_browse():
    """Browse curated thematic heritage trails and pilgrimage circuits."""
    from models.circuits import get_all_circuits
    theme_filter = request.args.get('theme')
    if theme_filter:
        from models.circuits import filter_circuits_by_theme
        circuits = filter_circuits_by_theme(theme_filter)
    else:
        circuits = get_all_circuits()
    return render_template('circuits.html', circuits=circuits, active_theme=theme_filter or 'all')


@main_bp.route('/circuit/<slug>')
def circuit_detail(slug):
    """View details, map stops, and day-by-day itinerary of a thematic circuit."""
    from models.circuits import get_circuit_by_slug, calculate_circuit_metrics
    circuit = get_circuit_by_slug(slug)
    if not circuit:
        abort(404)
    metrics = calculate_circuit_metrics(slug)
    return render_template('circuit_detail.html', circuit=circuit, metrics=metrics)


@main_bp.route('/festivals')
def festivals_calendar():
    """Display seasonal festivals and cultural celebrations across Bihar."""
    from models.festivals import get_all_festivals, get_festivals_by_month, get_festivals_by_district
    month_arg = request.args.get('month')
    district_arg = request.args.get('district')

    if month_arg:
        festivals = get_festivals_by_month(month_arg)
    elif district_arg:
        festivals = get_festivals_by_district(district_arg)
    else:
        festivals = get_all_festivals()

    return render_template(
        'festivals.html',
        festivals=festivals,
        selected_month=month_arg,
        selected_district=district_arg
    )


@main_bp.route('/festival/<slug>')
def festival_detail(slug):
    """View dedicated celebration details and visitor guide for a specific festival."""
    from models.festivals import get_festival_by_slug
    fest = get_festival_by_slug(slug)
    if not fest:
        abort(404)
    return render_template('festival_detail.html', festival=fest)


@main_bp.route('/crafts')
def crafts_directory():
    """Browse Bihar's GI-tagged handicrafts and authentic artisan centers."""
    from models.crafts import get_all_crafts, get_crafts_by_district
    district_filter = request.args.get('district')
    if district_filter:
        crafts = get_crafts_by_district(district_filter)
    else:
        crafts = get_all_crafts()
    return render_template('crafts.html', crafts=crafts, active_district=district_filter or 'all')


@main_bp.route('/craft/<slug>')
def craft_detail(slug):
    """View craft history, GI certification, materials, and artisan centers."""
    from models.crafts import get_craft_by_slug, get_artisan_centers_for_craft
    craft = get_craft_by_slug(slug)
    if not craft:
        abort(404)
    centers = get_artisan_centers_for_craft(slug)
    return render_template('craft_detail.html', craft=craft, artisan_centers=centers)


@main_bp.route('/eco-pledge')
def eco_pledge():
    """Showcase Bihar responsible tourism guidelines and green traveler pledge."""
    from models.eco import get_responsible_travel_code
    pillars = get_responsible_travel_code()
    return render_template('eco_pledge.html', pillars=pillars)


@main_bp.route('/safety')
def traveler_safety():
    """Emergency contacts, tourist police desks, 24/7 hospitals, and traveler safety guidelines."""
    from models.safety import (
        get_statewide_helplines,
        get_all_district_safety,
        get_district_safety,
        get_medical_facilities,
        get_safety_guidelines
    )
    district_filter = (request.args.get('district') or '').lower().strip()
    statewide = get_statewide_helplines()
    guidelines = get_safety_guidelines()
    all_districts = get_all_district_safety()

    if district_filter and district_filter in all_districts:
        selected_district_safety = get_district_safety(district_filter)
        medical_list = get_medical_facilities(district_filter)
    else:
        selected_district_safety = None
        medical_list = get_medical_facilities()
        district_filter = 'all'

    return render_template(
        'safety.html',
        statewide=statewide,
        all_districts=all_districts,
        selected_district=selected_district_safety,
        active_district=district_filter,
        medical_facilities=medical_list,
        guidelines=guidelines
    )