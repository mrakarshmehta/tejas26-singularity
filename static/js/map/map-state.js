/* ═══════════════════════════════════════════════════════════════════
   HiddenYatra — MapState (Shared State Manager)
   Synchronizes center/zoom/pitch/bearing between Leaflet & MapLibre
   ═══════════════════════════════════════════════════════════════════ */

(function (root) {
  'use strict';

  /**
   * @typedef {Object} MapViewState
   * @property {number} lat
   * @property {number} lng
   * @property {number} zoom
   * @property {number} pitch     - 0 in 2D, 0–85 in 3D
   * @property {number} bearing   - rotation in degrees (0 = north)
   */

  /**
   * Reactive shared state for the HiddenYatra map system.
   * Both Leaflet and MapLibre adapters read/write from this,
   * so switching engines preserves the exact viewport.
   */
  class MapState {
    constructor() {
      // View state
      this.lat = 25.0961;       // Bihar center
      this.lng = 85.3131;
      this.zoom = 8;
      this.pitch = 0;
      this.bearing = 0;

      // Engine state
      this.mode = '2d';          // '2d' | '3d'
      this.activeEngine = 'leaflet'; // 'leaflet' | 'maplibre'

      // Map visual mode (basemap style)
      this.mapMode = 'normal';   // 'normal'|'dark'|'terrain'|'terrain3d'|'satellite'|'hybrid'

      // Layer visibility state (layer-id → boolean)
      this._layers = {};

      // Layer opacity state (layer-id → number 0.0 - 1.0)
      this._layerOpacities = {};

      // Selected place
      this.selectedPlaceId = null;
      this.activeDistrict = null;

      // User location
      this.userLat = null;
      this.userLng = null;

      // Subscribers for state changes
      this._subscribers = {
        view: [],
        mode: [],
        mapmode: [],
        layer: [],
        'layer:opacity': [],
        'layers:reset': [],
        'layers:bulk': [],
        select: [],
      };

      // Debounce timer for high-frequency view updates
      this._viewDebounce = null;
    }

    /* ── View State Management ─────────────────────── */

    /**
     * Update the view state and notify subscribers.
     * @param {Partial<MapViewState>} state
     * @param {string} [source] - Which engine triggered this ('leaflet' | 'maplibre' | 'user')
     */
    setView(state, source) {
      let changed = false;
      if (state.lat !== undefined && state.lat !== this.lat) { this.lat = state.lat; changed = true; }
      if (state.lng !== undefined && state.lng !== this.lng) { this.lng = state.lng; changed = true; }
      if (state.zoom !== undefined && state.zoom !== this.zoom) { this.zoom = state.zoom; changed = true; }
      if (state.pitch !== undefined && state.pitch !== this.pitch) { this.pitch = state.pitch; changed = true; }
      if (state.bearing !== undefined && state.bearing !== this.bearing) { this.bearing = state.bearing; changed = true; }

      if (changed) {
        // Debounce rapid view changes (drag/zoom)
        clearTimeout(this._viewDebounce);
        this._viewDebounce = setTimeout(() => {
          this._notify('view', { source, state: this.getView() });
        }, 16); // ~60fps cap
      }
    }

    /** @returns {MapViewState} */
    getView() {
      return {
        lat: this.lat,
        lng: this.lng,
        zoom: this.zoom,
        pitch: this.pitch,
        bearing: this.bearing,
      };
    }

    /* ── Mode Management ───────────────────────────── */

    /**
     * Switch between 2D and 3D mode.
     * @param {'2d'|'3d'} mode
     */
    setMode(mode) {
      if (mode === this.mode) return;
      const prev = this.mode;
      this.mode = mode;
      this.activeEngine = mode === '3d' ? 'maplibre' : 'leaflet';
      this._notify('mode', { from: prev, to: mode });
    }

    /** @returns {boolean} */
    is3D() {
      return this.mode === '3d';
    }

    /* ── Map Mode (Visual Style) ───────────────────── */

    /**
     * Set the visual map mode (basemap style).
     * @param {string} modeId - 'normal'|'dark'|'terrain'|'terrain3d'|'satellite'|'hybrid'
     */
    setMapMode(modeId) {
      if (modeId === this.mapMode) return;
      const prev = this.mapMode;
      this.mapMode = modeId;
      this._notify('mapmode', { from: prev, to: modeId });
    }

    /** @returns {string} Current map mode ID */
    getMapMode() {
      return this.mapMode;
    }

    /* ── Layer State ───────────────────────────────── */

    /**
     * Set layer visibility with automatic hierarchical parent/child propagation.
     * @param {string} layerId
     * @param {boolean} visible
     * @param {boolean} [silent=false] - Whether to suppress event emission
     */
    setLayerVisible(layerId, visible, silent = false) {
      const prev = !!this._layers[layerId];
      this._layers[layerId] = !!visible;

      const registry = root.HYLayerRegistry;
      const def = registry ? registry.get(layerId) : null;
      const isParent = def && def.children && def.children.length > 0;

      // If this is a parent layer, propagate state to all children if desired
      if (isParent && def.children) {
        def.children.forEach(childId => {
          // Keep child setting or ensure child knows parent state
          if (!this._layers.hasOwnProperty(childId)) {
            const childDef = registry ? registry.get(childId) : null;
            this._layers[childId] = childDef ? childDef.defaultVisible : true;
          }
        });
      }

      if (!silent && prev !== visible) {
        this._notify('layer', {
          layerId,
          visible: !!visible,
          isParent,
          children: isParent ? def.children : null,
          parent: def ? def.parent : null,
        });
      }
    }

    /**
     * Check if a layer is set to visible in state.
     * @param {string} layerId
     * @returns {boolean}
     */
    isLayerVisible(layerId) {
      return !!this._layers[layerId];
    }

    /**
     * Check if a layer is functionally enabled (parent is visible AND layer itself is visible).
     * @param {string} layerId
     * @returns {boolean}
     */
    isLayerEnabled(layerId) {
      if (!this.isLayerVisible(layerId)) return false;

      const registry = root.HYLayerRegistry;
      const def = registry ? registry.get(layerId) : null;
      if (!def || !def.parent) return true;

      // Must have parent visible
      return this.isLayerVisible(def.parent);
    }

    /**
     * Set layer rendering opacity.
     * @param {string} layerId
     * @param {number} opacity - 0.0 to 1.0
     */
    setLayerOpacity(layerId, opacity) {
      const clamped = Math.max(0, Math.min(1, parseFloat(opacity) || 1.0));
      this._layerOpacities[layerId] = clamped;
      this._notify('layer:opacity', { layerId, opacity: clamped });
    }

    /**
     * Get layer rendering opacity.
     * @param {string} layerId
     * @returns {number}
     */
    getLayerOpacity(layerId) {
      if (this._layerOpacities.hasOwnProperty(layerId)) {
        return this._layerOpacities[layerId];
      }
      const registry = root.HYLayerRegistry;
      const def = registry ? registry.get(layerId) : null;
      return (def && def.opacity !== undefined) ? def.opacity : 1.0;
    }

    /**
     * Reset all layers to their default configured visibility and opacity.
     */
    resetLayers() {
      const registry = root.HYLayerRegistry;
      if (!registry) return;

      registry.getAll().forEach(def => {
        this._layers[def.id] = def.defaultVisible;
        if (def.opacity !== undefined) {
          this._layerOpacities[def.id] = def.opacity;
        }
      });

      this._notify('layers:reset', { state: { ...this._layers } });
    }

    /**
     * Hide all toggleable layers with 1 click.
     */
    hideAllLayers() {
      const registry = root.HYLayerRegistry;
      if (!registry) return;

      registry.getAll().forEach(def => {
        this._layers[def.id] = false;
      });

      this._notify('layers:bulk', { action: 'hide_all', visible: false });
    }

    /**
     * Show all layers with 1 click.
     */
    showAllLayers() {
      const registry = root.HYLayerRegistry;
      if (!registry) return;

      registry.getAll().forEach(def => {
        this._layers[def.id] = true;
      });

      this._notify('layers:bulk', { action: 'show_all', visible: true });
    }

    /**
     * Get the count of currently active visible root/child layers.
     * @returns {number}
     */
    getActiveLayerCount() {
      const registry = root.HYLayerRegistry;
      if (!registry) return 0;

      let count = 0;
      registry.getAll().forEach(def => {
        if (this.isLayerEnabled(def.id)) {
          count++;
        }
      });
      return count;
    }

    /** @returns {string[]} Array of visible layer IDs */
    getVisibleLayers() {
      return Object.keys(this._layers).filter(id => this._layers[id]);
    }

    /* ── Selection State ───────────────────────────── */

    selectPlace(placeId) {
      this.selectedPlaceId = placeId;
      this._notify('select', { placeId });
    }

    /* ── User Location ─────────────────────────────── */

    setUserLocation(lat, lng) {
      this.userLat = lat;
      this.userLng = lng;
    }

    getUserLocation() {
      if (this.userLat === null || this.userLng === null) return null;
      return { lat: this.userLat, lng: this.userLng };
    }

    /* ── Pub/Sub ───────────────────────────────────── */

    /**
     * Subscribe to state changes.
     * @param {'view'|'mode'|'layer'|'select'} event
     * @param {Function} callback
     * @returns {Function} unsubscribe function
     */
    on(event, callback) {
      if (!this._subscribers[event]) {
        this._subscribers[event] = [];
      }
      this._subscribers[event].push(callback);
      return () => {
        this._subscribers[event] = this._subscribers[event].filter(fn => fn !== callback);
      };
    }

    /** @private */
    _notify(event, data) {
      if (this._subscribers[event]) {
        this._subscribers[event].forEach(fn => {
          try { fn(data); } catch (e) { console.error(`[MapState] Error in ${event} subscriber:`, e); }
        });
      }
    }

    /* ── WebGL Capability Check ────────────────────── */

    /**
     * Check if the device supports 3D rendering.
     * @returns {boolean}
     */
    static canDo3D() {
      try {
        const canvas = document.createElement('canvas');
        const gl = canvas.getContext('webgl2') || canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
        if (!gl) return false;

        // Check for reasonable GPU capability
        const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
        if (debugInfo) {
          const renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
          // Block known software renderers
          if (/SwiftShader|llvmpipe|Mesa/i.test(renderer)) return false;
        }

        // Check device memory if available (Android Chrome)
        if (navigator.deviceMemory && navigator.deviceMemory < 3) return false;

        return true;
      } catch (e) {
        return false;
      }
    }
  }

  // Singleton
  root.HYMapState = new MapState();

  // Also expose the class for testing
  root.HYMapStateClass = MapState;

})(window);
