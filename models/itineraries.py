"""
HiddenYatra — Saved Itineraries Database Operations
Handles saving and retrieving user itineraries.
"""
import json
import logging
from models.connection import get_cursor

logger = logging.getLogger(__name__)


def save_itinerary(session_id, user_id, title, days, companion, budget, items_data):
    """Save an itinerary."""
    with get_cursor(commit=True) as cur:
        cur.execute("""
            INSERT INTO saved_itineraries (session_id, user_id, title, days, companion, budget, items_data)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            session_id, user_id, title, days, companion, budget,
            json.dumps(items_data) if not isinstance(items_data, str) else items_data
        ))
        return cur.lastrowid


create_itinerary = save_itinerary


def get_user_itineraries(session_id, user_id=None):
    """Get saved itineraries for a session or user."""
    with get_cursor() as cur:
        if user_id:
            cur.execute("""
                SELECT * FROM saved_itineraries
                WHERE user_id = %s OR session_id = %s
                ORDER BY created_at DESC
            """, (user_id, session_id))
        else:
            cur.execute("""
                SELECT * FROM saved_itineraries
                WHERE session_id = %s
                ORDER BY created_at DESC
            """, (session_id,))
        rows = cur.fetchall()

    result = []
    for r in rows:
        r_dict = dict(r)
        if isinstance(r_dict.get('items_data'), str):
            try:
                r_dict['items_data'] = json.loads(r_dict['items_data'])
            except (json.JSONDecodeError, TypeError):
                r_dict['items_data'] = []
        result.append(r_dict)
    return result


get_itineraries = get_user_itineraries


def delete_itinerary(itinerary_id):
    """Delete a saved itinerary."""
    with get_cursor(commit=True) as cur:
        cur.execute("DELETE FROM saved_itineraries WHERE id = %s", (itinerary_id,))


def get_itinerary_by_id(itinerary_id, session_id=None):
    """Get a saved itinerary by ID."""
    with get_cursor() as cur:
        cur.execute("SELECT * FROM saved_itineraries WHERE id = %s", (itinerary_id,))
        row = cur.fetchone()
        if not row:
            return None
        r_dict = dict(row)
        if isinstance(r_dict.get('items_data'), str):
            try:
                r_dict['items_data'] = json.loads(r_dict['items_data'])
            except (json.JSONDecodeError, TypeError):
                r_dict['items_data'] = []
        return r_dict


def get_itinerary_items(itinerary_id):
    """Get itinerary items for a given itinerary."""
    it = get_itinerary_by_id(itinerary_id)
    if not it:
        return []
    return it.get('items_data', [])


def add_itinerary_item(itinerary_id, day, place_id=None, notes=None, place_name=None):
    """Add an item to a saved itinerary."""
    it = get_itinerary_by_id(itinerary_id)
    if not it:
        return False
    items = it.get('items_data', [])
    items.append({'day': day, 'place_id': place_id, 'notes': notes, 'place_name': place_name})
    with get_cursor(commit=True) as cur:
        cur.execute("UPDATE saved_itineraries SET items_data = %s WHERE id = %s",
                    (json.dumps(items), itinerary_id))
    return True


def remove_itinerary_item(itinerary_id, item_index):
    """Remove an item from a saved itinerary by index."""
    it = get_itinerary_by_id(itinerary_id)
    if not it:
        return False
    items = it.get('items_data', [])
    if 0 <= item_index < len(items):
        items.pop(item_index)
        with get_cursor(commit=True) as cur:
            cur.execute("UPDATE saved_itineraries SET items_data = %s WHERE id = %s",
                        (json.dumps(items), itinerary_id))
        return True
    return False






def get_pacing_config(pace='balanced'):
    """Return pacing preferences: slots per day, max travel distance km, rest duration min."""
    pacing_presets = {
        'relaxed': {'places_per_day': 2, 'max_distance_km': 40, 'rest_minutes': 90, 'label': 'Relaxed & Leisurely'},
        'balanced': {'places_per_day': 3, 'max_distance_km': 80, 'rest_minutes': 60, 'label': 'Balanced Explorer'},
        'fast': {'places_per_day': 5, 'max_distance_km': 150, 'rest_minutes': 30, 'label': 'Fast-Paced & Intensive'}
    }
    return pacing_presets.get(pace, pacing_presets['balanced'])


def calculate_daily_slots(total_days, pace='balanced'):
    """Compute daily place allocation slots for trip duration."""
    config = get_pacing_config(pace)
    slots = []
    for day in range(1, total_days + 1):
        slots.append({
            'day': day,
            'max_places': config['places_per_day'],
            'target_distance_km': config['max_distance_km'],
            'pace_label': config['label']
        })
    return slots


def calculate_itinerary_budget(days=3, companion_type='solo', budget_tier='moderate'):
    """Calculate estimated trip budget with category breakdowns (in INR)."""
    tier_multipliers = {
        'budget': {'stay': 800, 'food': 400, 'transport': 300, 'activities': 200},
        'moderate': {'stay': 2200, 'food': 900, 'transport': 700, 'activities': 500},
        'luxury': {'stay': 5500, 'food': 2000, 'transport': 1800, 'activities': 1200}
    }
    companion_multipliers = {
        'solo': 1.0,
        'couple': 1.6,
        'family': 2.8,
        'friends': 3.2
    }

    rates = tier_multipliers.get(budget_tier, tier_multipliers['moderate'])
    comp_mult = companion_multipliers.get(companion_type, 1.0)

    daily_stay = int(rates['stay'] * comp_mult)
    daily_food = int(rates['food'] * comp_mult)
    daily_trans = int(rates['transport'] * comp_mult)
    daily_acts = int(rates['activities'] * comp_mult)

    total_stay = daily_stay * max(1, days - 1)
    total_food = daily_food * days
    total_trans = daily_trans * days
    total_acts = daily_acts * days

    subtotal = total_stay + total_food + total_trans + total_acts
    contingency = int(subtotal * 0.10)
    total = subtotal + contingency

    return {
        'days': days,
        'companion_type': companion_type,
        'budget_tier': budget_tier,
        'breakdown': {
            'accommodation': total_stay,
            'food_dining': total_food,
            'transportation': total_trans,
            'entry_activities': total_acts,
            'emergency_buffer': contingency
        },
        'daily_average': int(total / days) if days > 0 else total,
        'total_estimated_inr': total
    }


def get_itinerary_cultural_highlights(travel_month=None, districts=None):
    """
    Find relevant cultural festivals and thematic circuits matching travel month and districts.
    """
    highlights = {
        'festivals': [],
        'circuits': []
    }
    try:
        from models.festivals import get_festivals_by_month, get_all_festivals
        if travel_month:
            festivals = get_festivals_by_month(travel_month)
        else:
            festivals = get_all_festivals()[:3]
        highlights['festivals'] = festivals
    except Exception:
        pass

    try:
        from models.circuits import get_all_circuits
        all_circuits = get_all_circuits()
        if districts:
            dist_set = set(d.lower().strip() for d in districts if d)
            matched = []
            for c in all_circuits:
                c_districts = {s['district'].lower().strip() for s in c.get('stops', [])}
                if any(any(d in cd for cd in c_districts) for d in dist_set):
                    matched.append(c)
            highlights['circuits'] = matched if matched else all_circuits[:2]
        else:
            highlights['circuits'] = all_circuits[:2]
    except Exception:
        pass

    return highlights