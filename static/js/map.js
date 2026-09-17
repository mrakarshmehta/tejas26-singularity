/* ═══════════════════════════════════════════════════════
   HiddenYatra — Map Widget (Leaflet)
   Place detail view, food markers, hotel markers, admin map
   ═══════════════════════════════════════════════════════ */

// Fix Leaflet default icon URLs
if (typeof L !== 'undefined' && L.Icon && L.Icon.Default) {
  delete L.Icon.Default.prototype._getIconUrl;
  L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
    iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  });
}

// Mobile popup options helper
function _getResponsivePopupOptions(customMaxWidth) {
  const isMobile = typeof window !== 'undefined' && window.innerWidth < 480;
  return {
    maxWidth: isMobile ? 240 : (customMaxWidth || 300),
    autoPanPadding: isMobile ? [12, 12] : [30, 30],
    closeButton: true
  };
}

// HTML escape utility — prevents XSS in Leaflet popups
function _escHtml(str) {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// Global map references for interactive marker focusing
let placeMap = null;
let hotelMarkers = [];
let foodMarkers = [];
let googlePlaceMapInstance = null;

function focusMapMarker(type, index) {
  const markers = type === 'hotel' ? hotelMarkers : foodMarkers;
  if (!markers[index]) return;

  // Scroll to map
  const mapEl = document.getElementById('place-map');
  if (mapEl) {
    mapEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  const marker = markers[index];

  // If Google Maps instance
  if (googlePlaceMapInstance) {
    const pos = marker.getPosition ? marker.getPosition() : marker.position;
    if (pos) {
      const lat = typeof pos.lat === 'function' ? pos.lat() : pos.lat;
      const lng = typeof pos.lng === 'function' ? pos.lng() : pos.lng;
      googlePlaceMapInstance.panTo({ lat: lat, lng: lng });
      googlePlaceMapInstance.setZoom(15);
    }
    if (marker._infoWindow) {
      setTimeout(() => {
        marker._infoWindow.open({
          map: googlePlaceMapInstance,
          anchor: marker
        });
      }, 300);
    }
  } else if (placeMap && typeof placeMap.setView === 'function') {
    // Leaflet
    placeMap.setView(marker.getLatLng(), 15, { animate: true });
    setTimeout(() => {
      marker.openPopup();
    }, 400);
  }

  // Highlight the card
  const cardId = type === 'hotel' ? `accommodation-${index}` : `specialty-${index}`;
  const card = document.getElementById(cardId);

  // Remove existing highlights
  document.querySelectorAll('.map-active').forEach(el => el.classList.remove('map-active'));

  if (card) {
    card.classList.add('map-active');
    // Remove highlight after 4 seconds
    setTimeout(() => card.classList.remove('map-active'), 4000);
  }
}

// Light tile layer for Leaflet (Clean OpenStreetMap tiles with NO watermark)
const TILE_URL = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
const TILE_ATTR = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';

function initPlaceDetailMap() {
  const placeMapEl = document.getElementById("place-map");
  if (!placeMapEl || placeMapEl._initialized) return;

  const lat = parseFloat(placeMapEl.dataset.lat);
  const lng = parseFloat(placeMapEl.dataset.lng);
  const name = placeMapEl.dataset.name || "Location";

  if (isNaN(lat) || isNaN(lng)) return;

  // ── 1. Google Maps Engine (Primary) ─────────────────────
  if (typeof google !== "undefined" && google.maps && google.maps.Map) {
    placeMapEl._initialized = true;
    const mapId = placeMapEl.dataset.mapId || undefined;

    const mapOptions = {
      center: { lat: lat, lng: lng },
      zoom: 13,
      mapId: mapId,
      mapTypeControl: false,
      streetViewControl: false,
      fullscreenControl: false,
      zoomControl: true,
      scrollwheel: false,
    };

    const gMap = new google.maps.Map(placeMapEl, mapOptions);
    googlePlaceMapInstance = gMap;

    // Primary place marker
    let placeMarker;
    const placeContent = document.createElement('div');
    placeContent.innerHTML = '<div style="background:linear-gradient(135deg,#6366f1,#4f46e5);width:22px;height:22px;border-radius:50%;border:3px solid white;box-shadow:0 2px 10px rgba(99,102,241,0.6);display:flex;align-items:center;justify-content:center;color:white;font-size:11px;font-weight:bold;">📍</div>';

    if (google.maps.marker && google.maps.marker.AdvancedMarkerElement && mapId) {
      try {
        placeMarker = new google.maps.marker.AdvancedMarkerElement({
          map: gMap,
          position: { lat: lat, lng: lng },
          title: name,
          content: placeContent
        });
      } catch (err) {
        placeMarker = new google.maps.Marker({
          map: gMap,
          position: { lat: lat, lng: lng },
          title: name,
        });
      }
    } else {
      placeMarker = new google.maps.Marker({
        map: gMap,
        position: { lat: lat, lng: lng },
        title: name,
      });
    }

    const placeInfoWindow = new google.maps.InfoWindow({
      content: `<div style="color:#0f172a;font-family:sans-serif;font-size:13px;padding:4px;"><strong style="font-size:14px;">${_escHtml(name)}</strong><br><span style="color:#64748b;font-size:11px;">📍 ${lat.toFixed(4)}, ${lng.toFixed(4)}</span><br><a href="https://www.google.com/maps?q=${lat},${lng}" target="_blank" rel="noopener noreferrer" style="color:#6366f1;font-size:12px;text-decoration:none;font-weight:600;display:inline-block;margin-top:4px;">Open in Google Maps ↗</a></div>`
    });
    placeMarker._infoWindow = placeInfoWindow;

    if (placeMarker.addListener) {
      placeMarker.addListener('click', () => {
        placeInfoWindow.open({ map: gMap, anchor: placeMarker });
      });
    }

    const bounds = new google.maps.LatLngBounds();
    bounds.extend({ lat: lat, lng: lng });

    // Hotel markers
    hotelMarkers = [];
    const hotelsJson = placeMapEl.dataset.hotels;
    if (hotelsJson) {
      try {
        const hotels = JSON.parse(hotelsJson);
        hotels.forEach((h, idx) => {
          if (h.latitude && h.longitude) {
            const hLat = parseFloat(h.latitude);
            const hLng = parseFloat(h.longitude);
            if (!isNaN(hLat) && !isNaN(hLng)) {
              let hMarker;
              const hContent = document.createElement('div');
              hContent.innerHTML = '<div style="background:linear-gradient(135deg,#f59e0b,#d97706);width:16px;height:16px;border-radius:50%;border:2px solid white;box-shadow:0 2px 8px rgba(245,158,11,0.5);display:flex;align-items:center;justify-content:center;color:white;font-size:8px;">🏨</div>';

              if (google.maps.marker && google.maps.marker.AdvancedMarkerElement && mapId) {
                try {
                  hMarker = new google.maps.marker.AdvancedMarkerElement({
                    map: gMap,
                    position: { lat: hLat, lng: hLng },
                    title: h.name,
                    content: hContent
                  });
                } catch (e) {
                  hMarker = new google.maps.Marker({
                    map: gMap,
                    position: { lat: hLat, lng: hLng },
                    title: h.name
                  });
                }
              } else {
                hMarker = new google.maps.Marker({
                  map: gMap,
                  position: { lat: hLat, lng: hLng },
                  title: h.name
                });
              }

              const hInfo = new google.maps.InfoWindow({
                content: `<div style="color:#0f172a;font-family:sans-serif;font-size:12px;padding:4px;"><strong style="font-size:13px;">🏨 ${_escHtml(h.name)}</strong><br><span style="color:#64748b;">${h.type ? _escHtml(h.type.charAt(0).toUpperCase() + h.type.slice(1)) : 'Hotel'}</span>${h.price_range ? '<br><span style="color:#059669;font-weight:600;">💰 ' + _escHtml(h.price_range) + '</span>' : ''}${h.address ? '<br><span style="color:#64748b;">📍 ' + _escHtml(h.address) + '</span>' : ''}<br><a href="https://www.google.com/maps?q=${hLat},${hLng}" target="_blank" rel="noopener noreferrer" style="color:#6366f1;font-size:11px;font-weight:600;display:inline-block;margin-top:4px;">Directions ↗</a></div>`
              });
              hMarker._infoWindow = hInfo;

              if (hMarker.addListener) {
                hMarker.addListener('click', () => {
                  hInfo.open({ map: gMap, anchor: hMarker });
                  document.querySelectorAll('.map-active').forEach(el => el.classList.remove('map-active'));
                  const card = document.getElementById(`accommodation-${idx}`);
                  if (card) {
                    card.classList.add('map-active');
                    card.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    setTimeout(() => card.classList.remove('map-active'), 4000);
                  }
                });
              }

              hotelMarkers.push(hMarker);
              bounds.extend({ lat: hLat, lng: hLng });
            } else {
              hotelMarkers.push(null);
            }
          } else {
            hotelMarkers.push(null);
          }
        });
      } catch (e) { /* ignore parse errors */ }
    }

    // Food markers
    foodMarkers = [];
    const foodsJson = placeMapEl.dataset.foods;
    if (foodsJson) {
      try {
        const foods = JSON.parse(foodsJson);
        foods.forEach((f, idx) => {
          if (f.latitude && f.longitude) {
            const fLat = parseFloat(f.latitude);
            const fLng = parseFloat(f.longitude);
            if (!isNaN(fLat) && !isNaN(fLng)) {
              let fMarker;
              const fContent = document.createElement('div');
              fContent.innerHTML = '<div style="background:linear-gradient(135deg,#22c55e,#16a34a);width:16px;height:16px;border-radius:50%;border:2px solid white;box-shadow:0 2px 8px rgba(34,197,94,0.5);display:flex;align-items:center;justify-content:center;color:white;font-size:8px;">🍛</div>';

              if (google.maps.marker && google.maps.marker.AdvancedMarkerElement && mapId) {
                try {
                  fMarker = new google.maps.marker.AdvancedMarkerElement({
                    map: gMap,
                    position: { lat: fLat, lng: fLng },
                    title: f.name,
                    content: fContent
                  });
                } catch (e) {
                  fMarker = new google.maps.Marker({
                    map: gMap,
                    position: { lat: fLat, lng: fLng },
                    title: f.name
                  });
                }
              } else {
                fMarker = new google.maps.Marker({
                  map: gMap,
                  position: { lat: fLat, lng: fLng },
                  title: f.name
                });
              }

              const fInfo = new google.maps.InfoWindow({
                content: `<div style="color:#0f172a;font-family:sans-serif;font-size:12px;padding:4px;"><strong style="font-size:13px;">🍛 ${_escHtml(f.name)}</strong><br><span style="color:#64748b;">${_escHtml(f.category || 'Food')}</span>${f.where_to_find ? '<br><span style="color:#64748b;">📍 ' + _escHtml(f.where_to_find) + '</span>' : ''}<br><a href="https://www.google.com/maps?q=${fLat},${fLng}" target="_blank" rel="noopener noreferrer" style="color:#6366f1;font-size:11px;font-weight:600;display:inline-block;margin-top:4px;">Directions ↗</a></div>`
              });
              fMarker._infoWindow = fInfo;

              if (fMarker.addListener) {
                fMarker.addListener('click', () => {
                  fInfo.open({ map: gMap, anchor: fMarker });
                  document.querySelectorAll('.map-active').forEach(el => el.classList.remove('map-active'));
                  const card = document.getElementById(`specialty-${idx}`);
                  if (card) {
                    card.classList.add('map-active');
                    card.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    setTimeout(() => card.classList.remove('map-active'), 4000);
                  }
                });
              }

              foodMarkers.push(fMarker);
              bounds.extend({ lat: fLat, lng: fLng });
            } else {
              foodMarkers.push(null);
            }
          } else {
            foodMarkers.push(null);
          }
        });
      } catch (e) { /* ignore parse errors */ }
    }

    // Fit bounds if multiple markers exist
    if (hotelMarkers.some(m => m) || foodMarkers.some(m => m)) {
      gMap.fitBounds(bounds, 30);
    }

    // User distance calculation
    const distText = document.getElementById("distance-text");
    if (distText && navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          const R = 6371;
          const dLat = ((pos.coords.latitude - lat) * Math.PI) / 180;
          const dLon = ((pos.coords.longitude - lng) * Math.PI) / 180;
          const a =
            Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos((lat * Math.PI) / 180) *
            Math.cos((pos.coords.latitude * Math.PI) / 180) *
            Math.sin(dLon / 2) *
            Math.sin(dLon / 2);
          const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
          const km = R * c;
          distText.textContent = `You are approximately ${Math.round(km)} km away`;
        },
        () => {
          distText.textContent = "";
        }
      );
    }

    return;
  }

  // ── 2. Leaflet Fallback (using standard OSM tiles with NO watermark) ───
  if (typeof L !== "undefined") {
    placeMapEl._initialized = true;
    placeMap = L.map("place-map", {
      scrollWheelZoom: false,
      zoomControl: true,
    }).setView([lat, lng], 13);

    L.tileLayer(TILE_URL, { attribution: TILE_ATTR, maxZoom: 18 }).addTo(placeMap);

    // Custom marker icon — Place (indigo)
    const placeIcon = L.divIcon({
      html: '<div style="background:linear-gradient(135deg,#6366f1,#4f46e5);width:16px;height:16px;border-radius:50%;border:2.5px solid white;box-shadow:0 2px 10px rgba(99,102,241,0.5)"></div>',
      className: "",
      iconSize: [16, 16],
      iconAnchor: [8, 8],
    });

    L.marker([lat, lng], { icon: placeIcon }).addTo(placeMap).bindPopup(
      `<strong>${_escHtml(name)}</strong><br><small>📍 ${lat.toFixed(4)}, ${lng.toFixed(4)}</small><br><a href="https://www.google.com/maps?q=${lat},${lng}" target="_blank" style="color:#6366f1;font-size:12px;">Open in Google Maps</a>`
    );

    const bounds = L.latLngBounds([[lat, lng]]);

    // Hotel markers (orange)
    hotelMarkers = [];
    const hotelsJson = placeMapEl.dataset.hotels;
    if (hotelsJson) {
      try {
        const hotels = JSON.parse(hotelsJson);
        const hotelIcon = L.divIcon({
          html: '<div style="background:linear-gradient(135deg,#f59e0b,#d97706);width:12px;height:12px;border-radius:50%;border:2px solid white;box-shadow:0 2px 8px rgba(245,158,11,0.5)"></div>',
          className: "",
          iconSize: [12, 12],
          iconAnchor: [6, 6],
        });

        hotels.forEach((h, idx) => {
          if (h.latitude && h.longitude) {
            const popup = `<strong>🏨 ${_escHtml(h.name)}</strong><br><small>${h.type ? _escHtml(h.type.charAt(0).toUpperCase() + h.type.slice(1)) : 'Hotel'}</small>${h.price_range ? '<br>💰 ' + _escHtml(h.price_range) : ''}${h.address ? '<br>📍 ' + _escHtml(h.address) : ''}<br><a href="https://www.google.com/maps?q=${h.latitude},${h.longitude}" target="_blank" style="color:#6366f1;font-size:12px;">Directions</a>`;
            const marker = L.marker([h.latitude, h.longitude], { icon: hotelIcon })
              .addTo(placeMap)
              .bindPopup(popup);

            // Click marker → highlight card
            marker.on('click', () => {
              document.querySelectorAll('.map-active').forEach(el => el.classList.remove('map-active'));
              const card = document.getElementById(`accommodation-${idx}`);
              if (card) {
                card.classList.add('map-active');
                card.scrollIntoView({ behavior: 'smooth', block: 'center' });
                setTimeout(() => card.classList.remove('map-active'), 4000);
              }
            });

            hotelMarkers.push(marker);
            bounds.extend([h.latitude, h.longitude]);
          } else {
            hotelMarkers.push(null);
          }
        });
      } catch (e) { /* ignore parse errors */ }
    }

    // Food/Specialty markers (green)
    foodMarkers = [];
    const foodsJson = placeMapEl.dataset.foods;
    if (foodsJson) {
      try {
        const foods = JSON.parse(foodsJson);
        const foodIcon = L.divIcon({
          html: '<div style="background:linear-gradient(135deg,#22c55e,#16a34a);width:12px;height:12px;border-radius:50%;border:2px solid white;box-shadow:0 2px 8px rgba(34,197,94,0.5)"></div>',
          className: "",
          iconSize: [12, 12],
          iconAnchor: [6, 6],
        });

        foods.forEach((f, idx) => {
          if (f.latitude && f.longitude) {
            const popup = `<strong>🍛 ${_escHtml(f.name)}</strong><br><small>${_escHtml(f.category || 'Food')}</small>${f.where_to_find ? '<br>📍 ' + _escHtml(f.where_to_find) : ''}<br><a href="https://www.google.com/maps?q=${f.latitude},${f.longitude}" target="_blank" style="color:#6366f1;font-size:12px;">Directions</a>`;
            const marker = L.marker([f.latitude, f.longitude], { icon: foodIcon })
              .addTo(placeMap)
              .bindPopup(popup);

            // Click marker → highlight card
            marker.on('click', () => {
              document.querySelectorAll('.map-active').forEach(el => el.classList.remove('map-active'));
              const card = document.getElementById(`specialty-${idx}`);
              if (card) {
                card.classList.add('map-active');
                card.scrollIntoView({ behavior: 'smooth', block: 'center' });
                setTimeout(() => card.classList.remove('map-active'), 4000);
              }
            });

            foodMarkers.push(marker);
            bounds.extend([f.latitude, f.longitude]);
          } else {
            foodMarkers.push(null);
          }
        });
      } catch (e) { /* ignore parse errors */ }
    }

    // Fit bounds if we have extra markers
    if (hotelMarkers.some(m => m) || foodMarkers.some(m => m)) {
      placeMap.fitBounds(bounds.pad(0.3));
    }

    // Show user distance
    const distText = document.getElementById("distance-text");
    if (distText && navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          const R = 6371;
          const dLat = ((pos.coords.latitude - lat) * Math.PI) / 180;
          const dLon = ((pos.coords.longitude - lng) * Math.PI) / 180;
          const a =
            Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos((lat * Math.PI) / 180) *
            Math.cos((pos.coords.latitude * Math.PI) / 180) *
            Math.sin(dLon / 2) *
            Math.sin(dLon / 2);
          const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
          const km = R * c;
          distText.textContent = `You are approximately ${Math.round(km)} km away`;
        },
        () => {
          distText.textContent = "";
        }
      );
    }

    // User location marker (blue dot)
    let userMarker = null;

    function placeUserMarker(lat, lng) {
      if (!placeMap) return;
      if (userMarker) {
        placeMap.removeLayer(userMarker);
        userMarker = null;
      }
      const blueIcon = L.divIcon({
        html: '<div style="background:#3B82F6;width:18px;height:18px;border-radius:50%;border:3px solid white;box-shadow:0 2px 12px rgba(59,130,246,0.7)"></div>',
        className: '',
        iconSize: [18, 18],
        iconAnchor: [9, 9],
      });
      userMarker = L.marker([lat, lng], { icon: blueIcon }).addTo(placeMap);
      var ring = L.circleMarker([lat, lng], {
        radius: 22,
        color: '#3B82F6',
        fillColor: '#3B82F6',
        fillOpacity: 0.1,
        weight: 2,
        opacity: 0.3,
      }).addTo(placeMap);
      userMarker._ring = ring;
      setTimeout(function () {
        if (userMarker && userMarker._ring) {
          placeMap.removeLayer(userMarker._ring);
          userMarker._ring = null;
        }
      }, 2000);
    }

    var cached = window.HY && HY.getLocation();
    if (cached) {
      setTimeout(function () { placeUserMarker(cached.lat, cached.lng); }, 400);
    }

    document.addEventListener('hy-location-updated', function (e) {
      if (e.detail && e.detail.lat && e.detail.lng) {
        placeUserMarker(e.detail.lat, e.detail.lng);
      }
    });
  }
}

