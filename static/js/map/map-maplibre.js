/* ═══════════════════════════════════════════════════════════════════
   HiddenYatra — MapMaplibre (MapLibre GL JS Engine Adapter)
   Lazy-loaded 3D engine for terrain rendering.
   Only instantiated when user toggles "3D Terrain" mode.
   ═══════════════════════════════════════════════════════════════════ */

(function (root) {
  'use strict';

  /** MapLibre GL JS CDN URL (loaded dynamically) */
  const MAPLIBRE_JS_URL = 'https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js';
  const MAPLIBRE_CSS_URL = 'https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css';

  /** AWS Terrain Tiles (free, public dataset) */
  const TERRAIN_SOURCE = {
    type: 'raster-dem',
    tiles: ['https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png'],
    tileSize: 256,
    encoding: 'terrarium',
    maxzoom: 15,
  };

  /** Base style for MapLibre (minimal, matches CARTO light) */
  function buildMaplibreStyle(basemapId) {
    const tileSources = root.HYTileSources || {};
    const basemap = tileSources[basemapId] || tileSources['carto_light'];

    const tileUrl = basemap.url
      .replace('{r}', '')
      .replace('{s}', 'a'); // MapLibre doesn't use {s} subdomains the same way

    // For MapLibre, we need to expand subdomains manually
    const tileUrls = [];
    if (basemap.subdomains) {
      for (const s of basemap.subdomains) {
        tileUrls.push(basemap.url.replace('{s}', s).replace('{r}', ''));
      }
    } else {
      tileUrls.push(tileUrl);
    }

    return {
      version: 8,
      sources: {
        'basemap': {
          type: 'raster',
          tiles: tileUrls,
          tileSize: 256,
          attribution: basemap.attribution,
          maxzoom: basemap.maxZoom || 19,
        },
        'terrain-dem': TERRAIN_SOURCE,
      },
      layers: [
        {
          id: 'basemap-layer',
          type: 'raster',
          source: 'basemap',
        },
      ],
      terrain: {
        source: 'terrain-dem',
        exaggeration: 1.5,
      },
    };
  }

  class MapMaplibreAdapter {
    constructor() {
      /** @type {maplibregl.Map|null} */
      this.map = null;

      /** @type {HTMLElement|null} */
      this.container = null;

      /** @type {boolean} */
      this._loaded = false;

      /** @type {boolean} */
      this._terrainActive = false;

      /** @type {Map<string, string>} GeoJSON source IDs added */
      this._sources = new Map();
    }

    /* ── Initialization ────────────────────────────── */

    /**
     * Lazy-load MapLibre GL JS from CDN and initialize the map.
     * @param {HTMLElement} containerEl - The container div
     * @param {Object} [initialView] - { lat, lng, zoom, pitch, bearing }
     * @returns {Promise<maplibregl.Map>}
     */
    async init(containerEl, initialView) {
      this.container = containerEl;

      // Load MapLibre CSS
      if (!document.querySelector(`link[href="${MAPLIBRE_CSS_URL}"]`)) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = MAPLIBRE_CSS_URL;
        document.head.appendChild(link);
      }

      // Load MapLibre JS if not already loaded
      if (typeof maplibregl === 'undefined') {
        await this._loadScript(MAPLIBRE_JS_URL);
      }

      // Check WebGL support directly on canvas
      const testCanvas = document.createElement('canvas');
      const gl = testCanvas.getContext('webgl2') || testCanvas.getContext('webgl') || testCanvas.getContext('experimental-webgl');
      if (!gl) {
        const err = new Error('WebGL is not supported on this device');
        err.code = 'WEBGL_UNAVAILABLE';
        throw err;
      }
      console.log('[MapMaplibre] WebGL context verified:', gl instanceof (window.WebGL2RenderingContext || Object) ? 'WebGL 2' : 'WebGL 1');

      const view = initialView || (root.HYMapState ? root.HYMapState.getView() : {
        lat: 25.0961, lng: 85.3131, zoom: 8, pitch: 0, bearing: 0,
      });

      // Build the style
      const currentBasemap = root.HYMapState ?
        (root.HYMapState._currentBasemapId || 'carto_light') : 'carto_light';
      const style = buildMaplibreStyle(currentBasemap);

      // Create MapLibre instance
      try {
        this.map = new maplibregl.Map({
          container: containerEl,
          style: style,
          center: [view.lng, view.lat],
          zoom: view.zoom,
          pitch: view.pitch || 0,
          bearing: view.bearing || 0,
          maxPitch: 85,
          antialias: true,
        });
      } catch (mapErr) {
        mapErr.code = 'MAPLIBRE_INIT_FAILED';
        throw mapErr;
      }

      // Add navigation controls (zoom + compass)
      this.map.addControl(new maplibregl.NavigationControl({
        visualizePitch: true,
        showCompass: true,
        showZoom: true,
      }), 'bottom-right');

      // Wait for map to load with timeout safety
      await new Promise((resolve, reject) => {
        if (this.map.loaded()) {
          resolve();
          return;
        }

        const onLoad = () => {
          cleanup();
          resolve();
        };

        const onError = (e) => {
          if (e && e.error && e.error.message && e.error.message.includes('fatal')) {
            cleanup();
            reject(e.error);
          }
        };

        const timeout = setTimeout(() => {
          console.warn('[MapMaplibre] Map load event timeout (10s), proceeding with active style');
          cleanup();
          resolve();
        }, 10000);

        const cleanup = () => {
          clearTimeout(timeout);
          this.map.off('load', onLoad);
          this.map.off('error', onError);
        };

        this.map.on('load', onLoad);
        this.map.on('error', onError);
      });

      this._loaded = true;
      this._terrainActive = true;

      // Bind state synchronization
      this._bindStateSync();

      return this.map;
    }

    /** @private Load a script dynamically */
    _loadScript(url) {
      return new Promise((resolve, reject) => {
        // Check if already loaded
        if (document.querySelector(`script[src="${url}"]`)) {
          resolve();
          return;
        }
        const script = document.createElement('script');
        script.src = url;
        script.onload = resolve;
        script.onerror = () => {
          const err = new Error(`Failed to load 3D map engine from ${url}`);
          err.code = 'MAPLIBRE_SCRIPT_LOAD_FAILED';
          reject(err);
        };
        document.head.appendChild(script);
      });
    }

    /* ── State Synchronization ─────────────────────── */

    /** @private */
    _bindStateSync() {
      const state = root.HYMapState;
      if (!state || !this.map) return;

      // MapLibre → MapState
      this.map.on('moveend', () => {
        if (state.activeEngine !== 'maplibre') return;
        const center = this.map.getCenter();
        state.setView({
          lat: center.lat,
          lng: center.lng,
          zoom: this.map.getZoom(),
          pitch: this.map.getPitch(),
          bearing: this.map.getBearing(),
        }, 'maplibre');
      });

      // MapState → MapLibre
      state.on('view', (data) => {
        if (data.source === 'maplibre') return;
        if (state.activeEngine !== 'maplibre') return;
        if (!this.map) return;
        this.map.jumpTo({
          center: [data.state.lng, data.state.lat],
          zoom: data.state.zoom,
          pitch: data.state.pitch,
          bearing: data.state.bearing,
        });
      });
    }

    /* ── Terrain Control ───────────────────────────── */

    /**
     * Set terrain exaggeration factor.
     * @param {number} factor - 0 (flat) to 3 (extreme)
     */
    setTerrainExaggeration(factor) {
      if (!this.map || !this._loaded) return;
      this.map.setTerrain({
        source: 'terrain-dem',
        exaggeration: factor,
      });
    }

    /** Disable terrain (flat map in MapLibre) */
    disableTerrain() {
      if (!this.map || !this._loaded) return;
      this.map.setTerrain(null);
      this._terrainActive = false;
    }

    /** Enable terrain */
    enableTerrain(exaggeration = 1.5) {
      if (!this.map || !this._loaded) return;
      this.map.setTerrain({
        source: 'terrain-dem',
        exaggeration: exaggeration,
      });
      this._terrainActive = true;
    }

    /* ── GeoJSON Layer Management ──────────────────── */

    /**
     * Add a GeoJSON data layer.
     * @param {string} layerId
     * @param {Object} geojsonData
     * @param {Object} style
     */
    addGeoJSONLayer(layerId, geojsonData, style) {
      if (!this.map || !this._loaded) return;

      const sourceId = `source-${layerId}`;
      style = style || {};

      // Remove existing
      this.removeLayer(layerId);

      // Add source
      this.map.addSource(sourceId, {
        type: 'geojson',
        data: geojsonData,
      });

      // Check if dataset contains Points
      const hasPoints = geojsonData && geojsonData.features && geojsonData.features.some(f => f.geometry && f.geometry.type === 'Point');

      if (hasPoints || layerId === 'waterfalls_geo' || layerId === 'waterfalls') {
        this.map.addLayer({
          id: `${layerId}-circle`,
          type: 'circle',
          source: sourceId,
          paint: {
            'circle-radius': style.radius || 7,
            'circle-color': style.fillColor || style.color || '#06b6d4',
            'circle-stroke-width': 2,
            'circle-stroke-color': '#ffffff',
            'circle-opacity': style.fillOpacity !== undefined ? style.fillOpacity : 0.9,
          },
        });
      } else {
        // Add fill layer for polygons
        this.map.addLayer({
          id: `${layerId}-fill`,
          type: 'fill',
          source: sourceId,
          paint: {
            'fill-color': style.fillColor || '#6366f1',
            'fill-opacity': style.fillOpacity !== undefined ? style.fillOpacity : 0.06,
          },
        });

        // Add stroke layer
        this.map.addLayer({
          id: `${layerId}-line`,
          type: 'line',
          source: sourceId,
          paint: {
            'line-color': style.stroke || '#6366f1',
            'line-width': style.strokeWidth || 2,
            'line-opacity': style.strokeOpacity || 0.7,
          },
        });
      }

      this._sources.set(layerId, sourceId);
    }

    /**
     * Remove a layer by ID.
     * @param {string} layerId
     */
    removeLayer(layerId) {
      if (!this.map || !this._loaded) return;

      const fillId = `${layerId}-fill`;
      const lineId = `${layerId}-line`;
      const circleId = `${layerId}-circle`;
      const sourceId = `source-${layerId}`;

      if (this.map.getLayer(circleId)) this.map.removeLayer(circleId);
      if (this.map.getLayer(fillId)) this.map.removeLayer(fillId);
      if (this.map.getLayer(lineId)) this.map.removeLayer(lineId);
      if (this.map.getSource(sourceId)) this.map.removeSource(sourceId);

      this._sources.delete(layerId);
    }

    /**
     * Toggle layer visibility in 3D mode.
     * @param {string} layerId
     * @param {boolean} visible
     */
    async toggleLayer(layerId, visible) {
      if (!this.map || !this._loaded) return;

      const fillId = `${layerId}-fill`;
      const lineId = `${layerId}-line`;
      const circleId = `${layerId}-circle`;
      const sourceId = `source-${layerId}`;

      if (visible) {
        if (this.map.getSource(sourceId)) {
          if (this.map.getLayer(circleId)) this.map.setLayoutProperty(circleId, 'visibility', 'visible');
          if (this.map.getLayer(fillId)) this.map.setLayoutProperty(fillId, 'visibility', 'visible');
          if (this.map.getLayer(lineId)) this.map.setLayoutProperty(lineId, 'visibility', 'visible');
          return;
        }

        const def = root.HYLayerRegistry ? root.HYLayerRegistry.get(layerId) : null;
        if (!def) return;
        const isGeoJSON = (def.sourceType === 'geojson' || def.type === 'geojson');
        if (isGeoJSON && def.source) {
          const data = await root.HYLayerRegistry.fetchData(layerId);
          if (data) {
            this.addGeoJSONLayer(layerId, data, def.style);
          }
        }
      } else {
        if (this.map.getLayer(circleId)) this.map.setLayoutProperty(circleId, 'visibility', 'none');
        if (this.map.getLayer(fillId)) this.map.setLayoutProperty(fillId, 'visibility', 'none');
        if (this.map.getLayer(lineId)) this.map.setLayoutProperty(lineId, 'visibility', 'none');
      }
    }

    /**
     * Set opacity for a layer in MapLibre.
     * @param {string} layerId
     * @param {number} opacity - 0.0 to 1.0
     */
    setLayerOpacity(layerId, opacity) {
      if (!this.map || !this._loaded) return;

      const fillId = `${layerId}-fill`;
      const lineId = `${layerId}-line`;
      const circleId = `${layerId}-circle`;
      const def = root.HYLayerRegistry ? root.HYLayerRegistry.get(layerId) : null;
      const style = def ? def.style : {};

      if (this.map.getLayer(circleId)) {
        this.map.setPaintProperty(circleId, 'circle-opacity', (style.fillOpacity !== undefined ? style.fillOpacity : 0.9) * opacity);
      }
      if (this.map.getLayer(fillId)) {
        this.map.setPaintProperty(fillId, 'fill-opacity', (style.fillOpacity !== undefined ? style.fillOpacity : 0.25) * opacity);
      }
      if (this.map.getLayer(lineId)) {
        this.map.setPaintProperty(lineId, 'line-opacity', (style.strokeOpacity !== undefined ? style.strokeOpacity : 0.85) * opacity);
      }
    }

    /* ── Marker Placement ──────────────────────────── */

    /**
     * Add markers for tourist places.
     * @param {Array} places - Array of place objects with lat/lng
     */
    addPlaceMarkers(places) {
      if (!this.map || !this._loaded) return;

      const CATEGORY_COLORS = {
        temple: '#f59e0b', waterfall: '#06b6d4', nature: '#10b981',
        historical: '#8b5cf6', fort: '#d97706', religious: '#f97316',
        hidden_gem: '#ec4899', tourist_spot: '#6366f1', park: '#22c55e',
        lake: '#0284c7', cultural: '#8b5cf6', mountain: '#6366f1',
        museum: '#d97706', default: '#6366f1',
      };

      const CATEGORY_EMOJI = {
        temple: '🛕', waterfall: '💧', nature: '🌿', historical: '🏛️',
        fort: '🏰', religious: '🙏', hidden_gem: '💎', tourist_spot: '📍',
        park: '🌳', lake: '🌊', cultural: '🎭', mountain: '⛰️',
        museum: '🏛️', default: '📍',
      };

      places.forEach(p => {
        const lat = parseFloat(p.latitude);
        const lng = parseFloat(p.longitude);
        if (isNaN(lat) || isNaN(lng)) return;

        const color = CATEGORY_COLORS[p.category] || CATEGORY_COLORS.default;
        const emoji = CATEGORY_EMOJI[p.category] || CATEGORY_EMOJI.default;

        // Create marker element
        const el = document.createElement('div');
        el.className = 'hy-3d-marker';
        el.style.cssText = `
          width: 32px; height: 32px; border-radius: 50%;
          background: ${color}; border: 2px solid white;
          box-shadow: 0 4px 12px rgba(0,0,0,0.5);
          display: flex; align-items: center; justify-content: center;
          font-size: 14px; cursor: pointer;
          transition: transform 0.2s;
        `;
        el.textContent = emoji;
        el.title = p.name;

        el.addEventListener('mouseenter', () => { el.style.transform = 'scale(1.3)'; });
        el.addEventListener('mouseleave', () => { el.style.transform = 'scale(1)'; });

        // Add popup
        const popup = new maplibregl.Popup({
          offset: 16,
          closeButton: true,
          maxWidth: '280px',
          className: 'hy-3d-popup',
        }).setHTML(`
          <div style="font-family:var(--font-body,'Inter',sans-serif);padding:4px;">
            <strong style="font-size:0.95rem;">${this._escHtml(p.name)}</strong><br>
            <span style="color:#64748b;font-size:0.8rem;">📍 ${this._escHtml(p.district_name || p.state_name || '')}</span><br>
            <span style="color:#f59e0b;font-weight:700;font-size:0.8rem;">★ ${p.avg_rating || 4.5}</span>
            <div style="margin-top:8px;">
              <a href="/place/${encodeURIComponent(p.slug)}" style="color:#FF7A18;font-weight:600;font-size:0.82rem;text-decoration:none;">View Details →</a>
            </div>
          </div>
        `);

        new maplibregl.Marker({ element: el })
          .setLngLat([lng, lat])
          .setPopup(popup)
          .addTo(this.map);
      });
    }

    /** @private Escape HTML */
    _escHtml(str) {
      if (!str) return '';
      return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;')
        .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    /* ── Camera Animation ──────────────────────────── */

    /**
     * Smoothly pitch up to reveal terrain.
     * @param {number} [targetPitch=50]
     * @param {number} [durationMs=1500]
     * @returns {Promise}
     */
    animatePitchIn(targetPitch = 50, durationMs = 1500) {
      return new Promise(resolve => {
        if (!this.map) { resolve(); return; }
        this.map.easeTo({
          pitch: targetPitch,
          bearing: -15,
          duration: durationMs,
          easing: t => 1 - Math.pow(1 - t, 3), // ease-out cubic
        });
        setTimeout(resolve, durationMs);
      });
    }

    /**
     * Smoothly pitch down to flat view (for transition back to 2D).
     * @param {number} [durationMs=800]
     * @returns {Promise}
     */
    animatePitchOut(durationMs = 800) {
      return new Promise(resolve => {
        if (!this.map) { resolve(); return; }
        this.map.easeTo({
          pitch: 0,
          bearing: 0,
          duration: durationMs,
        });
        setTimeout(resolve, durationMs);
      });
    }

    /* ── Visibility Control ────────────────────────── */

    show() {
      if (this.container) {
        this.container.style.opacity = '1';
        this.container.style.pointerEvents = 'auto';
        this.container.style.zIndex = '2';
      }
      if (this.map) this.map.resize();
    }

    hide() {
      if (this.container) {
        this.container.style.opacity = '0';
        this.container.style.pointerEvents = 'none';
        this.container.style.zIndex = '0';
      }
    }

    fadeIn(durationMs = 500) {
      return new Promise(resolve => {
        if (!this.container) { resolve(); return; }
        this.container.style.zIndex = '2';
        this.container.style.pointerEvents = 'auto';
        this.container.style.transition = `opacity ${durationMs}ms ease`;
        requestAnimationFrame(() => {
          this.container.style.opacity = '1';
        });
        setTimeout(() => {
          if (this.map) this.map.resize();
          resolve();
        }, durationMs);
      });
    }

    fadeOut(durationMs = 500) {
      return new Promise(resolve => {
        if (!this.container) { resolve(); return; }
        this.container.style.transition = `opacity ${durationMs}ms ease`;
        this.container.style.opacity = '0';
        setTimeout(() => {
          this.container.style.pointerEvents = 'none';
          this.container.style.zIndex = '0';
          resolve();
        }, durationMs);
      });
    }

    /* ── Cleanup ───────────────────────────────────── */

    /**
     * Destroy the MapLibre instance and free GPU memory.
     */
    destroy() {
      if (this.map) {
        this.map.remove();
        this.map = null;
      }
      this._loaded = false;
      this._terrainActive = false;
      this._sources.clear();
    }

    /** @returns {boolean} */
    isLoaded() {
      return this._loaded && this.map !== null;
    }
  }

  root.HYMapMaplibreAdapter = MapMaplibreAdapter;

})(window);
