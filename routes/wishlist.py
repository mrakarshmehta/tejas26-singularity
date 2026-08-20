"""Wishlist routes — session-based, no login required."""
import logging
from flask import Blueprint, render_template, request, session, jsonify

from models.database import (
    add_to_wishlist, remove_from_wishlist,
    get_wishlist, get_wishlist_count, is_wishlisted
)
from utils import csrf_required, get_session_id as _get_session_id

logger = logging.getLogger(__name__)
wishlist_bp = Blueprint('wishlist', __name__)


@wishlist_bp.route('/wishlist')
def wishlist_page():
    sid = _get_session_id()
    places = get_wishlist(sid)
    return render_template('wishlist.html', places=places)


@wishlist_bp.route('/wishlist/add/<int:place_id>', methods=['POST'])
@wishlist_bp.route('/wishlist/<int:place_id>/add', methods=['POST'])
@csrf_required
def add_wish(place_id):
    if place_id <= 0:
        return jsonify({'error': 'Invalid place ID', 'status': 'error', 'wishlisted': False}), 400
    sid = _get_session_id()
    add_to_wishlist(sid, place_id)
    count = get_wishlist_count(sid)
    return jsonify({'status': 'added', 'count': count, 'wishlisted': True})


@wishlist_bp.route('/wishlist/remove/<int:place_id>', methods=['POST'])
@wishlist_bp.route('/wishlist/<int:place_id>/remove', methods=['POST'])
@csrf_required
def remove_wish(place_id):
    if place_id <= 0:
        return jsonify({'error': 'Invalid place ID', 'status': 'error', 'wishlisted': False}), 400
    sid = _get_session_id()
    remove_from_wishlist(sid, place_id)
    count = get_wishlist_count(sid)
    return jsonify({'status': 'removed', 'count': count, 'wishlisted': False})


@wishlist_bp.route('/wishlist/toggle/<int:place_id>', methods=['POST'])
@wishlist_bp.route('/wishlist/<int:place_id>/toggle', methods=['POST'])
@csrf_required
def toggle_wish(place_id):
    if place_id <= 0:
        return jsonify({'error': 'Invalid place ID', 'status': 'error', 'wishlisted': False}), 400
    sid = _get_session_id()
    if is_wishlisted(sid, place_id):
        remove_from_wishlist(sid, place_id)
        wishlisted = False
        status = 'removed'
    else:
        add_to_wishlist(sid, place_id)
        wishlisted = True
        status = 'added'
    count = get_wishlist_count(sid)
    return jsonify({'status': status, 'count': count, 'wishlisted': wishlisted})


@wishlist_bp.route('/wishlist/status/<int:place_id>')
@wishlist_bp.route('/wishlist/<int:place_id>/status')
def wish_status(place_id):
    if place_id <= 0:
        return jsonify({'error': 'Invalid place ID', 'wishlisted': False}), 400
    sid = _get_session_id()
    wishlisted = is_wishlisted(sid, place_id)
    return jsonify({'wishlisted': wishlisted})
