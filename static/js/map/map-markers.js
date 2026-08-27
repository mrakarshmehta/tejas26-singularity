/* ═══════════════════════════════════════════════════════════════════
   HiddenYatra — MapMarkers (Shared Marker Factory)
   Provides unified marker creation for both 2D (Leaflet) and 3D
   (MapLibre) engines using the same style/icon definitions.
   ═══════════════════════════════════════════════════════════════════ */

(function (root) {
  'use strict';

  /* ── Category Styling Constants ──────────────────── */

  const CATEGORY_COLORS = {
    temple:        '#f59e0b',
    waterfall:     '#06b6d4',
    nature:        '#10b981',
    historical:    '#8b5cf6',
    fort:          '#d97706',
    religious:     '#f97316',
    hidden_gem:    '#ec4899',
    tourist_spot:  '#6366f1',
    park:          '#22c55e',
    lake:          '#0284c7',
    cultural:      '#8b5cf6',
    mountain:      '#6366f1',
    museum:        '#d97706',
    hotel:         '#2563eb',
    homestay:      '#059669',
    default:       '#6366f1',
  };

  const CATEGORY_EMOJIS = {
    temple:        '🛕',
    waterfall:     '💧',
    nature:        '🌿',
    historical:    '🏛️',
    fort:          '🏰',
    religious:     '🙏',
    hidden_gem:    '💎',
    tourist_spot:  '📍',
    park:          '🌳',
    lake:          '🌊',
    cultural:      '🎭',
    mountain:      '⛰️',
    museum:        '🏛️',
    hotel:         '🏨',
    homestay:      '🏡',
    default:       '📍',
  };

  const CATEGORY_LABELS = {
    temple:        'Temple',
    waterfall:     'Waterfall',
    nature:        'Nature',
    historical:    'Historical',
    fort:          'Fort',
    religious:     'Religious',
    hidden_gem:    'Hidden Gem',
    tourist_spot:  'Tourist Spot',
    park:          'Park',
    lake:          'Lake',
    cultural:      'Cultural',
    mountain:      'Mountain',
    museum:        'Museum',
    hotel:         'Hotel',
    homestay:      'Homestay',
  };

  /* ── Shared Marker Factory ───────────────────────── */

  const MapMarkers = {

    /**
     * Get the color for a category.
     * @param {string} category
     * @returns {string} Hex color
     */
    getColor(category) {
      return CATEGORY_COLORS[category] || CATEGORY_COLORS.default;
    },

    /**
     * Get the emoji for a category.
     * @param {string} category
     * @returns {string} Emoji character
     */
    getEmoji(category) {
      return CATEGORY_EMOJIS[category] || CATEGORY_EMOJIS.default;
    },

    /**
     * Get the human-readable label for a category.
     * @param {string} category
     * @returns {string}
     */
    getLabel(category) {
      return CATEGORY_LABELS[category] || category || 'Place';
    },

    /**
     * Create a Leaflet DivIcon for a place.
     * @param {Object} place - Place data object
     * @param {Object} [options] - { size: number, pulse: boolean }
     * @returns {L.DivIcon}
     */
    createLeafletIcon(place, options) {
      const opts = options || {};
      const size = opts.size || 30;
      const color = this.getColor(place.category);
      const emoji = this.getEmoji(place.category);
      const pulse = opts.pulse || place.is_featured || false;

      const pulseRing = pulse ? `
        <span style="
          position:absolute;top:-4px;left:-4px;right:-4px;bottom:-4px;
          border-radius:50%;border:2px solid ${color};opacity:0.6;
          animation:hyMarkerPulse 2s infinite;
        "></span>` : '';

      return L.divIcon({
        className: 'hy-custom-marker',
        html: `
          <div style="
            position:relative;display:flex;align-items:center;justify-content:center;
            width:${size}px;height:${size}px;border-radius:50%;
            background:${color};border:2px solid white;
            box-shadow:0 3px 10px rgba(0,0,0,0.35);
            font-size:${Math.round(size * 0.47)}px;cursor:pointer;
            transition:transform 0.2s;
          " onmouseover="this.style.transform='scale(1.2)'"
             onmouseout="this.style.transform='scale(1)'"
          >
            ${emoji}
            ${pulseRing}
          </div>`,
        iconSize: [size, size],
        iconAnchor: [size / 2, size / 2],
        popupAnchor: [0, -(size / 2 + 4)],
      });
    },

    /**
     * Create a DOM element for a MapLibre marker.
     * @param {Object} place
     * @param {Object} [options] - { size: number }
     * @returns {HTMLElement}
     */
    createMaplibreMarkerEl(place, options) {
      const opts = options || {};
      const size = opts.size || 32;
      const color = this.getColor(place.category);
      const emoji = this.getEmoji(place.category);

      const el = document.createElement('div');
      el.className = 'hy-3d-marker';
      el.style.cssText = `
        width:${size}px;height:${size}px;border-radius:50%;
        background:${color};border:2px solid white;
        box-shadow:0 4px 12px rgba(0,0,0,0.5);
        display:flex;align-items:center;justify-content:center;
        font-size:${Math.round(size * 0.44)}px;cursor:pointer;
        transition:transform 0.2s;
      `;
      el.textContent = emoji;
      el.title = place.name || '';

      el.addEventListener('mouseenter', () => { el.style.transform = 'scale(1.3)'; });
      el.addEventListener('mouseleave', () => { el.style.transform = 'scale(1)'; });

      return el;
    },

    /**
     * Build popup HTML content for a place (shared between engines).
     * @param {Object} place
     * @returns {string} HTML string
     */
    buildPopupHTML(place) {
      const name = this._escHtml(place.name);
      const category = this.getLabel(place.category);
      const emoji = this.getEmoji(place.category);
      const district = this._escHtml(place.district_name || '');
      const state = this._escHtml(place.state_name || '');
      const rating = parseFloat(place.avg_rating) || 4.5;
      const ratingCount = parseInt(place.review_count) || 0;
      const slug = encodeURIComponent(place.slug || '');
      const coverUrl = place.cover_image_url || '';

      const coverSection = coverUrl ? `
        <div style="
          height:120px;background:url('${this._escHtml(coverUrl)}') center/cover no-repeat;
          border-radius:8px 8px 0 0;margin:-8px -12px 8px -12px;
        "></div>` : '';

      const locationStr = district ? `${district}${state ? ', ' + state : ''}` : state || '';

      return `
        <div class="hy-marker-popup" style="font-family:var(--font-body,'Inter',sans-serif);min-width:200px;">
          ${coverSection}
          <div style="padding:0 4px;">
            <span style="
              display:inline-block;padding:2px 8px;border-radius:6px;
              font-size:0.7rem;font-weight:700;text-transform:uppercase;
              background:${this.getColor(place.category)}22;color:${this.getColor(place.category)};
              margin-bottom:4px;
            ">${emoji} ${this._escHtml(category)}</span>
            <h4 style="margin:4px 0 2px;font-size:0.95rem;font-weight:700;color:var(--text-primary,#1e293b);">${name}</h4>
            ${locationStr ? `<div style="font-size:0.78rem;color:var(--text-muted,#64748b);margin-bottom:4px;">📍 ${locationStr}</div>` : ''}
            <div style="display:flex;align-items:center;gap:4px;margin-bottom:8px;">
              <span style="color:#f59e0b;font-weight:700;font-size:0.82rem;">★ ${rating.toFixed(1)}</span>
              ${ratingCount > 0 ? `<span style="color:var(--text-muted,#94a3b8);font-size:0.72rem;">(${ratingCount})</span>` : ''}
            </div>
            ${slug ? `
              <div style="display:flex;gap:6px;">
                <a href="/place/${slug}" style="
                  flex:1;text-align:center;padding:6px 10px;border-radius:8px;
                  background:var(--primary,#FF7A18);color:#fff;
                  font-size:0.78rem;font-weight:700;text-decoration:none;
                  transition:opacity 0.2s;
                " onmouseover="this.style.opacity='0.9'" onmouseout="this.style.opacity='1'">View Details</a>
                <a href="https://www.google.com/maps/dir/?api=1&destination=${place.latitude},${place.longitude}" target="_blank" style="
                  padding:6px 10px;border-radius:8px;
                  background:var(--bg-tertiary,#f1f5f9);color:var(--text-primary,#1e293b);
                  font-size:0.78rem;font-weight:600;text-decoration:none;
                  transition:opacity 0.2s;
                " onmouseover="this.style.opacity='0.8'" onmouseout="this.style.opacity='1'">🧭 Route</a>
              </div>
            ` : ''}
          </div>
        </div>`;
    },

    /**
     * Create a numbered stop marker (for itinerary maps).
     * @param {number} stopNumber
     * @param {string} [color='#f59e0b']
     * @returns {L.DivIcon}
     */
    createStopIcon(stopNumber, color) {
      const c = color || '#f59e0b';
      return L.divIcon({
        className: 'hy-stop-marker',
        html: `
          <div style="
            width:28px;height:28px;border-radius:50%;
            background:${c};color:#fff;
            font-weight:800;font-size:13px;
            display:flex;align-items:center;justify-content:center;
            border:2px solid white;
            box-shadow:0 2px 8px rgba(0,0,0,0.3);
          ">${stopNumber}</div>`,
        iconSize: [28, 28],
        iconAnchor: [14, 14],
      });
    },

    /**
     * Create a user location pulse marker.
     * @returns {L.DivIcon}
     */
    createUserLocationIcon() {
      return L.divIcon({
        className: 'hy-user-marker',
        html: `
          <div style="
            width:16px;height:16px;border-radius:50%;
            background:#3b82f6;border:3px solid white;
            box-shadow:0 0 0 4px rgba(59,130,246,0.3), 0 2px 8px rgba(0,0,0,0.2);
            animation:hyUserPulse 2s infinite;
          "></div>`,
        iconSize: [16, 16],
        iconAnchor: [8, 8],
      });
    },

    /** @private */
    _escHtml(str) {
      if (!str) return '';
      return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;')
        .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    },
  };

  /* ── Google Advanced Marker Factory ───────────────── */

  const GoogleMarkerFactory = {

    /**
     * Create the DOM element for a Google Advanced Marker (Tourist Place).
     * @param {Object} place
     * @param {Object} [options]
     * @returns {HTMLElement}
     */
    createPlaceMarkerDOM(place, options) {
      const opts = options || {};
      const category = place.category || 'default';
      const color = MapMarkers.getColor(category);
      const emoji = MapMarkers.getEmoji(category);
      const label = MapMarkers.getLabel(category);
      const isGem = !!place.is_hidden_gem;
      const isFeatured = !!place.is_featured;
      const isSpecial = isGem || isFeatured;

      const markerEl = document.createElement('div');
      markerEl.className = 'hy-gmp-marker' +
        (isFeatured ? ' pulse-gold' : '') +
        (isGem ? ' pulse-pink' : '') +
        (opts.selected ? ' selected' : '');

      markerEl.setAttribute('role', 'button');
      markerEl.setAttribute('tabindex', '0');
      markerEl.setAttribute('aria-label', `${place.name || 'Place'} - ${label}`);
      markerEl.title = place.name || '';
      markerEl.dataset.placeId = place.id || '';
      markerEl.dataset.category = category;

      const size = isSpecial ? 38 : 32;

      // Inner pin circle
      const pinEl = document.createElement('div');
      pinEl.className = 'hy-gmp-pin';
      pinEl.style.backgroundColor = color;
      pinEl.style.width = `${size}px`;
      pinEl.style.height = `${size}px`;

      const emojiEl = document.createElement('span');
      emojiEl.className = 'hy-gmp-emoji';
      emojiEl.textContent = emoji;
      pinEl.appendChild(emojiEl);
      markerEl.appendChild(pinEl);

      // Gem badge
      if (isGem) {
        const badgeEl = document.createElement('span');
        badgeEl.className = 'hy-gmp-badge gem';
        badgeEl.textContent = '💎';
        badgeEl.title = 'Hidden Gem';
        markerEl.appendChild(badgeEl);
      } else if (isFeatured) {
        const badgeEl = document.createElement('span');
        badgeEl.className = 'hy-gmp-badge featured';
        badgeEl.textContent = '✨';
        badgeEl.title = 'Featured';
        markerEl.appendChild(badgeEl);
      }

      return markerEl;
    },

    /**
     * Create the DOM element for GeoJSON point layers (Hotels, Homestays, OSM Waterfalls).
     * @param {Object} props - Feature properties
     * @param {string} layerType - 'hotels' | 'homestays' | 'waterfalls' | 'waterfalls_geo'
     * @param {Object} [options]
     * @returns {HTMLElement}
     */
    createPointMarkerDOM(props, layerType, options) {
      const opts = options || {};
      const markerEl = document.createElement('div');

      let color = '#2563eb';
      let emoji = '🏨';
      let label = 'Hotel';
      let name = props.name || 'Hotel';
      let cls = 'hotel';
      let size = 28;

      if (layerType === 'homestays') {
        color = '#059669';
        emoji = '🏡';
        label = 'Homestay';
        name = props.title || 'Homestay';
        cls = 'homestay';
      } else if (layerType === 'waterfalls' || layerType === 'waterfalls_geo') {
        color = '#0891b2';
        emoji = '💦';
        label = 'OpenStreetMap Waterfall';
        name = props.name || 'Waterfall';
        cls = 'waterfall-osm';
        size = 26;
      }

      markerEl.className = `hy-gmp-marker point-marker ${cls}` + (opts.selected ? ' selected' : '');
      markerEl.setAttribute('role', 'button');
      markerEl.setAttribute('tabindex', '0');
      markerEl.setAttribute('aria-label', `${name} - ${label}`);
      markerEl.title = name;

      const pinEl = document.createElement('div');
      pinEl.className = 'hy-gmp-pin';
      pinEl.style.backgroundColor = color;
      pinEl.style.width = `${size}px`;
      pinEl.style.height = `${size}px`;

      const emojiEl = document.createElement('span');
      emojiEl.className = 'hy-gmp-emoji';
      emojiEl.textContent = emoji;
      pinEl.appendChild(emojiEl);
      markerEl.appendChild(pinEl);

      return markerEl;
    },

    /**
     * Instantiate an AdvancedMarkerElement on the given Google Map.
     * @param {google.maps.Map} googleMap
     * @param {Object} data - Place record or GeoJSON feature
     * @param {Object} [options] - { type: 'place'|'hotels'|'homestays'|'waterfalls_geo', onClick: Function }
     * @returns {google.maps.marker.AdvancedMarkerElement|null}
     */
    createMarker(googleMap, data, options) {
      if (typeof google === 'undefined' || !google.maps || !google.maps.marker || !google.maps.marker.AdvancedMarkerElement) {
        console.warn('[HYGoogleMarkerFactory] AdvancedMarkerElement not available');
        return null;
      }

      const opts = options || {};
      const type = opts.type || 'place';
      let lat, lng, domEl, title, zIndex;

      if (type === 'place') {
        lat = parseFloat(data.latitude);
        lng = parseFloat(data.longitude);
        if (isNaN(lat) || isNaN(lng)) return null;

        domEl = this.createPlaceMarkerDOM(data, opts);
        title = data.name || 'Tourist Place';
        const isSpecial = !!data.is_hidden_gem || !!data.is_featured;
        zIndex = isSpecial ? 150 : 100;
      } else {
        const coords = data.geometry ? data.geometry.coordinates : [0, 0];
        lng = coords[0];
        lat = coords[1];
        if (isNaN(lat) || isNaN(lng) || lat === 0) return null;

        const props = data.properties || data;
        domEl = this.createPointMarkerDOM(props, type, opts);
        title = props.name || props.title || 'Location';
        zIndex = type === 'hotels' ? 90 : (type === 'homestays' ? 90 : 80);
      }

      const isRequiredCollision = (type === 'place' && (!!data.is_hidden_gem || !!data.is_featured));

      const marker = new google.maps.marker.AdvancedMarkerElement({
        map: googleMap,
        position: { lat, lng },
        content: domEl,
        title: title,
        zIndex: zIndex,
        collisionBehavior: isRequiredCollision
          ? ((google.maps.CollisionBehavior && google.maps.CollisionBehavior.REQUIRED) || 'REQUIRED')
          : ((google.maps.CollisionBehavior && google.maps.CollisionBehavior.OPTIONAL_AND_HIDES_LOWER_PRIORITY) || 'OPTIONAL_AND_HIDES_LOWER_PRIORITY'),
      });

      // Attach metadata
      marker._hyData = data;
      marker._hyType = type;
      marker._hyId = (type === 'place' ? data.id : (data.properties ? (data.properties.id || data.properties.osm_id || data.properties.name) : 'point'));
      marker._hyElement = domEl;

      // Event listener for click
      if (typeof opts.onClick === 'function') {
        domEl.addEventListener('click', (e) => {
          e.stopPropagation();
          opts.onClick(data, marker);
        });

        domEl.addEventListener('keydown', (e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            e.stopPropagation();
            opts.onClick(data, marker);
          }
        });
      }

      return marker;
    },

    /**
     * Build rich InfoWindow HTML for a tourist place.
     * @param {Object} place
     * @returns {string} Safe HTML string
     */
    buildPlacePopupHTML(place) {
      const esc = MapMarkers._escHtml;
      const name = esc(place.name);
      const category = MapMarkers.getLabel(place.category);
      const emoji = MapMarkers.getEmoji(place.category);
      const color = MapMarkers.getColor(place.category);
      const district = esc(place.district_name || '');
      const state = esc(place.state_name || '');
      const rating = parseFloat(place.avg_rating) || 4.5;
      const ratingCount = parseInt(place.review_count) || 0;
      const slug = encodeURIComponent(place.slug || '');
      const lat = parseFloat(place.latitude);
      const lng = parseFloat(place.longitude);
      const directionsUrl = (place.maps_link && place.maps_link.startsWith('http'))
        ? esc(place.maps_link)
        : `https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}`;

      let coverUrl = '';
      if (place.cover_image && String(place.cover_image).trim() !== '') {
        coverUrl = place.cover_image.startsWith('http')
          ? esc(place.cover_image)
          : '/static/uploads/places/' + esc(place.cover_image);
      } else {
        coverUrl = '/static/placeholder-place.svg';
      }

      const locationStr = district ? `${district}${state ? ', ' + state : ''}` : state || 'Bihar';

      return `
        <div class="popup-card hy-gmp-popup-card" style="width:260px;font-family:var(--font-body,'Inter',sans-serif);line-height:1.4;">
          <div style="position:relative;height:125px;overflow:hidden;border-radius:8px 8px 0 0;background:#0f172a;margin:-12px -12px 8px -12px;">
            <img src="${coverUrl}" alt="${name}" style="width:100%;height:100%;object-fit:cover;display:block;" onerror="this.onerror=null;this.src='/static/placeholder-place.svg';">
            <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0.05) 0%,rgba(0,0,0,0.7) 100%);pointer-events:none;"></div>
            <span style="position:absolute;top:8px;left:8px;padding:2px 8px;border-radius:6px;background:${color};color:#fff;font-size:0.68rem;font-weight:700;text-transform:uppercase;z-index:2;">
              ${emoji} ${esc(category)}
            </span>
            ${place.is_hidden_gem ? '<span style="position:absolute;top:8px;right:8px;padding:2px 8px;border-radius:6px;background:#ec4899;color:#fff;font-size:0.68rem;font-weight:700;z-index:2;">💎 Gem</span>' : ''}
          </div>
          <div style="padding:0 2px;">
            <h4 style="margin:2px 0 4px;font-size:0.95rem;font-weight:700;color:var(--text-primary,#1e293b);">${name}</h4>
            <div style="font-size:0.78rem;color:var(--text-muted,#64748b);margin-bottom:4px;">📍 ${locationStr}</div>
            <div style="display:flex;align-items:center;gap:6px;margin-bottom:8px;">
              <span style="color:#f59e0b;font-weight:700;font-size:0.82rem;">★ ${rating.toFixed(1)}</span>
              ${ratingCount > 0 ? `<span style="color:var(--text-muted,#94a3b8);font-size:0.72rem;">(${ratingCount})</span>` : ''}
            </div>
            <div style="display:flex;gap:6px;margin-top:6px;">
              ${slug ? `<a href="/place/${slug}" style="flex:1;text-align:center;padding:5px 8px;border-radius:6px;background:var(--primary,#FF7A18);color:#fff;font-size:0.78rem;font-weight:700;text-decoration:none;">Details →</a>` : ''}
              <a href="${directionsUrl}" target="_blank" rel="noopener noreferrer" style="padding:5px 8px;border-radius:6px;background:var(--bg-tertiary,#f1f5f9);color:var(--text-primary,#1e293b);font-size:0.78rem;font-weight:600;text-decoration:none;">🧭 Route</a>
            </div>
          </div>
        </div>
      `;
    },

    /**
     * Build rich InfoWindow HTML for a Hotel (public business info only).
     * @param {Object} props
     * @param {Array<number>} coords - [lng, lat]
     * @returns {string} Safe HTML string
     */
    buildHotelPopupHTML(props, coords) {
      const esc = MapMarkers._escHtml;
      const name = esc(props.name || 'Hotel');
      const district = esc(props.district_name || 'Bihar');
      const address = props.address ? esc(props.address) : '';
      const phone = props.phone ? esc(props.phone) : '';
      const lat = coords ? coords[1] : 25.0;
      const lng = coords ? coords[0] : 85.0;

      return `
        <div class="hy-gmp-popup-card" style="min-width:200px;max-width:240px;font-family:var(--font-body,'Inter',sans-serif);line-height:1.4;padding:2px;">
          <h4 style="margin:0 0 4px 0;font-size:0.95rem;color:#1e3a8a;font-weight:700;">🏨 ${name}</h4>
          <span style="display:inline-block;padding:2px 6px;background:#dbeafe;color:#1e40af;border-radius:4px;font-size:0.72rem;font-weight:600;margin-bottom:6px;">${district}</span>
          ${address ? `<p style="margin:2px 0 4px 0;font-size:0.78rem;color:#475569;">📍 ${address}</p>` : ''}
          ${phone ? `<p style="margin:2px 0 6px 0;font-size:0.78rem;color:#475569;">📞 <a href="tel:${phone}" style="color:#2563eb;text-decoration:none;font-weight:600;">${phone}</a></p>` : ''}
          <div style="margin-top:8px;">
            <a href="https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}" target="_blank" rel="noopener noreferrer" style="display:inline-block;padding:4px 10px;background:#2563eb;color:#fff;border-radius:4px;font-size:0.76rem;text-decoration:none;font-weight:600;">Get Directions ↗</a>
          </div>
        </div>
      `;
    },

    /**
     * Build rich InfoWindow HTML for a Homestay (public stay info only).
     * @param {Object} props
     * @param {Array<number>} coords
     * @returns {string} Safe HTML string
     */
    buildHomestayPopupHTML(props, coords) {
      const esc = MapMarkers._escHtml;
      const title = esc(props.title || 'Homestay');
      const district = esc(props.district_name || 'Bihar');
      const priceText = props.price_per_night && props.price_per_night > 0 ? `₹${props.price_per_night}/night` : 'Free Cultural Stay';
      const propType = esc((props.property_type || 'Homestay').replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()));
      const ratingText = props.avg_rating ? `⭐ ${props.avg_rating} (${props.review_count || 0})` : '⭐ 5.0 (New)';
      const detailUrl = props.detail_url ? esc(props.detail_url) : (props.slug ? `/stays/${esc(props.slug)}` : '#');

      const imgHtml = props.cover_image
        ? `<img src="/static/uploads/stays/${esc(props.cover_image)}" alt="${title}" style="width:100%;height:85px;object-fit:cover;border-radius:6px;margin-bottom:6px;display:block;" onerror="this.style.display='none'">`
        : '';

      return `
        <div class="hy-gmp-popup-card" style="min-width:200px;max-width:240px;font-family:var(--font-body,'Inter',sans-serif);line-height:1.4;padding:2px;">
          ${imgHtml}
          <h4 style="margin:0 0 4px 0;font-size:0.92rem;color:#064e3b;line-height:1.3;font-weight:700;">🏡 ${title}</h4>
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
            <span style="font-size:0.72rem;color:#065f46;background:#d1fae5;padding:2px 6px;border-radius:4px;font-weight:600;">${propType}</span>
            <span style="font-size:0.72rem;color:#475569;font-weight:500;">${ratingText}</span>
          </div>
          <p style="margin:0 0 6px 0;font-size:0.82rem;color:#059669;font-weight:700;">${priceText} • <span style="font-size:0.75rem;color:#64748b;font-weight:normal;">${district}</span></p>
          <a href="${detailUrl}" style="display:inline-block;width:100%;text-align:center;box-sizing:border-box;padding:5px 10px;background:#059669;color:#fff;border-radius:4px;font-size:0.78rem;text-decoration:none;font-weight:600;">Explore Homestay →</a>
        </div>
      `;
    },

    /**
     * Build rich InfoWindow HTML for OSM Waterfalls (preserving OpenStreetMap attribution).
     * @param {Object} props
     * @param {Array<number>} coords - [lng, lat]
     * @returns {string} Safe HTML string
     */
    buildWaterfallPopupHTML(props, coords) {
      const esc = MapMarkers._escHtml;
      const name = esc(props.name || 'Waterfall');
      const nameHi = props.name_hi ? ` (${esc(props.name_hi)})` : '';
      const lat = coords ? coords[1].toFixed(4) : '';
      const lng = coords ? coords[0].toFixed(4) : '';
      const osmId = props.osm_id ? esc(String(props.osm_id)) : 'node';
      const sourceUrl = props.source_url ? esc(props.source_url) : `https://www.openstreetmap.org/node/${osmId}`;

      return `
        <div class="hy-gmp-popup-card" style="min-width:190px;max-width:230px;font-family:var(--font-body,'Inter',sans-serif);line-height:1.4;padding:2px;">
          <h4 style="margin:0 0 4px 0;font-size:0.95rem;color:#0e7490;font-weight:700;">💦 ${name}${nameHi}</h4>
          <p style="margin:0 0 6px 0;font-size:0.78rem;color:#475569;">
            <strong>Coordinates:</strong> ${lat}°N, ${lng}°E<br>
            <strong>Source:</strong> OpenStreetMap (${osmId})
          </p>
          <a href="${sourceUrl}" target="_blank" rel="noopener noreferrer" style="font-size:0.75rem;color:#0284c7;text-decoration:underline;font-weight:500;">View on OpenStreetMap ↗</a>
        </div>
      `;
    },

    /**
     * Set selection visual on a marker element.
     * @param {google.maps.marker.AdvancedMarkerElement} marker
     * @param {boolean} isSelected
     */
    setSelected(marker, isSelected) {
      if (!marker || !marker._hyElement) return;
      marker._hyElement.classList.toggle('selected', isSelected);
      marker.zIndex = isSelected ? 999 : (marker._hyType === 'place' ? 100 : 80);
    },
  };

  /* ── Inject Global Marker Styles (Google & Custom) ── */
  if (typeof document !== 'undefined') {
    const styleId = 'hy-gmp-marker-styles';
    if (!document.getElementById(styleId)) {
      const style = document.createElement('style');
      style.id = styleId;
      style.textContent = `
        .hy-gmp-marker {
          position: relative;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          user-select: none;
          touch-action: manipulation;
          transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
        }
        .hy-gmp-marker::after {
          content: '';
          position: absolute;
          inset: -8px;
          min-width: 44px;
          min-height: 44px;
          border-radius: 50%;
          pointer-events: auto;
        }
        .hy-gmp-pin {
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 50%;
          border: 2px solid #ffffff;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.45);
          transition: box-shadow 0.2s, transform 0.2s;
        }
        .hy-gmp-emoji {
          font-size: 0.95rem;
          line-height: 1;
          pointer-events: none;
        }
        .hy-gmp-badge {
          position: absolute;
          top: -4px;
          right: -4px;
          width: 16px;
          height: 16px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 10px;
          background: rgba(236, 72, 153, 0.95);
          color: white;
          box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
          border: 1px solid #ffffff;
          pointer-events: none;
        }
        .hy-gmp-badge.featured {
          background: rgba(245, 158, 11, 0.95);
        }
        .hy-gmp-marker:hover .hy-gmp-pin {
          transform: scale(1.18);
          box-shadow: 0 8px 20px rgba(0, 0, 0, 0.6);
        }
        .hy-gmp-marker.selected .hy-gmp-pin {
          transform: scale(1.25);
          outline: 3px solid #FF7A18;
          box-shadow: 0 8px 24px rgba(255, 122, 24, 0.5);
        }
        .hy-gmp-marker.pulse-gold .hy-gmp-pin {
          animation: hyGmpPulseGold 2s infinite;
        }
        .hy-gmp-marker.pulse-pink .hy-gmp-pin {
          animation: hyGmpPulsePink 2s infinite;
        }
        @keyframes hyGmpPulseGold {
          0% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.75); }
          70% { box-shadow: 0 0 0 10px rgba(245, 158, 11, 0); }
          100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
        }
        @keyframes hyGmpPulsePink {
          0% { box-shadow: 0 0 0 0 rgba(236, 72, 153, 0.75); }
          70% { box-shadow: 0 0 0 10px rgba(236, 72, 153, 0); }
          100% { box-shadow: 0 0 0 0 rgba(236, 72, 153, 0); }
        }
      `;
      document.head.appendChild(style);
    }
  }

  root.HYMapMarkers = MapMarkers;
  root.HYGoogleMarkerFactory = GoogleMarkerFactory;

})(window);