// Global callback for Google Maps API script
window._hyInitPlaceDetailMap = initPlaceDetailMap;

document.addEventListener("DOMContentLoaded", () => {
  initPlaceDetailMap();

  /* ── Admin Map (click to set coordinates) ────────── */
  const adminMapEl = document.getElementById("admin-map");
  if (adminMapEl && typeof L !== "undefined") {
    const existingLat = parseFloat(adminMapEl.dataset.lat);
    const existingLng = parseFloat(adminMapEl.dataset.lng);

    const defaultLat = !isNaN(existingLat) ? existingLat : 20.5937;
    const defaultLng = !isNaN(existingLng) ? existingLng : 78.9629;
    const defaultZoom = !isNaN(existingLat) ? 12 : 5;

    const map = L.map("admin-map").setView([defaultLat, defaultLng], defaultZoom);
    L.tileLayer(TILE_URL, { attribution: TILE_ATTR, maxZoom: 18 }).addTo(map);
    setTimeout(() => map.invalidateSize(), 250);

    const latInput = document.getElementById("lat-input");
    const lngInput = document.getElementById("lng-input");

    let marker = null;

    // Place existing marker if editing
    if (!isNaN(existingLat) && !isNaN(existingLng)) {
      marker = L.marker([existingLat, existingLng]).addTo(map);
    }

    // Click to set coordinate
    map.on("click", (e) => {
      const { lat, lng } = e.latlng;
      if (latInput) latInput.value = lat.toFixed(6);
      if (lngInput) lngInput.value = lng.toFixed(6);

      if (marker) {
        marker.setLatLng([lat, lng]);
      } else {
        marker = L.marker([lat, lng]).addTo(map);
      }
    });
  }

  /* ── District Map ──────────────────────────────── */
  const districtMapEl = document.getElementById("district-map");
  if (districtMapEl && typeof L !== "undefined") {
    const placesJson = districtMapEl.dataset.places;
    if (placesJson) {
      try {
        const places = JSON.parse(placesJson);
        const validPlaces = places.filter(p => p.latitude && p.longitude);

        if (validPlaces.length > 0) {
          const map = L.map("district-map", {
            scrollWheelZoom: false,
            zoomControl: true,
          });

          L.tileLayer(TILE_URL, { attribution: TILE_ATTR, maxZoom: 18 }).addTo(map);

          const bounds = L.latLngBounds();

          validPlaces.forEach(p => {
            const lat = parseFloat(p.latitude);
            const lng = parseFloat(p.longitude);
            if (!isNaN(lat) && !isNaN(lng)) {
              const cat = (p.category || '').toLowerCase();
              let bg = 'linear-gradient(135deg,#FF7A18,#E0620E)';
              let emoji = '📍';

              if (cat.includes('temple') || cat.includes('religious')) {
                bg = 'linear-gradient(135deg,#d97706,#b45309)'; emoji = '🛕';
              } else if (cat.includes('mountain') || cat.includes('hill')) {
                bg = 'linear-gradient(135deg,#6366f1,#4f46e5)'; emoji = '⛰️';
              } else if (cat.includes('waterfall') || cat.includes('lake')) {
                bg = 'linear-gradient(135deg,#06b6d4,#0891b2)'; emoji = '🌊';
              } else if (cat.includes('historical') || cat.includes('monument')) {
                bg = 'linear-gradient(135deg,#e11d48,#be123c)'; emoji = '🏛️';
              } else if (cat.includes('nature') || cat.includes('sanctuary')) {
                bg = 'linear-gradient(135deg,#10b981,#047857)'; emoji = '🌿';
              } else if (cat.includes('cultural')) {
                bg = 'linear-gradient(135deg,#8b5cf6,#6d28d9)'; emoji = '🎭';
              }

              const markerIcon = L.divIcon({
                html: `<div style="background:${bg};width:24px;height:24px;border-radius:50%;border:2px solid white;box-shadow:0 3px 10px rgba(0,0,0,0.3);display:flex;align-items:center;justify-content:center;font-size:12px;">${emoji}</div>`,
                className: "",
                iconSize: [24, 24],
                iconAnchor: [12, 12],
              });

              const popupHtml = `
                <div style="font-family:sans-serif;padding:4px;">
                  <strong style="color:var(--text-primary,#111);font-size:13px;">${p.name}</strong><br>
                  <span style="color:#64748b;font-size:11px;">📍 ${p.category || 'Tourist Spot'}</span><br>
                  <a href="/place/${p.slug}" style="color:#FF7A18;font-weight:600;font-size:12px;text-decoration:none;display:inline-block;margin-top:6px;">View Place Details →</a>
                </div>
              `;

              L.marker([lat, lng], { icon: markerIcon })
                .addTo(map)
                .bindPopup(popupHtml, _getResponsivePopupOptions());

              bounds.extend([lat, lng]);
            }
          });

          if (bounds.isValid()) {
            map.fitBounds(bounds.pad(0.2));
          } else {
            map.setView([25.6, 85.1], 8);
          }

          setTimeout(() => map.invalidateSize(), 250);
        }
      } catch (e) { console.error("District map error:", e); }
    }
  }

  /* ── Itinerary Route Map ────────────────────────── */
  const itineraryMapEl = document.getElementById("itinerary-map");
  if (itineraryMapEl && typeof L !== "undefined") {
    const daysJson = itineraryMapEl.dataset.days;
    if (daysJson) {
      try {
        const days = JSON.parse(daysJson);
        const routePoints = [];

        const map = L.map("itinerary-map", {
          scrollWheelZoom: false,
          zoomControl: true,
        });

        L.tileLayer(TILE_URL, { attribution: TILE_ATTR, maxZoom: 18 }).addTo(map);

        const bounds = L.latLngBounds();
        let stopCount = 0;

        const dayKeys = Object.keys(days).sort((a, b) => parseInt(a) - parseInt(b));
        dayKeys.forEach(dayNum => {
          const items = days[dayNum];
          items.forEach(item => {
            if (item.latitude && item.longitude) {
              stopCount++;
              const lat = parseFloat(item.latitude);
              const lng = parseFloat(item.longitude);
              routePoints.push([lat, lng]);

              const numberIcon = L.divIcon({
                html: `<div style="background:#FF7A18;color:white;font-weight:700;font-size:11px;width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;border:2px solid white;box-shadow:0 2px 8px rgba(0,0,0,0.5)">${stopCount}</div>`,
                className: "",
                iconSize: [24, 24],
                iconAnchor: [12, 12],
              });

              const popupHtml = `
                <div style="font-family:sans-serif;padding:4px;">
                  <span style="background:#FF7A18;color:white;font-size:10px;padding:2px 6px;border-radius:10px;font-weight:700;">Day ${dayNum} • Stop ${stopCount}</span><br>
                  <strong style="color:var(--text-primary,#111);font-size:13px;display:block;margin-top:4px;">${item.place_name}</strong>
                  <span style="color:#64748b;font-size:11px;">📍 ${item.category || 'Spot'}</span><br>
                  <a href="/place/${item.place_slug}" style="color:#FF7A18;font-weight:600;font-size:12px;text-decoration:none;display:inline-block;margin-top:6px;">View Place →</a>
                </div>
              `;

              L.marker([lat, lng], { icon: numberIcon })
                .addTo(map)
                .bindPopup(popupHtml, _getResponsivePopupOptions());

              bounds.extend([lat, lng]);
            }
          });
        });

        // Draw polyline connecting stops in itinerary order
        if (routePoints.length > 1) {
          L.polyline(routePoints, {
            color: '#FF7A18',
            weight: 3.5,
            opacity: 0.85,
            dashArray: '6, 8'
          }).addTo(map);
        }

        if (bounds.isValid()) {
          map.fitBounds(bounds.pad(0.25));
        } else {
          map.setView([25.6, 85.1], 7);
        }

        setTimeout(() => map.invalidateSize(), 250);

      } catch (e) { console.error("Itinerary map error:", e); }
    }
  }

});


// Explore Map Radius Control
window.HY_setSearchRadius = function(radiusKm) {
  const km = parseFloat(radiusKm) || 5.0;
  console.log('[Map] Updating search radius:', km, 'km');
  if (window.SNS && typeof window.SNS.setRadius === 'function') {
    window.SNS.setRadius(km);
  }
  if (window.HY_RADIUS_CIRCLE && typeof window.HY_RADIUS_CIRCLE.setRadius === 'function') {
    window.HY_RADIUS_CIRCLE.setRadius(km * 1000);
  }
};
