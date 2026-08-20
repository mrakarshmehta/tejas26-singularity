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
