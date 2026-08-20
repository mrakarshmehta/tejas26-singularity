/* ═══════════════════════════════════════════════════════════════════
   HiddenYatra — MapCore (HYMap Orchestrator)
   Central coordinator for the hybrid Leaflet + MapLibre map system.
   Receives the existing Leaflet map instance and wires up
   state, layers, controls, and 3D transitions.
   ═══════════════════════════════════════════════════════════════════ */

(function (root) {
  'use strict';

  class HYMap {
    /**
     * @param {L.Map|google.maps.Map} mapInstance - The existing, already-initialized map
     * @param {Object} [options]
     * @param {HTMLElement} [options.container] - Map container element
     * @param {Array} [options.places] - ALL_PLACES data array
     */
    constructor(mapInstance, options) {
      const opts = options || {};
      const engineType = root.MAP_ENGINE || 'leaflet';

      /** @type {'leaflet'|'google'} */
      this.engineType = engineType;

      /** @type {HTMLElement} */
      this.container = opts.container || (
        engineType === 'google'
          ? mapInstance.getDiv().parentElement
          : mapInstance.getContainer().parentElement
      );

      /** @type {Array} */
      this.places = opts.places || [];

      /* ── Adapters ────────────────────────────── */

      if (engineType === 'google') {
        /** @type {HYMapGoogleAdapter|null} */
        this.googleAdapter = new root.HYMapGoogleAdapter(mapInstance);

        /** @type {L.Map|null} */
        this.leafletMap = null;
        /** @type {HYMapLeafletAdapter|null} */
        this.leafletAdapter = null;
        /** @type {HYMapMaplibreAdapter|null} */
        this.maplibreAdapter = null;
      } else {
        // Leaflet mode (existing behavior, unchanged)
        /** @type {L.Map} */
        this.leafletMap = mapInstance;
        /** @type {HYMapLeafletAdapter} */
        this.leafletAdapter = new root.HYMapLeafletAdapter(mapInstance);
        /** @type {HYMapMaplibreAdapter} */
        this.maplibreAdapter = new root.HYMapMaplibreAdapter();
        /** @type {HYMapGoogleAdapter|null} */
        this.googleAdapter = null;
      }

      /* ── Controls ────────────────────────────── */

      /** @type {HYMapControls|null} */
      this.controls = null;

      /** @type {HYMapModeManager|null} */
      this.modeManager = null;

      /* ── Internal State ──────────────────────────── */

      /** @type {boolean} */
      this._initialized = false;

      /** @type {HTMLElement|null} */
      this._maplibreContainer = null;
    }

    /* ── Initialization ────────────────────────────── */

    /**
     * Initialize the HYMap system.
     * Call this AFTER the existing Leaflet map is fully set up.
     */
    init() {
      if (this._initialized) return;

      // Sync initial state from the active engine
      if (this.engineType === 'google') {
        // Google Maps engine — use googleAdapter for initial state
        const center = this.googleAdapter.getCenter();
        root.HYMapState.activeEngine = 'google';
        root.HYMapState.setView({
          lat: center.lat,
          lng: center.lng,
          zoom: this.googleAdapter.getZoom(),
          pitch: this.googleAdapter.map.getTilt ? this.googleAdapter.map.getTilt() : 0,
          bearing: this.googleAdapter.map.getHeading ? this.googleAdapter.map.getHeading() : 0,
        }, 'init');
      } else {
        // Leaflet engine — existing behavior
        const center = this.leafletMap.getCenter();
        root.HYMapState.setView({
          lat: center.lat,
          lng: center.lng,
          zoom: this.leafletMap.getZoom(),
          pitch: 0,
          bearing: 0,
        }, 'init');
      }

      // Initialize default layer visibility
      const registry = root.HYLayerRegistry;
      if (registry) {
        registry.getAll().forEach(def => {
          root.HYMapState.setLayerVisible(def.id, def.defaultVisible);
        });
      }

      // Create MapLibre container only in Leaflet mode (3D transitions)
      if (this.engineType !== 'google') {
        this._createMaplibreContainer();
      }

      // Build Layer Manager UI
      this._buildControls();

      // Inject toolbar buttons (Layers only — 3D is now in mode dock)
      this._injectToolbarButtons();

      // Initialize Mode Manager & build bottom dock
      this._initModeManager();

      // Subscribe to state changes
      this._bindStateListeners();

      this._initialized = true;

      console.log('[HYMap] ✅ Advanced Map System initialized (' + this.engineType + ' engine)');
    }

    /* ── MapLibre Container ────────────────────────── */

    /** @private */
    _createMaplibreContainer() {
      // Only create in Leaflet mode (Google Maps handles 3D natively)
      if (this.engineType === 'google' || !this.leafletMap) return;

      // Create a hidden container for MapLibre, overlaid on the Leaflet map
      const mapMain = this.leafletMap.getContainer();
      const wrapper = mapMain.parentElement;

      this._maplibreContainer = document.createElement('div');
      this._maplibreContainer.id = 'hy-maplibre-canvas';
      this._maplibreContainer.className = 'hy-maplibre-canvas';
      this._maplibreContainer.style.cssText = `
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        z-index: 0; opacity: 0; pointer-events: none;
      `;

      // Insert after the Leaflet map container
      wrapper.style.position = 'relative';
      wrapper.appendChild(this._maplibreContainer);
    }

    /* ── Controls ──────────────────────────────────── */

    /** @private */
    _buildControls() {
      const adapterConfig = this.engineType === 'google'
        ? { googleAdapter: this.googleAdapter }
        : { leafletAdapter: this.leafletAdapter, maplibreAdapter: this.maplibreAdapter };

      this.controls = new root.HYMapControls(adapterConfig);

      this.controls.buildPanel(this.container);
    }

    /** @private */
    _injectToolbarButtons() {
      const bar = document.getElementById('map-floating-bar');
      if (!bar) return;

      const actionsDiv = bar.querySelector('.bar-actions');
      if (!actionsDiv) return;

      // Layer Manager button
      const layersBtn = document.createElement('button');
      layersBtn.id = 'hy-layers-btn';
      layersBtn.className = 'bar-btn';
      layersBtn.title = 'Map Layers (Custom Layer Manager)';
      layersBtn.setAttribute('aria-label', 'Toggle map layers panel');
      layersBtn.innerHTML = `
        <span class="btn-icon">🗺️</span>
        <span class="btn-label">Layers</span>
        <span class="hy-layers-badge" id="hy-layers-btn-badge" style="display:none;"></span>
      `;
      layersBtn.addEventListener('click', () => {
        if (this.controls) this.controls.togglePanel();
      });

      // Insert Layers button before the reset button
      // NOTE: 3D toggle button removed — now handled by mode dock at bottom
      const resetBtn = actionsDiv.querySelector('#reset-filters-btn');
      if (resetBtn) {
        actionsDiv.insertBefore(layersBtn, resetBtn);
      } else {
        actionsDiv.appendChild(layersBtn);
      }

      // Create 3D-specific controls (hidden initially)
      this._create3DControlsBar();
    }

    /** @private Create the floating 3D controls bar */
    _create3DControlsBar() {
      const bar = document.createElement('div');
      bar.id = 'hy-3d-controls';
      bar.className = 'hy-3d-controls';
      bar.style.display = 'none';
      bar.innerHTML = `
        <button class="hy-3d-ctrl-btn" id="hy-3d-reset-view" title="Reset 3D View">
          🧭 Reset View
        </button>
        <button class="hy-3d-ctrl-btn" id="hy-3d-zoom-in" title="Zoom In">+</button>
        <button class="hy-3d-ctrl-btn" id="hy-3d-zoom-out" title="Zoom Out">−</button>
        <div class="hy-3d-pitch-indicator">
          <span class="hy-3d-pitch-label">Pitch:</span>
          <span class="hy-3d-pitch-value" id="hy-pitch-value">50°</span>
        </div>
      `;

      this.container.appendChild(bar);

      // Bind 3D control events
      const resetBtn = bar.querySelector('#hy-3d-reset-view');
      if (resetBtn) {
        resetBtn.addEventListener('click', () => {
          if (this.maplibreAdapter.map) {
            this.maplibreAdapter.map.easeTo({
              pitch: 50,
              bearing: 0,
              zoom: 8,
              center: [85.3131, 25.0961],
              duration: 1000,
            });
          }
        });
      }

      const zoomIn = bar.querySelector('#hy-3d-zoom-in');
      if (zoomIn) {
        zoomIn.addEventListener('click', () => {
          if (this.maplibreAdapter.map) this.maplibreAdapter.map.zoomIn();
        });
      }

      const zoomOut = bar.querySelector('#hy-3d-zoom-out');
      if (zoomOut) {
        zoomOut.addEventListener('click', () => {
          if (this.maplibreAdapter.map) this.maplibreAdapter.map.zoomOut();
        });
      }
    }

    /* ── Mode Manager Init ─────────────────────────── */

    /** @private Initialize the MapModeManager and build the bottom dock */
    _initModeManager() {
      if (!root.HYMapModeManager) {
        console.warn('[HYMap] MapModeManager not loaded, skipping mode dock');
        return;
      }

      this.modeManager = new root.HYMapModeManager({
        leafletAdapter: this.leafletAdapter,
        maplibreAdapter: this.maplibreAdapter,
        googleAdapter: this.googleAdapter,
        toggle3D: () => this._toggle3D(),
      });

      // Build the dock inside the map container
      this.modeManager.buildDock(this.container);
    }

    /* ── 3D Toggle ─────────────────────────────────── */

    /** @private */
    async _toggle3D() {
      const state = root.HYMapState;
      const transition = root.HYMapTransition;

      if (transition.isTransitioning()) return;

      if (state.is3D()) {
        // 3D → 2D
        await transition.transitionTo2D(this.leafletAdapter, this.maplibreAdapter);

        // Show/hide 3D HUD & update mode dock
        this._update3DUI(false);

        // Sync mode dock back to previous 2D mode
        if (this.modeManager) {
          this.modeManager.syncFromEngineMode('2d');
        }
      } else {
        // 2D → 3D
        const success = await transition.transitionTo3D(
          this.leafletAdapter,
          this.maplibreAdapter,
          this._maplibreContainer,
          this.places
        );

        if (success) {
          // Update controls reference
          if (this.controls) {
            this.controls.maplibreAdapter = this.maplibreAdapter;
          }

          // Show 3D HUD
          this._update3DUI(true);

          // Sync mode dock to 3D
          if (this.modeManager) {
            this.modeManager.syncFromEngineMode('3d');
          }

          // Update pitch indicator on camera move
          if (this.maplibreAdapter.map) {
            this.maplibreAdapter.map.on('pitchend', () => {
              const pitchEl = document.getElementById('hy-pitch-value');
              if (pitchEl) {
                pitchEl.textContent = `${Math.round(this.maplibreAdapter.map.getPitch())}°`;
              }
            });
          }
        }
      }
    }

    /**
     * Show/hide 3D-specific UI elements.
     * @private
     * @param {boolean} is3D
     */
    _update3DUI(is3D) {
      const controls3D = document.getElementById('hy-3d-controls');
      if (controls3D) {
        controls3D.style.display = is3D ? 'flex' : 'none';
      }

      // Add/remove 3D class on mode dock for styling
      if (this.modeManager && this.modeManager._dock) {
        this.modeManager._dock.classList.toggle('hy-mode-dock--3d', is3D);
      }
    }

    /* ── State Listeners ───────────────────────────── */

    /** @private */
    _bindStateListeners() {
      const state = root.HYMapState;

      // Listen for layer toggle events from the Layer Manager
      state.on('layer', (data) => {
        if (data.event === 'feature-click' && data.feature) {
          // A district/block boundary was clicked
          const name = data.feature.properties.name ||
                       data.feature.properties.NAME ||
                       data.feature.properties.district || '';
          if (name) {
            // Update the district filter dropdown to match
            const districtSelect = document.getElementById('map-district-filter');
            if (districtSelect) {
              const option = Array.from(districtSelect.options).find(
                opt => opt.value.toLowerCase() === name.toLowerCase()
              );
              if (option) {
                districtSelect.value = option.value;
                districtSelect.dispatchEvent(new Event('change'));
              }
            }
          }
        }
      });
    }

    /* ── Public API ─────────────────────────────────── */

    /**
     * Toggle a specific layer on/off.
     * @param {string} layerId
     * @param {boolean} visible
     */
    async setLayerVisible(layerId, visible) {
      root.HYMapState.setLayerVisible(layerId, visible);

      // Update checkbox in Layer Manager
      if (this.controls && this.controls._panel) {
        const cb = this.controls._panel.querySelector(`input[value="${layerId}"]`);
        if (cb) cb.checked = visible;
      }

      // Route to active engine
      if (this.engineType === 'google' && this.googleAdapter) {
        await this.googleAdapter.toggleLayer(layerId, visible);
      } else {
        if (this.leafletAdapter) {
          await this.leafletAdapter.toggleLayer(layerId, visible);
        }
        if (this.maplibreAdapter && this.maplibreAdapter.isLoaded()) {
          await this.maplibreAdapter.toggleLayer(layerId, visible);
        }
      }
    }

    /**
     * Switch the visual map mode (normal, dark, terrain, terrain3d, satellite, hybrid).
     * @param {string} modeId
     */
    async setMapMode(modeId) {
      if (this.modeManager) {
        await this.modeManager.setMode(modeId);
      }
    }

    /**
     * Switch the base map tile source.
     * @param {string} sourceId - Key from HYTileSources
     */
    setBasemap(sourceId) {
      if (this.engineType === 'google' && this.googleAdapter) {
        this.googleAdapter.setBasemap(sourceId);
      } else if (this.leafletAdapter) {
        this.leafletAdapter.setBasemap(sourceId);
      }
    }

    /**
     * Get the current mode.
     * @returns {'2d'|'3d'}
     */
    getMode() {
      return root.HYMapState.mode;
    }

    /**
     * Fly to a location on whichever engine is active.
     * @param {number} lat
     * @param {number} lng
     * @param {number} [zoom]
     */
    flyTo(lat, lng, zoom) {
      if (this.engineType === 'google' && this.googleAdapter) {
        this.googleAdapter.flyTo(lat, lng, zoom);
      } else {
        const state = root.HYMapState;
        if (state.is3D() && this.maplibreAdapter.isLoaded()) {
          this.maplibreAdapter.map.flyTo({
            center: [lng, lat],
            zoom: zoom || this.maplibreAdapter.map.getZoom(),
            duration: 1500,
          });
        } else {
          this.leafletAdapter.flyTo(lat, lng, zoom);
        }
      }
    }

    /**
     * Clean up all resources.
     */
    destroy() {
      if (this.modeManager) this.modeManager.destroy();
      if (this.controls) this.controls.destroy();
      if (this.googleAdapter) this.googleAdapter.destroy();
      if (this.maplibreAdapter) this.maplibreAdapter.destroy();
      if (this._maplibreContainer && this._maplibreContainer.parentElement) {
        this._maplibreContainer.parentElement.removeChild(this._maplibreContainer);
      }
      this._initialized = false;
    }
  }

  root.HYMap = HYMap;

})(window);
