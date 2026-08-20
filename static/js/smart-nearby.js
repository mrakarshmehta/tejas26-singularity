/* ═══════════════════════════════════════════════════════════════════════════════
   HiddenYatra — Google Maps–style Smart Nearby Discovery System JS Engine
   Handles live search, Overpass API integration, radius selector, distance sorting,
   category filtering, GPS location detection, and 10 Nearby Essentials rendering.
   ═══════════════════════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  window.SNS = window.SNS || {};

  // Default Patna coordinates if unlocated
  let currentLat = 25.5941;
  let currentLng = 85.1376;
  let currentRadius = 5.0; // Default 5 km radius
  let currentCategory = '';
  let currentQuery = '';
  let isGpsActive = false;
  let activeMap = null;
  let markersLayer = null;
  let fetchTimeout = null;

  // Category Icon & Label Map
  const CATEGORY_INFO = {
    'hotel': { icon: '🏨', label: 'Hotels' },
    'hospital': { icon: '🏥', label: 'Hospitals' },
    'petrol_pump': { icon: '⛽', label: 'Petrol Pumps' },
    'restaurant': { icon: '🍽️', label: 'Restaurants' },
    'pharmacy': { icon: '💊', label: 'Medical Stores' },
    'atm': { icon: '🏧', label: 'ATMs' },
    'police_station': { icon: '🚓', label: 'Police Stations' },
    'bus_stand': { icon: '🚏', label: 'Bus Stops' },
    'railway_station': { icon: '🚉', label: 'Railway Stations' },
    'airport': { icon: '✈️', label: 'Airports' },
    'parking': { icon: '🅿️', label: 'Parking Lots' },
    'ev_charging': { icon: '⚡', label: 'EV Charging Stations' },
    'toilet': { icon: '🚻', label: 'Public Toilets' },
    'tourist_place': { icon: '📍', label: 'Tourist Places' }
  };

  // Escaping utility for XSS prevention
  function _esc(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // Initialize Smart Nearby Discovery System
  SNS.init = function (options) {
    options = options || {};
    const containerId = options.containerId || 'sn-discovery-container';
    const mapId = options.mapId || 'sn-map-canvas';

    if (options.lat) currentLat = parseFloat(options.lat);
    if (options.lng) currentLng = parseFloat(options.lng);

    // 1. Acquire user GPS location if allowed
    if (!options.lat && window.HY && HY.getLocation()) {
      const loc = HY.getLocation();
      currentLat = loc.lat;
      currentLng = loc.lng;
      isGpsActive = true;
      SNS.updateLocationBadge('Nearest to You');
    } else if (!options.lat && navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((pos) => {
        currentLat = pos.coords.latitude;
        currentLng = pos.coords.longitude;
        isGpsActive = true;
        SNS.updateLocationBadge('Nearest to You');
        if (window.HY) {
          sessionStorage.setItem('hy_location', JSON.stringify({ lat: currentLat, lng: currentLng }));
        }
        SNS.fetchNearby();
      }, () => {
        SNS.updateLocationBadge('Place Coordinates');
      });
    }

    // 2. Setup Map if map container exists (Google Maps or Leaflet)
    const mapEl = document.getElementById(mapId);
    if (mapEl) {
      if ((window.MAP_ENGINE === 'google' || typeof L === 'undefined') && typeof google !== 'undefined' && google.maps) {
        activeMap = new google.maps.Map(mapEl, {
          center: { lat: currentLat, lng: currentLng },
          zoom: 13,
          mapId: window.GOOGLE_MAPS_MAP_ID || undefined,
          streetViewControl: false,
          fullscreenControl: false,
        });
        markersLayer = [];

        activeMap.addListener('idle', () => {
          const center = activeMap.getCenter();
          const bounds = activeMap.getBounds();
          if (center && bounds) {
            currentLat = center.lat();
            currentLng = center.lng();
            clearTimeout(fetchTimeout);
            fetchTimeout = setTimeout(() => {
              const ne = bounds.getNorthEast();
              const sw = bounds.getSouthWest();
              const boundsStr = `${sw.lat()},${ne.lat()},${sw.lng()},${ne.lng()}`;
              SNS.fetchNearby({ bounds: boundsStr, skipMapPan: true });
            }, 300);
          }
        });
      } else if (typeof L !== 'undefined') {
        activeMap = L.map(mapId, { zoomControl: true }).setView([currentLat, currentLng], 13);
        L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
          attribution: '&copy; OpenStreetMap &copy; CARTO',
          maxZoom: 18
        }).addTo(activeMap);

        markersLayer = L.layerGroup().addTo(activeMap);

        // Drag / Zoom End triggers instant nearby search update
        activeMap.on('moveend', () => {
          const center = activeMap.getCenter();
          const bounds = activeMap.getBounds();
          currentLat = center.lat;
          currentLng = center.lng;

          clearTimeout(fetchTimeout);
          fetchTimeout = setTimeout(() => {
            const boundsStr = `${bounds.getSouth()},${bounds.getNorth()},${bounds.getWest()},${bounds.getEast()}`;
            SNS.fetchNearby({ bounds: boundsStr, skipMapPan: true });
          }, 300);
        });
      }
    }

    // 3. Bind Category Bar & Quick Filter Chips
    document.querySelectorAll('.sn-cat-chip[data-category]').forEach(chip => {
      chip.addEventListener('click', function () {
        document.querySelectorAll('.sn-cat-chip').forEach(c => c.classList.remove('active'));
        this.classList.add('active');
        currentCategory = this.dataset.category || '';
        SNS.fetchNearby();
      });
    });

    // 4. Bind Radius Selector Buttons (1km, 2km, 5km, 10km)
    document.querySelectorAll('.sn-radius-btn').forEach(btn => {
      btn.addEventListener('click', function () {
        document.querySelectorAll('.sn-radius-btn').forEach(b => {
          b.classList.remove('active');
          b.style.background = 'transparent';
          b.style.color = 'var(--sn-text)';
        });
        this.classList.add('active');
        this.style.background = 'var(--sn-primary, #6366f1)';
        this.style.color = '#fff';
        currentRadius = parseFloat(this.dataset.radius || '5.0');
        SNS.fetchNearby();
      });
    });

    // Initial Fetch
    SNS.fetchNearby();
  };

  // Update Location Badge ("Nearest to You" vs "Place Location")
  SNS.updateLocationBadge = function (label) {
    const badgeEl = document.getElementById('sn-location-badge');
    if (badgeEl) {
      badgeEl.innerHTML = isGpsActive ? `📍 ${label}` : `📌 ${label}`;
    }
  };

  // Fetch Nearby Results from API
  SNS.fetchNearby = function (params) {
    params = params || {};
    const stack = document.getElementById('sn-cards-stack');
    const countEl = document.getElementById('sn-results-count');

    // Show Skeleton Loaders
    if (stack) {
      stack.innerHTML = `
        <div class="sn-skeleton-card">
          <div class="sn-skeleton-line" style="width:60%;"></div>
          <div class="sn-skeleton-line" style="width:85%;"></div>
          <div class="sn-skeleton-line" style="width:40%;"></div>
        </div>
        <div class="sn-skeleton-card">
          <div class="sn-skeleton-line" style="width:50%;"></div>
          <div class="sn-skeleton-line" style="width:75%;"></div>
        </div>
      `;
    }

    let url = `/api/nearby?lat=${currentLat}&lng=${currentLng}&radius=${currentRadius}`;
    if (currentCategory) url += `&category=${encodeURIComponent(currentCategory)}`;
    if (currentQuery) url += `&q=${encodeURIComponent(currentQuery)}`;
    if (params.bounds) url += `&bounds=${encodeURIComponent(params.bounds)}`;

    fetch(url)
      .then(r => r.json())
      .then(data => {
        if (!data || data.status !== 'success') {
          SNS.renderError('Unable to retrieve nearby results.');
          return;
        }

        const results = data.results || [];
        if (countEl) countEl.textContent = results.length;

        // Render Cards & Map Markers
        SNS.renderResults(results);
        if (activeMap && !params.skipMapPan && results.length > 0) {
          if (typeof activeMap.panTo === 'function') {
            activeMap.panTo({ lat: currentLat, lng: currentLng });
          } else if (typeof activeMap.setView === 'function') {
            activeMap.setView([currentLat, currentLng], 13);
          }
        }
      })
      .catch(() => {
        // Fallback to /api/smart-nearby
        fetch(`/api/smart-nearby?lat=${currentLat}&lng=${currentLng}&category=${encodeURIComponent(currentCategory || '')}`)
          .then(r => r.json())
          .then(d => {
            if (d && d.results) {
              if (countEl) countEl.textContent = d.results.length;
              SNS.renderResults(d.results);
            }
          })
          .catch(() => SNS.renderError('Failed to connect to discovery server.'));
      });
  };

  // Render Result Cards & Markers
  SNS.renderResults = function (results) {
    const stack = document.getElementById('sn-cards-stack');
    if (markersLayer) {
      if (Array.isArray(markersLayer)) {
        markersLayer.forEach(m => { if (m && typeof m.setMap === 'function') m.setMap(null); });
        markersLayer = [];
      } else if (typeof markersLayer.clearLayers === 'function') {
        markersLayer.clearLayers();
      }
    }

    if (!results || results.length === 0) {
      if (stack) {
        const catInfo = CATEGORY_INFO[currentCategory] || { label: 'essential services' };
        stack.innerHTML = `
          <div class="sn-empty-state">
            <span class="sn-empty-icon">🔍</span>
            <h4 style="font-weight:700;color:var(--sn-text);">No nearby ${catInfo.label.toLowerCase()} found</h4>
            <p style="font-size:0.85rem;margin-top:6px;">Try selecting a larger search radius (e.g., 10 km) or selecting another category.</p>
          </div>
        `;
      }
      return;
    }

    let cardsHtml = '';
    results.forEach((item, idx) => {
      const catMeta = CATEGORY_INFO[item.category] || { icon: '📍', label: item.category || 'Service' };
      const icon = item.icon || catMeta.icon;
      const cardId = `sn-card-${idx}`;

      // 10 Essentials Collapsible HTML
      let essentialsHtml = '';
      if (item.essentials && item.essentials.length > 0) {
        const essentialItems = item.essentials.map(ess => `
          <div class="sn-essential-item">
            <div class="sn-essential-name">
              <span>${_esc(ess.icon)}</span>
              <span>${_esc(ess.name)}</span>
            </div>
            <div class="sn-essential-meta">
              <span>📍 ${_esc(ess.distance_formatted)}</span>
              ${ess.walking_time_text ? `<span> • 🚶 ${_esc(ess.walking_time_text)}</span>` : ''}
              ${ess.phone ? `<span> • 📞 ${_esc(ess.phone)}</span>` : ''}
            </div>
          </div>
        `).join('');

        essentialsHtml = `
          <div class="sn-essentials-toggle" onclick="SNS.toggleEssentials('${cardId}')">
            <span>✨ 10 Nearby Essentials</span>
            <span class="sn-arrow" id="${cardId}-arrow">▼</span>
          </div>
          <div class="sn-essentials-content hidden" id="${cardId}-essentials">
            ${essentialItems}
          </div>
        `;
      }

      // Action buttons: Navigate, Call (if phone exists), Website (if available), View on Map
      const directionsUrl = item.directions_url || `https://www.google.com/maps/dir/?api=1&destination=${item.latitude},${item.longitude}`;
      let actionButtons = `
        <a href="${_esc(directionsUrl)}" target="_blank" class="sn-btn sn-btn-primary">
          🧭 Navigate
        </a>
      `;

      if (item.phone) {
        actionButtons += `
          <a href="tel:${_esc(item.phone)}" class="sn-btn sn-btn-outline" style="max-width:90px;" title="Call ${_esc(item.name)}">
            📞 Call
          </a>
        `;
      }

      if (item.website) {
        actionButtons += `
          <a href="${_esc(item.website)}" target="_blank" class="sn-btn sn-btn-outline" style="max-width:90px;" title="Visit Website">
            🌐 Website
          </a>
        `;
      }

      if (activeMap) {
        actionButtons += `<button onclick="SNS.focusMarker(${idx})" class="sn-btn sn-btn-outline">📍 View on Map</button>`;
      }

      // Main Card HTML
      cardsHtml += `
        <div class="sn-card" id="${cardId}" data-lat="${item.latitude}" data-lng="${item.longitude}">
          <div class="sn-card-header">
            <div class="sn-card-title-group">
              <div class="sn-card-name">${icon} ${_esc(item.name)}</div>
              <div class="sn-card-badges">
                <span class="sn-badge sn-badge-cat">${_esc(item.category_label || catMeta.label)}</span>
                <span class="sn-badge sn-badge-dist">📍 ${_esc(item.distance_formatted)}</span>
                ${item.rating ? `<span class="sn-badge sn-badge-rating">⭐ ${item.rating}</span>` : ''}
              </div>
            </div>
            <button class="sn-save-btn ${item.is_saved ? 'saved' : ''}" onclick="SNS.toggleSave('${item.raw_id || item.id}', '${item.item_type || 'service'}', this)" title="Save to wishlist">
              ❤️
            </button>
          </div>

          <div class="sn-card-meta">
            <div class="sn-meta-row">
              <span>📍 ${_esc(item.address)}</span>
            </div>
            <div class="sn-meta-row">
              <span class="${item.is_open !== false ? 'sn-status-open' : 'sn-status-closed'}">
                ${item.is_open !== false ? '🟢' : '🔴'} ${_esc(item.open_status_text || 'Open Now')}
              </span>
              ${item.phone ? `<span> • 📞 ${_esc(item.phone)}</span>` : ''}
            </div>
          </div>

          <!-- Travel Time Bar -->
          <div class="sn-travel-times">
            <div class="sn-travel-item">🚶 ${_esc(item.walking_time_text || item.travel_summary)}</div>
            <div style="color:var(--sn-border);">|</div>
            <div class="sn-travel-item">🚗 ${_esc(item.driving_time_text || item.travel_summary)}</div>
          </div>

          <!-- Action Buttons: Navigate, Call, Website, View on Map -->
          <div class="sn-card-actions">
            ${actionButtons}
          </div>

          <!-- 10 Nearby Essentials -->
          ${essentialsHtml}
        </div>
      `;

      // Add Map Marker
      if (markersLayer && item.latitude && item.longitude) {
        if (Array.isArray(markersLayer) && typeof google !== 'undefined' && google.maps) {
          const markerPos = { lat: item.latitude, lng: item.longitude };
          const infoWindow = new google.maps.InfoWindow({
            content: `
              <div style="font-family:sans-serif;padding:6px;min-width:180px;">
                <strong style="font-size:14px;color:#111;">${icon} ${_esc(item.name)}</strong><br>
                <span style="font-size:12px;color:#64748b;display:block;margin-top:2px;">📍 ${_esc(item.distance_formatted)} • 🚶 ${_esc(item.walking_time_text || '')}</span>
                <div style="margin-top:8px;display:flex;gap:6px;">
                  <a href="${_esc(directionsUrl)}" target="_blank" style="display:inline-block;padding:4px 10px;background:#6366f1;color:#fff;border-radius:6px;font-size:11px;text-decoration:none;font-weight:600;">Navigate →</a>
                </div>
              </div>
            `
          });

          let gMarker = null;
          if (google.maps.marker && google.maps.marker.AdvancedMarkerElement) {
            // Modern Google AdvancedMarkerElement
            const pinDiv = document.createElement('div');
            pinDiv.className = 'sn-gmarker-pin';
            pinDiv.style.cssText = 'background:linear-gradient(135deg,#6366f1,#4f46e5);width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-size:14px;border:2px solid white;box-shadow:0 4px 10px rgba(0,0,0,0.4);cursor:pointer;';
            pinDiv.textContent = icon;

            gMarker = new google.maps.marker.AdvancedMarkerElement({
              position: markerPos,
              map: activeMap,
              title: item.name,
              content: pinDiv,
            });

            gMarker.addListener('click', () => {
              infoWindow.open({ anchor: gMarker, map: activeMap });
            });
          } else if (typeof google.maps.Marker === 'function') {
            // Legacy Marker fallback
            gMarker = new google.maps.Marker({
              position: markerPos,
              map: activeMap,
              title: item.name,
            });

            gMarker.addListener('click', () => {
              infoWindow.open({ anchor: gMarker, map: activeMap });
            });
          }

          if (gMarker) {
            markersLayer.push(gMarker);
          }
        } else if (typeof L !== 'undefined' && typeof markersLayer.addLayer === 'function') {
          const markerIcon = L.divIcon({
            html: `<div style="background:linear-gradient(135deg,#6366f1,#4f46e5);width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-size:14px;border:2px solid white;box-shadow:0 4px 10px rgba(0,0,0,0.4);">${icon}</div>`,
            className: '',
            iconSize: [28, 28],
            iconAnchor: [14, 14]
          });

          const marker = L.marker([item.latitude, item.longitude], { icon: markerIcon });
          marker.bindPopup(`
            <div style="font-family:sans-serif;padding:6px;min-width:180px;">
              <strong style="font-size:14px;color:var(--text-primary,#111);">${icon} ${_esc(item.name)}</strong><br>
              <span style="font-size:12px;color:#64748b;display:block;margin-top:2px;">📍 ${_esc(item.distance_formatted)} • 🚶 ${_esc(item.walking_time_text || '')}</span>
              <div style="margin-top:8px;display:flex;gap:6px;">
                <a href="${_esc(directionsUrl)}" target="_blank" style="display:inline-block;padding:4px 10px;background:#6366f1;color:#fff;border-radius:6px;font-size:11px;text-decoration:none;font-weight:600;">Navigate →</a>
              </div>
            </div>
          `);
          markersLayer.addLayer(marker);
        }
      }
    });

    if (stack) stack.innerHTML = cardsHtml;
  };

  // Focus marker on map click
  SNS.focusMarker = function (idx) {
    const card = document.getElementById(`sn-card-${idx}`);
    if (!card || !activeMap) return;
    const lat = parseFloat(card.dataset.lat);
    const lng = parseFloat(card.dataset.lng);
    if (!isNaN(lat) && !isNaN(lng)) {
      if (typeof activeMap.panTo === 'function') {
        activeMap.panTo({ lat, lng });
        if (typeof activeMap.setZoom === 'function') activeMap.setZoom(15);
      } else if (typeof activeMap.setView === 'function') {
        activeMap.setView([lat, lng], 15, { animate: true });
      }
    }
  };

  // Toggle 10 Nearby Essentials panel
  SNS.toggleEssentials = function (cardId) {
    const content = document.getElementById(`${cardId}-essentials`);
    const arrow = document.getElementById(`${cardId}-arrow`);
    if (content) {
      content.classList.toggle('hidden');
      if (arrow) arrow.textContent = content.classList.contains('hidden') ? '▼' : '▲';
    }
  };

  // Toggle Save / Wishlist
  SNS.toggleSave = function (rawId, itemType, btnEl) {
    if (itemType !== 'place') {
      alert('Facility bookmarked!');
      btnEl.classList.toggle('saved');
      return;
    }
    fetch(`/wishlist/${rawId}/add`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRF-Token': window.HY_CSRF_TOKEN || ''
      }
    })
      .then(r => r.json())
      .then(() => {
        btnEl.classList.toggle('saved');
      })
      .catch(() => {
        btnEl.classList.toggle('saved');
      });
  };

  // Render error message
  SNS.renderError = function (msg) {
    const stack = document.getElementById('sn-cards-stack');
    if (stack) {
      stack.innerHTML = `
        <div class="sn-empty-state">
          <span class="sn-empty-icon">⚠️</span>
          <h4 style="font-weight:700;color:var(--sn-text);">${_esc(msg)}</h4>
          <button onclick="SNS.fetchNearby()" class="sn-btn sn-btn-primary" style="margin-top:14px;max-width:180px;">Retry Search</button>
        </div>
      `;
    }
  };

})();
