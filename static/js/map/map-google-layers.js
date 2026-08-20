/* ═══════════════════════════════════════════════════════════════════
   HiddenYatra — Google Custom Geographic Layers Manager (Phase G3)
   Manages vector polygon and line overlay layers on Google Maps:
   - State & District boundaries
   - Block boundaries (with zoom gating minZoom: 10 & lazy loading)
   - Rivers networks
   - Lakes, reservoirs & dams
   - Forests & wildlife sanctuaries

   Uses dedicated google.maps.Data instances per layer with
   in-memory caching, request deduplication, and shared InfoWindows.
   ═══════════════════════════════════════════════════════════════════ */

(function (root) {
  'use strict';

  // Helper: Escape HTML to prevent XSS injection
  function escHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  /* ── Vector Layer Style Specifications ─────────── */
  const LAYER_STYLES = {
    state_boundary: {
      strokeColor: '#f59e0b',
      strokeWeight: 3.0,
      strokeOpacity: 0.90,
      fillOpacity: 0.0,
      zIndex: 10,
      hoverStrokeColor: '#fbbf24',
      hoverStrokeWeight: 4.5,
    },
    district_boundaries: {
      strokeColor: '#6366f1',
      strokeWeight: 2.0,
      strokeOpacity: 0.75,
      fillColor: '#6366f1',
      fillOpacity: 0.06,
      hoverStrokeColor: '#818cf8',
      hoverStrokeWeight: 3.2,
      hoverFillOpacity: 0.18,
      zIndex: 20,
    },
    block_boundaries: {
      strokeColor: '#94a3b8',
      strokeWeight: 1.0,
      strokeOpacity: 0.45,
      fillColor: '#94a3b8',
      fillOpacity: 0.02,
      hoverStrokeColor: '#f59e0b',
      hoverStrokeWeight: 2.4,
      hoverFillOpacity: 0.14,
      zIndex: 30,
      minZoom: 10,
    },
    rivers: {
      strokeColor: '#0284c7',
      strokeWeight: 2.5,
      strokeOpacity: 0.85,
      hoverStrokeColor: '#38bdf8',
      hoverStrokeWeight: 4.8,
      hoverStrokeOpacity: 1.0,
      zIndex: 40,
    },
    lakes_dams: {
      strokeColor: '#0891b2',
      strokeWeight: 1.8,
      strokeOpacity: 0.90,
      fillColor: '#06b6d4',
      fillOpacity: 0.35,
      hoverStrokeColor: '#22d3ee',
      hoverStrokeWeight: 2.6,
      hoverFillOpacity: 0.55,
      zIndex: 50,
    },
    forests: {
      strokeColor: '#166534',
      strokeWeight: 1.8,
      strokeOpacity: 0.85,
      fillColor: '#15803d',
      fillOpacity: 0.28,
      hoverStrokeColor: '#22c55e',
      hoverStrokeWeight: 2.6,
      hoverFillOpacity: 0.45,
      zIndex: 60,
    },
  };

  class GoogleGeoLayerManager {
    /**
     * @param {google.maps.Map} googleMap
     * @param {Object} [options]
     * @param {google.maps.InfoWindow} [options.infoWindow]
     */
    constructor(googleMap, options = {}) {
      if (!googleMap) throw new Error('[HYGoogleGeoLayerManager] Missing Google Map instance');

      /** @type {google.maps.Map} */
      this.map = googleMap;

      /** @type {google.maps.InfoWindow|null} Shared InfoWindow reference */
      this._infoWindow = options.infoWindow || null;

      /** @type {Map<string, Object>} Layer records (layerId -> layer state object) */
      this._layers = new Map();

      /** @type {Map<string, Object>} In-memory parsed GeoJSON cache (url -> FeatureCollection) */
      this._dataCache = new Map();

      /** @type {Map<string, Promise>} In-flight network request deduplication */
      this._inflightRequests = new Map();

      /** @type {number} Current map zoom level */
      this._currentZoom = googleMap.getZoom() || 8;

      /** @type {google.maps.MapsEventListener|null} */
      this._zoomListener = null;

      this._initZoomWatcher();
    }

    /* ── Zoom Gating Watcher ───────────────────────── */

    /** @private */
    _initZoomWatcher() {
      this._zoomListener = this.map.addListener('zoom_changed', () => {
        const newZoom = this.map.getZoom();
        if (newZoom !== this._currentZoom) {
          this._currentZoom = newZoom;
          this._applyZoomGating();
        }
      });
    }

    /**
     * Apply zoom gating to layers with minZoom constraints (e.g. block_boundaries).
     * Does NOT mutate the user's toggle state in HYMapState.
     * @private
     */
    _applyZoomGating() {
      this._layers.forEach((layerObj, layerId) => {
        if (!layerObj.dataLayer) return;
        const minZoom = layerObj.minZoom || (LAYER_STYLES[layerId] && LAYER_STYLES[layerId].minZoom);

        if (minZoom !== undefined) {
          if (this._currentZoom < minZoom) {
            // Below minZoom: hide from map canvas
            layerObj.dataLayer.setMap(null);
          } else if (layerObj.visible) {
            // Above/at minZoom & user has enabled layer: restore to map canvas
            layerObj.dataLayer.setMap(this.map);
          }
        }
      });
    }

    /* ── Shared InfoWindow Helper ──────────────────── */

    /**
     * Set or get the shared InfoWindow instance.
     * @param {google.maps.InfoWindow} [infoWindow]
     * @returns {google.maps.InfoWindow}
     */
    getInfoWindow(infoWindow) {
      if (infoWindow) {
        this._infoWindow = infoWindow;
      }
      if (!this._infoWindow && typeof google !== 'undefined' && google.maps && google.maps.InfoWindow) {
        this._infoWindow = new google.maps.InfoWindow({
          maxWidth: 320,
          minWidth: 220,
        });
      }
      return this._infoWindow;
    }

    /* ── Data Fetching & Caching ───────────────────── */

    /**
     * Fetch GeoJSON data with in-memory caching and request deduplication.
     * @param {string} layerId
     * @param {string} sourceUrl
     * @returns {Promise<Object|null>}
     */
    async fetchGeoJson(layerId, sourceUrl) {
      if (!sourceUrl) return null;

      // 1. Check in-memory cache
      if (this._dataCache.has(sourceUrl)) {
        return this._dataCache.get(sourceUrl);
      }

      // 2. Check if HYLayerRegistry already cached it
      if (root.HYLayerRegistry && typeof root.HYLayerRegistry.fetchData === 'function') {
        try {
          const cached = await root.HYLayerRegistry.fetchData(layerId);
          if (cached) {
            this._dataCache.set(sourceUrl, cached);
            return cached;
          }
        } catch (e) {
          // fallback to direct fetch below
        }
      }

      // 3. Check in-flight request deduplication
      if (this._inflightRequests.has(sourceUrl)) {
        return this._inflightRequests.get(sourceUrl);
      }

      // 4. Perform fresh fetch
      const fetchPromise = (async () => {
        try {
          const response = await fetch(sourceUrl);
          if (!response.ok) {
            throw new Error(`HTTP error ${response.status} fetching ${sourceUrl}`);
          }
          const data = await response.json();
          this._dataCache.set(sourceUrl, data);
          return data;
        } catch (err) {
          console.error(`[HYGoogleGeoLayerManager] Failed to load GeoJSON for ${layerId}:`, err);
          return null;
        } finally {
          this._inflightRequests.delete(sourceUrl);
        }
      })();

      this._inflightRequests.set(sourceUrl, fetchPromise);
      return fetchPromise;
    }

    /* ── Layer Lifecycle ───────────────────────────── */

    /**
     * Load and instantiate a geographic vector layer.
     * @param {string} layerId
     * @returns {Promise<google.maps.Data|null>}
     */
    async loadLayer(layerId) {
      // Return existing layer if already created
      if (this._layers.has(layerId)) {
        const existing = this._layers.get(layerId);
        return existing.dataLayer;
      }

      const def = root.HYLayerRegistry ? root.HYLayerRegistry.get(layerId) : null;
      let sourceUrl = def ? def.source : null;

      // Handle state_boundary fallback to districts.geojson if not explicitly set
      if (layerId === 'state_boundary' && !sourceUrl) {
        sourceUrl = '/static/data/bihar/districts.geojson';
      }

      if (!sourceUrl) {
        console.warn(`[HYGoogleGeoLayerManager] No source URL for layer: ${layerId}`);
        return null;
      }

      const geojsonData = await this.fetchGeoJson(layerId, sourceUrl);
      if (!geojsonData) return null;

      // Create dedicated google.maps.Data instance
      const dataLayer = new google.maps.Data();

      // Configure layer state object
      const baseStyle = LAYER_STYLES[layerId] || (def ? def.style : {}) || {};
      const minZoom = baseStyle.minZoom || (def ? def.minZoom : undefined);
      const opacity = (def && def.opacity !== undefined) ? def.opacity : 0.85;

      const layerRecord = {
        id: layerId,
        dataLayer: dataLayer,
        def: def,
        sourceUrl: sourceUrl,
        visible: true,
        opacity: opacity,
        baseStyle: baseStyle,
        minZoom: minZoom,
        interactive: def ? (def.interactive !== false) : true,
      };

      this._layers.set(layerId, layerRecord);

      // Ingest GeoJSON features
      try {
        dataLayer.addGeoJson(geojsonData);
      } catch (err) {
        console.error(`[HYGoogleGeoLayerManager] Error ingesting GeoJSON for ${layerId}:`, err);
        return null;
      }

      // Apply dynamic styling with opacity multiplier
      this._applyLayerStyle(layerId);

      // Attach event listeners (hover highlight and click InfoWindow)
      this._bindLayerEvents(layerId, dataLayer, layerRecord);

      // Attach to map if within zoom constraints
      const currentZoom = this.map.getZoom() || 8;
      if (minZoom === undefined || currentZoom >= minZoom) {
        dataLayer.setMap(this.map);
      }

      console.log(`[HYGoogleGeoLayerManager] Loaded geographic layer: ${layerId}`);
      return dataLayer;
    }

    /**
     * Toggle visibility of a geographic layer.
     * @param {string} layerId
     * @param {boolean} visible
     */
    async toggleLayer(layerId, visible) {
      if (visible) {
        let layerRecord = this._layers.get(layerId);
        if (!layerRecord) {
          // Lazy load on first activation
          await this.loadLayer(layerId);
          layerRecord = this._layers.get(layerId);
        }

        if (layerRecord) {
          layerRecord.visible = true;
          const minZoom = layerRecord.minZoom;
          const currentZoom = this.map.getZoom() || 8;

          if (minZoom === undefined || currentZoom >= minZoom) {
            layerRecord.dataLayer.setMap(this.map);
          }
        }
      } else {
        const layerRecord = this._layers.get(layerId);
        if (layerRecord) {
          layerRecord.visible = false;
          layerRecord.dataLayer.setMap(null);
        }
      }
    }

    /**
     * Set opacity for a geographic layer.
     * @param {string} layerId
     * @param {number} opacity - 0.0 to 1.0
     */
    setLayerOpacity(layerId, opacity) {
      const layerRecord = this._layers.get(layerId);
      if (!layerRecord) return;

      layerRecord.opacity = Math.max(0, Math.min(1, opacity));
      this._applyLayerStyle(layerId);
    }

    /**
     * Apply declarative style function to a Data layer.
     * Multiplies base style opacities by layer opacity.
     * @private
     * @param {string} layerId
     */
    _applyLayerStyle(layerId) {
      const layerRecord = this._layers.get(layerId);
      if (!layerRecord || !layerRecord.dataLayer) return;

      const baseStyle = layerRecord.baseStyle || {};
      const layerOpacity = layerRecord.opacity !== undefined ? layerRecord.opacity : 1.0;

      layerRecord.dataLayer.setStyle((feature) => {
        const geomType = feature.getGeometry().getType();
        const isLine = geomType === 'LineString' || geomType === 'MultiLineString';

        const strokeColor = baseStyle.strokeColor || baseStyle.stroke || '#6366f1';
        const strokeWeight = baseStyle.strokeWeight || baseStyle.strokeWidth || 2;
        const strokeOpacity = (baseStyle.strokeOpacity !== undefined ? baseStyle.strokeOpacity : 0.85) * layerOpacity;

        const fillColor = baseStyle.fillColor || strokeColor;
        const fillOpacity = isLine ? 0 : ((baseStyle.fillOpacity !== undefined ? baseStyle.fillOpacity : 0.25) * layerOpacity);
        const zIndex = baseStyle.zIndex || 20;

        return {
          strokeColor: strokeColor,
          strokeWeight: strokeWeight,
          strokeOpacity: strokeOpacity,
          fillColor: fillColor,
          fillOpacity: fillOpacity,
          zIndex: zIndex,
        };
      });
    }

    /* ── Event Binding ─────────────────────────────── */

    /**
     * Bind hover and click events on a Data layer.
     * @private
     * @param {string} layerId
     * @param {google.maps.Data} dataLayer
     * @param {Object} layerRecord
     */
    _bindLayerEvents(layerId, dataLayer, layerRecord) {
      const baseStyle = layerRecord.baseStyle || {};

      // 1. Mouseover — hover highlight
      dataLayer.addListener('mouseover', (event) => {
        const geomType = event.feature.getGeometry().getType();
        const isLine = geomType === 'LineString' || geomType === 'MultiLineString';

        const hoverStroke = baseStyle.hoverStrokeColor || baseStyle.hoverStroke || '#38bdf8';
        const hoverWeight = (baseStyle.hoverStrokeWeight || baseStyle.strokeWeight || 2) + (isLine ? 1.5 : 1);
        const hoverFillOpacity = Math.min(1.0, (baseStyle.hoverFillOpacity || 0.40) * layerRecord.opacity);

        if (isLine) {
          dataLayer.overrideStyle(event.feature, {
            strokeColor: hoverStroke,
            strokeWeight: hoverWeight,
            strokeOpacity: 1.0,
            zIndex: 99,
          });
        } else {
          dataLayer.overrideStyle(event.feature, {
            strokeColor: hoverStroke,
            strokeWeight: hoverWeight,
            fillOpacity: hoverFillOpacity,
            zIndex: 99,
          });
        }
      });

      // 2. Mouseout — revert highlight
      dataLayer.addListener('mouseout', (event) => {
        dataLayer.revertStyle(event.feature);
      });

      // 3. Click — zoom to bounds and open shared InfoWindow
      if (layerRecord.interactive) {
        dataLayer.addListener('click', (event) => {
          this._handleFeatureClick(layerId, event);
        });
      }
    }

    /**
     * Handle feature click event.
     * @private
     * @param {string} layerId
     * @param {google.maps.Data.MouseEvent} event
     */
    _handleFeatureClick(layerId, event) {
      const feature = event.feature;
      const geom = feature.getGeometry();
      const geomType = geom.getType();

      // Pan or Fit Bounds smoothly
      if (geomType === 'Point') {
        const latLng = geom.get();
        this.map.panTo(latLng);
      } else {
        const bounds = new google.maps.LatLngBounds();
        geom.forEachLatLng((latLng) => bounds.extend(latLng));
        if (!bounds.isEmpty()) {
          this.map.fitBounds(bounds, { top: 50, right: 50, bottom: 50, left: 50 });
        }
      }

      // Extract properties safely
      const props = {};
      feature.forEachProperty((val, key) => { props[key] = val; });

      // Build Safe HTML Content
      const contentHTML = this.buildFeaturePopupHTML(layerId, props);

      // Open Shared InfoWindow
      const infoWindow = this.getInfoWindow();
      if (infoWindow) {
        infoWindow.setContent(contentHTML);
        infoWindow.setPosition(event.latLng);
        infoWindow.open({
          map: this.map,
          shouldFocus: false,
        });
      }

      // Notify HYMapState
      if (root.HYMapState) {
        root.HYMapState._notify('layer', {
          layerId: layerId,
          event: 'feature-click',
          feature: { properties: props },
        });
      }
    }

    /* ── Safe Popup HTML Builders ──────────────────── */

    /**
     * Build rich, sanitized HTML for a feature click popup.
     * @param {string} layerId
     * @param {Object} props
     * @returns {string}
     */
    buildFeaturePopupHTML(layerId, props) {
      if (layerId === 'district_boundaries') {
        return this._buildDistrictPopup(props);
      }
      if (layerId === 'block_boundaries') {
        return this._buildBlockPopup(props);
      }
      if (layerId === 'rivers') {
        return this._buildRiverPopup(props);
      }
      if (layerId === 'lakes_dams') {
        return this._buildLakeDamPopup(props);
      }
      if (layerId === 'forests') {
        return this._buildForestPopup(props);
      }
      if (layerId === 'state_boundary') {
        return this._buildStatePopup(props);
      }

      const name = props.name || props.NAME || props.title || 'Geographic Feature';
      return `<div style="padding:4px 6px;font-family:system-ui,sans-serif;"><strong>${escHtml(name)}</strong></div>`;
    }

    /** @private */
    _buildDistrictPopup(props) {
      const name = props.name || 'District';
      const state = props.state || 'Bihar';
      const hqLat = props.hq_lat ? parseFloat(props.hq_lat).toFixed(4) : null;
      const hqLng = props.hq_lng ? parseFloat(props.hq_lng).toFixed(4) : null;

      return `
        <div style="font-family:system-ui,-apple-system,sans-serif;padding:6px 8px;max-width:260px;">
          <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
            <span style="font-size:14px;">📍</span>
            <strong style="font-size:14px;color:#0f172a;">${escHtml(name)}</strong>
          </div>
          <div style="font-size:12px;color:#64748b;margin-bottom:6px;">
            State: <strong>${escHtml(state)}</strong>
          </div>
          ${hqLat && hqLng ? `
            <div style="font-size:11px;color:#94a3b8;margin-bottom:8px;">
              HQ: ${hqLat}°N, ${hqLng}°E
            </div>
          ` : ''}
          <div style="border-top:1px solid #e2e8f0;padding-top:6px;margin-top:6px;font-size:10px;color:#94a3b8;">
            Source: Census of India / DataMeet (ODbL)
          </div>
        </div>
      `;
    }

    /** @private */
    _buildBlockPopup(props) {
      const name = props.name || 'Block';
      const districtName = props.district_name || 'Bihar';
      const censusCode = props.census_code || null;
      const lgdCode = props.lgd_code || null;
      const districtSlug = props.district_slug || '';
      const blockSlug = props.slug || '';

      // Check if block has a valid linkable destination slug
      const isSeeded = Boolean(districtSlug && blockSlug);

      return `
        <div style="font-family:system-ui,-apple-system,sans-serif;padding:6px 8px;max-width:260px;">
          <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
            <span style="font-size:14px;">🔲</span>
            <strong style="font-size:14px;color:#0f172a;">${escHtml(name)} Block</strong>
          </div>
          <div style="font-size:12px;color:#64748b;margin-bottom:6px;">
            District: <strong>${escHtml(districtName)}</strong>
          </div>
          ${censusCode || lgdCode ? `
            <div style="font-size:11px;color:#94a3b8;margin-bottom:8px;line-height:1.4;">
              ${censusCode ? `Census Code: <strong>${escHtml(censusCode)}</strong><br>` : ''}
              ${lgdCode ? `LGD Code: <strong>${escHtml(lgdCode)}</strong>` : ''}
            </div>
          ` : ''}
          ${isSeeded ? `
            <a href="/state/bihar/${encodeURIComponent(districtSlug)}/${encodeURIComponent(blockSlug)}"
               style="display:inline-block;background:#6366f1;color:#ffffff;text-decoration:none;font-size:11px;font-weight:600;padding:4px 10px;border-radius:4px;margin-top:4px;">
              Explore ${escHtml(name)} →
            </a>
          ` : ''}
          <div style="border-top:1px solid #e2e8f0;padding-top:6px;margin-top:6px;font-size:10px;color:#94a3b8;">
            Source: Survey of India / Census 2011 (MIT)
          </div>
        </div>
      `;
    }

    /** @private */
    _buildRiverPopup(props) {
      const name = props.name || props.name_en || 'River';
      const nameHi = props.name_hi || null;
      const waterway = props.waterway || 'river';
      const sourceUrl = props.source_url || 'https://www.openstreetmap.org';

      return `
        <div style="font-family:system-ui,-apple-system,sans-serif;padding:6px 8px;max-width:260px;">
          <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
            <span style="font-size:14px;">🌊</span>
            <strong style="font-size:14px;color:#0284c7;">${escHtml(name)}</strong>
            ${nameHi ? `<span style="font-size:12px;color:#64748b;">(${escHtml(nameHi)})</span>` : ''}
          </div>
          <div style="font-size:12px;color:#64748b;margin-bottom:6px;">
            Type: <strong>${escHtml(waterway)}</strong>
          </div>
          <div style="border-top:1px solid #e2e8f0;padding-top:6px;margin-top:6px;font-size:10px;color:#94a3b8;">
            Source: <a href="${escHtml(sourceUrl)}" target="_blank" rel="noopener" style="color:#0284c7;text-decoration:none;">OpenStreetMap (ODbL)</a>
          </div>
        </div>
      `;
    }

    /** @private */
    _buildLakeDamPopup(props) {
      const name = props.name || props.name_en || 'Water Body';
      const nameHi = props.name_hi || null;
      const waterType = props.natural || props.water || props.landuse || 'Lake / Reservoir';

      return `
        <div style="font-family:system-ui,-apple-system,sans-serif;padding:6px 8px;max-width:260px;">
          <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
            <span style="font-size:14px;">💧</span>
            <strong style="font-size:14px;color:#0891b2;">${escHtml(name)}</strong>
            ${nameHi ? `<span style="font-size:12px;color:#64748b;">(${escHtml(nameHi)})</span>` : ''}
          </div>
          <div style="font-size:12px;color:#64748b;margin-bottom:6px;">
            Classification: <strong>${escHtml(waterType)}</strong>
          </div>
          <div style="border-top:1px solid #e2e8f0;padding-top:6px;margin-top:6px;font-size:10px;color:#94a3b8;">
            Source: OpenStreetMap contributors (ODbL)
          </div>
        </div>
      `;
    }

    /** @private */
    _buildForestPopup(props) {
      const name = props.name || props.name_en || 'Forest Area';
      const nameHi = props.name_hi || null;
      const type = props.type || props.boundary || props.leisure || 'Protected Forest';
      const protectClass = props.protect_class ? `IUCN Category ${escHtml(props.protect_class)}` : null;

      return `
        <div style="font-family:system-ui,-apple-system,sans-serif;padding:6px 8px;max-width:260px;">
          <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
            <span style="font-size:14px;">🌲</span>
            <strong style="font-size:14px;color:#166534;">${escHtml(name)}</strong>
            ${nameHi ? `<span style="font-size:12px;color:#64748b;">(${escHtml(nameHi)})</span>` : ''}
          </div>
          <div style="font-size:12px;color:#64748b;margin-bottom:4px;">
            Type: <strong>${escHtml(type)}</strong>
          </div>
          ${protectClass ? `
            <div style="font-size:11px;color:#15803d;margin-bottom:6px;">
              Protection: <strong>${protectClass}</strong>
            </div>
          ` : ''}
          <div style="border-top:1px solid #e2e8f0;padding-top:6px;margin-top:6px;font-size:10px;color:#94a3b8;">
            Source: OpenStreetMap & Forest Survey of India (ODbL)
          </div>
        </div>
      `;
    }

    /** @private */
    _buildStatePopup(props) {
      return `
        <div style="font-family:system-ui,-apple-system,sans-serif;padding:6px 8px;max-width:260px;">
          <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
            <span style="font-size:14px;">🗺️</span>
            <strong style="font-size:14px;color:#f59e0b;">State of Bihar</strong>
          </div>
          <div style="font-size:12px;color:#64748b;margin-bottom:4px;">
            Capital: <strong>Patna</strong> | 38 Districts | 534 Blocks
          </div>
          <div style="border-top:1px solid #e2e8f0;padding-top:6px;margin-top:6px;font-size:10px;color:#94a3b8;">
            Source: Survey of India / Census 2011
          </div>
        </div>
      `;
    }

    /* ── Cleanup ───────────────────────────────────── */

    /**
     * Destroy all managed layers and event listeners.
     */
    destroy() {
      if (this._zoomListener) {
        google.maps.event.removeListener(this._zoomListener);
        this._zoomListener = null;
      }

      this._layers.forEach((layerObj) => {
        if (layerObj.dataLayer) {
          layerObj.dataLayer.setMap(null);
        }
      });
      this._layers.clear();
      this._dataCache.clear();
      this._inflightRequests.clear();
      this._infoWindow = null;
    }
  }

  root.HYGoogleGeoLayerManager = GoogleGeoLayerManager;

})(window);
