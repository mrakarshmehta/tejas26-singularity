/* ═══════════════════════════════════════════════════════════════════
   HiddenYatra — MapLeaflet (Leaflet Engine Adapter)
   Wraps the existing Leaflet map instance for the hybrid system.
   DOES NOT modify the existing Leaflet initialization in explore_map.
   Instead, it receives the already-initialized `map` instance.
   ═══════════════════════════════════════════════════════════════════ */

(function (root) {
  'use strict';

  class MapLeafletAdapter {
    /**
     * @param {L.Map} leafletMap - The existing L.map instance
     */
    constructor(leafletMap) {
      if (!leafletMap) throw new Error('[MapLeafletAdapter] Missing Leaflet map instance');

      /** @type {L.Map} */
      this.map = leafletMap;

      /** @type {L.TileLayer|null} Current base tile layer */
      this._baseLayer = null;

      /** @type {Map<string, L.Layer>} Active overlay layers (layerId → L.Layer) */
      this._overlays = new Map();

      /** @type {HTMLElement} The map container element */
      this.container = leafletMap.getContainer();

      // Bind to MapState for view sync
      this._bindStateSync();
    }

    /* ── State Synchronization ─────────────────────── */

    /** @private */
    _bindStateSync() {
      const state = root.HYMapState;
      if (!state) return;

      // Leaflet → MapState: sync view on move/zoom
      this.map.on('moveend', () => {
        if (state.activeEngine !== 'leaflet') return;
        const center = this.map.getCenter();
        state.setView({
          lat: center.lat,
          lng: center.lng,
          zoom: this.map.getZoom(),
        }, 'leaflet');
      });

      // MapState → Leaflet: respond to view changes from other engines
      state.on('view', (data) => {
        if (data.source === 'leaflet') return; // Don't echo our own changes
        if (state.activeEngine !== 'leaflet') return;
        this.map.setView([data.state.lat, data.state.lng], data.state.zoom, { animate: false });
      });
    }

    /* ── Base Map Switching ────────────────────────── */

    /**
     * Switch the base tile layer.
     * @param {string} sourceId - Key from HYTileSources
     */
    setBasemap(sourceId) {
      const sources = root.HYTileSources;
      if (!sources || !sources[sourceId]) {
        console.warn(`[MapLeafletAdapter] Unknown tile source: ${sourceId}`);
        return;
      }

      const src = sources[sourceId];

      // Remove current base layer
      if (this._baseLayer) {
        this.map.removeLayer(this._baseLayer);
      }

      // Create and add new tile layer
      const opts = {
        attribution: src.attribution,
        maxZoom: src.maxZoom || 19,
      };
      if (src.subdomains) opts.subdomains = src.subdomains;

      this._baseLayer = L.tileLayer(src.url, opts);
      this._baseLayer.addTo(this.map);

      // Move base layer to bottom
      this._baseLayer.bringToBack();
    }

    /** @returns {string|null} The current base tile source ID */
    getCurrentBasemap() {
      return this._currentBasemapId || 'carto_light';
    }

    /* ── GeoJSON Layer Management ──────────────────── */

    /**
     * Add a GeoJSON layer to the map.
     * @param {string} layerId
     * @param {Object} geojsonData - GeoJSON FeatureCollection
     * @param {Object} [styleOpts] - Style options from layer definition
     * @returns {L.GeoJSON} The created layer
     */
    addGeoJSONLayer(layerId, geojsonData, styleOpts) {
      // Remove existing layer with same ID if present
      this.removeLayer(layerId);

      const def = root.HYLayerRegistry ? root.HYLayerRegistry.get(layerId) : null;
      const style = styleOpts || (def ? def.style : {});

      const layer = L.geoJSON(geojsonData, {
        pointToLayer: (feature, latlng) => {
          if (layerId === 'waterfalls_geo' || layerId === 'waterfalls' || layerId === 'hotels' || layerId === 'homestays') {
            const mColor = layerId === 'hotels' ? '#2563eb' : (layerId === 'homestays' ? '#059669' : (style.fillColor || style.color || '#06b6d4'));
            const cls = layerId === 'hotels' ? 'hy-hotel-marker' : (layerId === 'homestays' ? 'hy-homestay-marker' : 'hy-waterfall-marker');
            return L.circleMarker(latlng, {
              radius: style.radius || 7,
              fillColor: mColor,
              color: '#ffffff',
              weight: 2,
              opacity: 1.0,
              fillOpacity: style.fillOpacity !== undefined ? style.fillOpacity : 0.9,
              className: cls,
            });
          }
          return L.marker(latlng);
        },

        style: (feature) => ({
          color: style.stroke || '#6366f1',
          weight: style.strokeWidth || 2,
          opacity: style.strokeOpacity || 0.8,
          fillColor: style.fillColor || style.stroke || '#6366f1',
          fillOpacity: (feature.geometry && (feature.geometry.type === 'LineString' || feature.geometry.type === 'MultiLineString'))
            ? 0
            : (style.fillOpacity !== undefined ? style.fillOpacity : 0.2),
          dashArray: style.dashArray || null,
        }),

        onEachFeature: (feature, featureLayer) => {
          const props = feature.properties || {};

          // Interactive hover highlighting
          featureLayer.on('mouseover', () => {
            const isLine = feature.geometry && (feature.geometry.type === 'LineString' || feature.geometry.type === 'MultiLineString');
            const isPoint = feature.geometry && feature.geometry.type === 'Point';
            if (isLine) {
              featureLayer.setStyle({
                weight: (style.strokeWidth || 3) + 2,
                opacity: 1.0,
              });
            } else if (isPoint) {
              if (typeof featureLayer.setStyle === 'function') {
                featureLayer.setStyle({
                  radius: (style.radius || 7) + 2,
                  fillOpacity: 1.0,
                });
              }
            } else {
              featureLayer.setStyle({
                fillOpacity: Math.min(1.0, (style.fillOpacity || 0.35) + 0.25),
                color: style.hoverStroke || style.stroke || '#0891b2',
                weight: (style.strokeWidth || 2) + 1,
              });
            }
            if (typeof featureLayer.bringToFront === 'function') {
              featureLayer.bringToFront();
            }
          });

          featureLayer.on('mouseout', () => {
            layer.resetStyle(featureLayer);
          });

          // Rich Tooltip with Category Metadata
          let tooltipHtml = '';
          if (layerId === 'rivers') {
            const hiName = props.name_hi ? ` <span style="color:#64748b;font-size:0.78rem;">(${props.name_hi})</span>` : '';
            const segments = props.segment_count ? ` • <span style="font-size:0.75rem;color:#64748b;">${props.segment_count} OSM segments</span>` : '';
            tooltipHtml = `<div style="font-family:inherit;line-height:1.3;">
              <strong style="font-size:0.88rem;color:#0284c7;">🌊 ${props.name || 'River'}</strong>${hiName}<br>
              <span style="font-size:0.75rem;color:#475569;">OpenStreetMap Waterway${segments}</span>
            </div>`;
          } else if (layerId === 'lakes_dams') {
            const hiName = props.name_hi ? ` <span style="color:#64748b;font-size:0.78rem;">(${props.name_hi})</span>` : '';
            const wtype = props.water || props.natural || 'waterbody';
            tooltipHtml = `<div style="font-family:inherit;line-height:1.3;">
              <strong style="font-size:0.88rem;color:#0891b2;">💧 ${props.name || 'Waterbody'}</strong>${hiName}<br>
              <span style="font-size:0.75rem;color:#475569;text-transform:capitalize;">OpenStreetMap ${wtype}</span>
            </div>`;
          } else if (layerId === 'forests') {
            const hiName = props.name_hi ? ` <span style="color:#64748b;font-size:0.78rem;">(${props.name_hi})</span>` : '';
            const ftype = props.type || props.boundary || props.landuse || 'Protected Area';
            tooltipHtml = `<div style="font-family:inherit;line-height:1.3;">
              <strong style="font-size:0.88rem;color:#15803d;">🌲 ${props.name || 'Forest Area'}</strong>${hiName}<br>
              <span style="font-size:0.75rem;color:#475569;text-transform:capitalize;">OpenStreetMap ${ftype}</span>
            </div>`;
          } else if (layerId === 'waterfalls_geo' || layerId === 'waterfalls') {
            const hiName = props.name_hi ? ` <span style="color:#64748b;font-size:0.78rem;">(${props.name_hi})</span>` : '';
            tooltipHtml = `<div style="font-family:inherit;line-height:1.3;">
              <strong style="font-size:0.88rem;color:#0891b2;">💦 ${props.name || 'Waterfall'}</strong>${hiName}<br>
              <span style="font-size:0.75rem;color:#475569;">OpenStreetMap Waterfall</span>
            </div>`;
            const popupHtml = `<div style="font-family:inherit;line-height:1.4;padding:4px;">
              <h4 style="margin:0 0 4px 0;font-size:0.95rem;color:#0e7490;">💦 ${props.name || 'Waterfall'}</h4>
              <p style="margin:0 0 6px 0;font-size:0.8rem;color:#475569;">
                <strong>Coordinates:</strong> ${feature.geometry.coordinates[1].toFixed(4)}°N, ${feature.geometry.coordinates[0].toFixed(4)}°E<br>
                <strong>Source:</strong> OpenStreetMap (${props.osm_id || 'node'})
              </p>
              ${props.source_url ? `<a href="${props.source_url}" target="_blank" rel="noopener noreferrer" style="font-size:0.75rem;color:#0284c7;text-decoration:underline;">View on OpenStreetMap ↗</a>` : ''}
            </div>`;
            featureLayer.bindPopup(popupHtml);
          } else if (layerId === 'block_boundaries' || layerId === 'blocks') {
            const bName = props.name || 'Block';
            const dName = props.district_name || 'District';
            tooltipHtml = `<div style="font-family:inherit;line-height:1.3;">
              <strong style="font-size:0.88rem;color:#475569;">🔲 ${bName}</strong><br>
              <span style="font-size:0.75rem;color:#64748b;">${dName} District</span>
            </div>`;
            const isSeeded = !!props.block_id;
            const linkHtml = isSeeded
              ? `<a href="/state/bihar/${props.district_slug || 'bihar'}/${props.slug}" style="display:inline-block;margin-top:6px;padding:4px 10px;background:var(--primary,#f59e0b);color:#fff;border-radius:4px;font-size:0.78rem;text-decoration:none;font-weight:500;">Explore ${bName} Block →</a>`
              : `<span style="display:inline-block;margin-top:4px;font-size:0.72rem;color:#94a3b8;font-style:italic;">Administrative C.D. Block</span>`;
            const popupHtml = `<div style="font-family:inherit;line-height:1.4;padding:4px;min-width:180px;">
              <h4 style="margin:0 0 4px 0;font-size:0.95rem;color:#1e293b;">🔲 ${bName} Block</h4>
              <p style="margin:0 0 6px 0;font-size:0.8rem;color:#475569;">
                <strong>District:</strong> ${dName}<br>
                ${props.census_code ? `<strong>Census Code:</strong> ${props.census_code}<br>` : ''}
                ${props.lgd_code ? `<strong>LGD Code:</strong> ${props.lgd_code}<br>` : ''}
              </p>
              ${linkHtml}
            </div>`;
            featureLayer.bindPopup(popupHtml);
          } else if (layerId === 'hotels') {
            const hName = props.name || 'Hotel';
            const dName = props.district_name || 'Bihar';
            tooltipHtml = `<div style="font-family:inherit;line-height:1.3;">
              <strong style="font-size:0.88rem;color:#1d4ed8;">🏨 ${hName}</strong><br>
              <span style="font-size:0.75rem;color:#64748b;">${dName} District</span>
            </div>`;
            const phoneHtml = props.phone ? `<p style="margin:2px 0 6px 0;font-size:0.8rem;color:#475569;"><strong>Phone:</strong> <a href="tel:${props.phone}" style="color:#2563eb;text-decoration:none;">${props.phone}</a></p>` : '';
            const addrHtml = props.address ? `<p style="margin:2px 0 6px 0;font-size:0.78rem;color:#64748b;">📍 ${props.address}</p>` : '';
            const coords = feature.geometry ? feature.geometry.coordinates : [0, 0];
            const popupHtml = `<div style="font-family:inherit;line-height:1.4;padding:4px;min-width:190px;">
              <h4 style="margin:0 0 4px 0;font-size:0.95rem;color:#1e3a8a;">🏨 ${hName}</h4>
              <span style="display:inline-block;padding:2px 6px;background:#dbeafe;color:#1e40af;border-radius:4px;font-size:0.72rem;font-weight:600;margin-bottom:6px;">${dName}</span>
              ${addrHtml}
              ${phoneHtml}
              <div style="margin-top:8px;">
                <a href="https://www.google.com/maps/dir/?api=1&destination=${coords[1]},${coords[0]}" target="_blank" rel="noopener noreferrer" style="display:inline-block;padding:4px 10px;background:#2563eb;color:#fff;border-radius:4px;font-size:0.76rem;text-decoration:none;font-weight:500;">Get Directions ↗</a>
              </div>
            </div>`;
            featureLayer.bindPopup(popupHtml);
          } else if (layerId === 'homestays') {
            const sTitle = props.title || 'Homestay';
            const priceText = props.price_per_night && props.price_per_night > 0 ? `₹${props.price_per_night}/night` : 'Free Cultural Stay';
            const dName = props.district_name || 'Bihar';
            tooltipHtml = `<div style="font-family:inherit;line-height:1.3;">
              <strong style="font-size:0.88rem;color:#047857;">🏡 ${sTitle}</strong><br>
              <span style="font-size:0.75rem;color:#059669;font-weight:600;">${priceText}</span> • <span style="font-size:0.75rem;color:#64748b;">${dName}</span>
            </div>`;
            const imgHtml = props.cover_image ? `<img src="/static/uploads/stays/${props.cover_image}" style="width:100%;height:88px;object-fit:cover;border-radius:6px;margin-bottom:6px;" onerror="this.style.display='none'">` : '';
            const propType = (props.property_type || 'Homestay').replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
            const ratingText = props.avg_rating ? `⭐ ${props.avg_rating} (${props.review_count || 0})` : '⭐ 5.0 (New)';
            const popupHtml = `<div style="font-family:inherit;line-height:1.4;padding:4px;min-width:200px;max-width:240px;">
              ${imgHtml}
              <h4 style="margin:0 0 4px 0;font-size:0.92rem;color:#064e3b;line-height:1.3;">🏡 ${sTitle}</h4>
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                <span style="font-size:0.72rem;color:#065f46;background:#d1fae5;padding:2px 6px;border-radius:4px;font-weight:600;">${propType}</span>
                <span style="font-size:0.72rem;color:#475569;font-weight:500;">${ratingText}</span>
              </div>
              <p style="margin:0 0 6px 0;font-size:0.82rem;color:#059669;font-weight:700;">${priceText}</p>
              <a href="${props.detail_url || '#'}" style="display:inline-block;width:100%;text-align:center;box-sizing:border-box;padding:5px 10px;background:#059669;color:#fff;border-radius:4px;font-size:0.78rem;text-decoration:none;font-weight:600;">Explore Homestay →</a>
            </div>`;
            featureLayer.bindPopup(popupHtml);
          } else {
            const name = props.name || props.NAME || props.district || props.DISTRICT || 'Region';
            tooltipHtml = `<strong>📍 ${name}</strong>`;
          }

          featureLayer.bindTooltip(tooltipHtml, {
            sticky: true,
            direction: 'top',
            className: 'hy-geo-tooltip',
          });

          // Click handler — zoom to feature bounds
          if (def && def.interactive) {
            featureLayer.on('click', () => {
              const bounds = featureLayer.getBounds();
              if (bounds.isValid()) {
                this.map.fitBounds(bounds, { padding: [40, 40], maxZoom: 13 });
              }
              // Emit selection event
              if (root.HYMapState) {
                root.HYMapState._notify('layer', {
                  layerId,
                  event: 'feature-click',
                  feature: feature,
                });
              }
            });
          }
        },
      });

      layer.addTo(this.map);
      this._overlays.set(layerId, layer);

      // Also register in the LayerRegistry
      if (root.HYLayerRegistry) {
        root.HYLayerRegistry.setLeafletLayer(layerId, layer);
      }

      return layer;
    }

    /**
     * Remove a layer from the map.
     * @param {string} layerId
     */
    removeLayer(layerId) {
      const layer = this._overlays.get(layerId);
      if (layer) {
        this.map.removeLayer(layer);
        this._overlays.delete(layerId);
        if (root.HYLayerRegistry) {
          root.HYLayerRegistry.removeLeafletLayer(layerId);
        }
      }
    }

    /**
     * Add culture markers to the Leaflet map.
     * @param {string} layerId
     * @param {Array<Object>} items
     * @param {Object} [styleOpts]
     * @returns {L.LayerGroup}
     */
    addCultureMarkerLayer(layerId, items, styleOpts) {
      this.removeLayer(layerId);
      const style = styleOpts || {};
      const markerColor = style.markerColor || '#d97706';
      const markers = [];

      items.forEach(item => {
        if (item.lat && item.lng) {
          const cm = L.circleMarker([item.lat, item.lng], {
            radius: 7,
            fillColor: markerColor,
            color: '#ffffff',
            weight: 2,
            opacity: 1.0,
            fillOpacity: 0.9,
          });

          const popupContent = `
            <div style="font-family:sans-serif;min-width:180px;line-height:1.4;">
              <div style="display:flex;align-items:center;gap:4px;margin-bottom:4px;">
                <span>${item.icon || '🏺'}</span>
                <strong style="color:${markerColor};font-size:0.75rem;text-transform:uppercase;">${item.subcategory || 'Culture'}</strong>
              </div>
              <h4 style="margin:2px 0 4px;font-size:0.9rem;">${item.name}</h4>
              <div style="font-size:0.75rem;color:#64748b;">📍 ${item.district || 'Bihar'}</div>
              ${item.description ? `<p style="margin:4px 0;font-size:0.75rem;color:#475569;">${item.description}</p>` : ''}
              ${item.detail_url ? `<a href="${item.detail_url}" style="font-size:0.75rem;color:${markerColor};font-weight:600;">Explore →</a>` : ''}
            </div>
          `;
          cm.bindPopup(popupContent);
          markers.push(cm);
        }
      });

      const layerGroup = L.layerGroup(markers);
      layerGroup.addTo(this.map);
      this._overlays.set(layerId, layerGroup);
      return layerGroup;
    }

    /**
     * Toggle layer visibility.
     * @param {string} layerId
     * @param {boolean} visible
     */
    async toggleLayer(layerId, visible) {
      if (visible) {
        // Handle culture parent group
        if (layerId === 'culture') {
          const cultureChildren = ['culture_heritage', 'culture_festivals', 'culture_crafts', 'culture_performing_arts', 'culture_food'];
          for (const childId of cultureChildren) {
            await this.toggleLayer(childId, true);
          }
          return;
        }

        // Check if layer is already loaded
        if (this._overlays.has(layerId)) {
          const layer = this._overlays.get(layerId);
          if (!this.map.hasLayer(layer)) {
            layer.addTo(this.map);
          }
          return;
        }

        // Need to load the layer data
        const def = root.HYLayerRegistry ? root.HYLayerRegistry.get(layerId) : null;
        if (!def) return;

        // Culture point markers
        if (layerId.startsWith('culture_') && def.source) {
          const data = await root.HYLayerRegistry.fetchData(layerId);
          if (data && data.items) {
            this.addCultureMarkerLayer(layerId, data.items, def.style);
          }
          return;
        }

        const isGeoJSON = (def.sourceType === 'geojson' || def.type === 'geojson');
        if (isGeoJSON && def.source) {
          const data = await root.HYLayerRegistry.fetchData(layerId);
          if (data) {
            this.addGeoJSONLayer(layerId, data, def.style);
          }
        }
      } else {
        // Handle culture parent group
        if (layerId === 'culture') {
          const cultureChildren = ['culture_heritage', 'culture_festivals', 'culture_crafts', 'culture_performing_arts', 'culture_food'];
          for (const childId of cultureChildren) {
            await this.toggleLayer(childId, false);
          }
          return;
        }

        // Hide layer (keep in memory for fast re-toggle)
        const layer = this._overlays.get(layerId);
        if (layer && this.map.hasLayer(layer)) {
          this.map.removeLayer(layer);
        }
      }
    }

    /**
     * Set opacity for a layer if supported.
     * @param {string} layerId
     * @param {number} opacity - 0.0 to 1.0
     */
    setLayerOpacity(layerId, opacity) {
      const layer = this._overlays.get(layerId);
      if (!layer) return;

      const def = root.HYLayerRegistry ? root.HYLayerRegistry.get(layerId) : null;
      const baseStyle = def ? def.style : {};

      if (typeof layer.setStyle === 'function') {
        layer.setStyle({
          fillOpacity: (baseStyle.fillOpacity !== undefined ? baseStyle.fillOpacity : 0.25) * opacity,
          opacity: (baseStyle.strokeOpacity !== undefined ? baseStyle.strokeOpacity : 0.85) * opacity,
        });
      } else if (typeof layer.setOpacity === 'function') {
        layer.setOpacity(opacity);
      }
    }

    /* ── Visibility Control ────────────────────────── */

    /** Show the Leaflet map container */
    show() {
      this.container.style.opacity = '1';
      this.container.style.pointerEvents = 'auto';
      this.container.style.zIndex = '1';
      setTimeout(() => this.map.invalidateSize(), 100);
    }

    /** Hide the Leaflet map container (for 3D transition) */
    hide() {
      this.container.style.opacity = '0';
      this.container.style.pointerEvents = 'none';
      this.container.style.zIndex = '0';
    }

    /**
     * Smoothly fade out.
     * @param {number} [durationMs=500]
     * @returns {Promise}
     */
    fadeOut(durationMs = 500) {
      return new Promise(resolve => {
        this.container.style.transition = `opacity ${durationMs}ms ease`;
        this.container.style.opacity = '0';
        setTimeout(() => {
          this.container.style.pointerEvents = 'none';
          this.container.style.zIndex = '0';
          resolve();
        }, durationMs);
      });
    }

    /**
     * Smoothly fade in.
     * @param {number} [durationMs=500]
     * @returns {Promise}
     */
    fadeIn(durationMs = 500) {
      return new Promise(resolve => {
        this.container.style.zIndex = '1';
        this.container.style.pointerEvents = 'auto';
        this.container.style.transition = `opacity ${durationMs}ms ease`;
        requestAnimationFrame(() => {
          this.container.style.opacity = '1';
        });
        setTimeout(() => {
          this.map.invalidateSize();
          resolve();
        }, durationMs);
      });
    }

    /* ── Utility ───────────────────────────────────── */

    /** @returns {{lat:number, lng:number}} */
    getCenter() {
      const c = this.map.getCenter();
      return { lat: c.lat, lng: c.lng };
    }

    /** @returns {number} */
    getZoom() {
      return this.map.getZoom();
    }

    /**
     * Fly to a location.
     * @param {number} lat
     * @param {number} lng
     * @param {number} [zoom]
     * @param {number} [durationSec=1.2]
     */
    flyTo(lat, lng, zoom, durationSec = 1.2) {
      this.map.flyTo([lat, lng], zoom || this.map.getZoom(), { duration: durationSec });
    }

    /** Invalidate map size (call after container resize) */
    invalidateSize() {
      this.map.invalidateSize();
    }
  }

  root.HYMapLeafletAdapter = MapLeafletAdapter;

})(window);
