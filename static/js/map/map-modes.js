/* ═══════════════════════════════════════════════════════════════════
   HiddenYatra — MapModes (Mode Registry & Manager)
   Centralized registry of visual map modes and mode-switching logic.
   Modes are VISUAL STYLES (basemaps), NOT data layers.
   ═══════════════════════════════════════════════════════════════════ */

(function (root) {
  'use strict';

  /* ── Mode Definitions ────────────────────────────── */

  const MAP_MODES = {
    normal: {
      id: 'normal',
      label: 'Normal',
      icon: '🗺️',
      engine: 'leaflet',
      tileSource: 'carto_light',
      labelOverlay: null,
      requires3D: false,
      description: 'Clean standard map',
    },
    dark: {
      id: 'dark',
      label: 'Dark',
      icon: '🌙',
      engine: 'leaflet',
      tileSource: 'carto_dark',
      labelOverlay: null,
      requires3D: false,
      description: 'Dark themed map',
    },
    terrain: {
      id: 'terrain',
      label: 'Terrain',
      icon: '⛰️',
      engine: 'leaflet',
      tileSource: 'opentopomap',
      labelOverlay: null,
      requires3D: false,
      description: 'Topographic contour map',
    },
    terrain3d: {
      id: 'terrain3d',
      label: '3D',
      icon: '🏔️',
      engine: 'maplibre',
      tileSource: 'carto_light',
      labelOverlay: null,
      requires3D: true,
      description: '3D terrain with elevation',
    },
    satellite: {
      id: 'satellite',
      label: 'Satellite',
      icon: '🛰️',
      engine: 'leaflet',
      tileSource: 'esri_satellite',
      labelOverlay: null,
      requires3D: false,
      description: 'Satellite imagery',
    },
    hybrid: {
      id: 'hybrid',
      label: 'Hybrid',
      icon: '🌐',
      engine: 'leaflet',
      tileSource: 'esri_satellite',
      labelOverlay: 'carto_labels',
      requires3D: false,
      description: 'Satellite with road labels',
    },
  };

  /** Ordered array for UI rendering */
  const MODE_ORDER = ['normal', 'dark', 'terrain', 'terrain3d', 'satellite', 'hybrid'];

  /* ── Mode Manager ────────────────────────────────── */

  class MapModeManager {
    /**
     * @param {Object} opts
     * @param {Object} opts.leafletAdapter  - HYMapLeafletAdapter
     * @param {Object} opts.maplibreAdapter - HYMapMaplibreAdapter
     * @param {Object} [opts.googleAdapter] - HYMapGoogleAdapter
     * @param {Function} opts.toggle3D     - Reference to HYMap._toggle3D()
     */
    constructor(opts) {
      this.leafletAdapter = opts.leafletAdapter;
      this.maplibreAdapter = opts.maplibreAdapter;
      this.googleAdapter = opts.googleAdapter || null;
      this.toggle3D = opts.toggle3D;

      /** @type {L.TileLayer|null} Current label overlay (for Hybrid mode) */
      this._labelOverlay = null;

      /** @type {HTMLElement|null} The mode dock container */
      this._dock = null;
    }

    /* ── Mode Switching ────────────────────────────── */

    /**
     * Switch to a map mode.
     * @param {string} modeId
     * @returns {Promise<boolean>} true if switch succeeded
     */
    async setMode(modeId) {
      const modeDef = MAP_MODES[modeId];
      if (!modeDef) {
        console.warn(`[MapModes] Unknown mode: ${modeId}`);
        return false;
      }

      const state = root.HYMapState;
      const currentMode = state.getMapMode();

      if (currentMode === modeId) return true;

      // Check 3D capability
      if (modeDef.requires3D && !root.HYMapStateClass.canDo3D()) {
        console.warn('[MapModes] Device does not support 3D mode');
        return false;
      }

      const currentDef = MAP_MODES[currentMode];
      const wasIn3D = currentDef && currentDef.requires3D;
      const goingTo3D = modeDef.requires3D;

      // ── Google Maps Engine Handling (Phase G4A) ──
      const isGoogleEngine = (root.MAP_ENGINE === 'google' || Boolean(this.googleAdapter));
      if (isGoogleEngine) {
        state.setMapMode(modeId);
        this._updateDockActive(modeId);

        if (goingTo3D) {
          if (this.googleAdapter && this.googleAdapter.terrainManager) {
            this.googleAdapter.terrainManager.enable();
            this.googleAdapter.terrainManager.focusRajgir();
          } else if (this.googleAdapter && this.googleAdapter.setTilt) {
            this.googleAdapter.setTilt(50);
          }
        } else if (wasIn3D && !goingTo3D) {
          if (this.googleAdapter && this.googleAdapter.terrainManager) {
            this.googleAdapter.terrainManager.disable();
          }
          if (this.googleAdapter && this.googleAdapter.setTilt) {
            this.googleAdapter.setTilt(0);
          }
        }
        return true;
      }

      // ── Leaflet / MapLibre Engine Handling ───────
      // ── Case 1: 2D → 3D ────────────────────────
      if (!wasIn3D && goingTo3D) {
        // Update state first so dock UI reflects immediately
        state.setMapMode(modeId);
        this._updateDockActive(modeId);

        // Trigger the existing 3D transition
        if (this.toggle3D) {
          await this.toggle3D();
        }
        return true;
      }

      // ── Case 2: 3D → 2D ────────────────────────
      if (wasIn3D && !goingTo3D) {
        // Update state first
        state.setMapMode(modeId);
        this._updateDockActive(modeId);

        // Exit 3D first
        if (this.toggle3D && state.is3D()) {
          await this.toggle3D();
        }

        // Now swap basemap in Leaflet
        this._applyLeafletMode(modeDef);
        return true;
      }

      // ── Case 3: 2D → 2D (basemap swap only) ───
      state.setMapMode(modeId);
      this._updateDockActive(modeId);
      this._applyLeafletMode(modeDef);
      return true;
    }

    /**
     * Apply a 2D mode's basemap + optional label overlay.
     * @private
     * @param {Object} modeDef - Mode definition object
     */
    _applyLeafletMode(modeDef) {
      // Remove any existing label overlay
      this._removeLabelOverlay();

      // Switch basemap
      if (this.leafletAdapter) {
        this.leafletAdapter.setBasemap(modeDef.tileSource);
      }

      // Add label overlay if needed (Hybrid mode)
      if (modeDef.labelOverlay) {
        this._addLabelOverlay(modeDef.labelOverlay);
      }
    }

    /**
     * Add a transparent label tile overlay on top of the basemap.
     * @private
     * @param {string} sourceId - Tile source ID from HYTileSources
     */
    _addLabelOverlay(sourceId) {
      const sources = root.HYTileSources;
      if (!sources || !sources[sourceId]) return;

      const src = sources[sourceId];
      const opts = {
        attribution: src.attribution,
        maxZoom: src.maxZoom || 19,
        pane: 'overlayPane', // Render above base tiles but below markers
      };
      if (src.subdomains) opts.subdomains = src.subdomains;

      this._labelOverlay = L.tileLayer(src.url, opts);
      if (this.leafletAdapter && this.leafletAdapter.map) {
        this._labelOverlay.addTo(this.leafletAdapter.map);
      }
    }

    /** @private Remove label overlay from Leaflet map */
    _removeLabelOverlay() {
      if (this._labelOverlay) {
        if (this.leafletAdapter && this.leafletAdapter.map) {
          this.leafletAdapter.map.removeLayer(this._labelOverlay);
        }
        this._labelOverlay = null;
      }
    }

    /* ── Mode Dock UI ──────────────────────────────── */

    /**
     * Build and inject the floating mode dock into the map container.
     * @param {HTMLElement} container - Map container element
     */
    buildDock(container) {
      if (this._dock) return;

      const can3D = root.HYMapStateClass.canDo3D();
      const currentMode = root.HYMapState.getMapMode();

      const dock = document.createElement('div');
      dock.id = 'hy-mode-dock';
      dock.className = 'hy-mode-dock';
      dock.setAttribute('role', 'toolbar');
      dock.setAttribute('aria-label', 'Map visual style');

      let buttonsHTML = '';
      MODE_ORDER.forEach(modeId => {
        const def = MAP_MODES[modeId];
        if (!def) return;

        // Skip 3D mode if device doesn't support it
        if (def.requires3D && !can3D) return;

        const isActive = modeId === currentMode;
        buttonsHTML += `
          <button
            class="hy-mode-pill ${isActive ? 'active' : ''}"
            data-mode="${modeId}"
            title="${def.description}"
            aria-label="${def.label} map style"
            aria-pressed="${isActive}"
          >
            <span class="hy-mode-pill-icon">${def.icon}</span>
            <span class="hy-mode-pill-label">${def.label}</span>
          </button>`;
      });

      dock.innerHTML = `<div class="hy-mode-dock-inner">${buttonsHTML}</div>`;

      container.appendChild(dock);
      this._dock = dock;

      // Bind click events
      dock.querySelectorAll('.hy-mode-pill').forEach(pill => {
        pill.addEventListener('click', () => {
          const modeId = pill.dataset.mode;
          this.setMode(modeId);
        });
      });

      // Keyboard navigation: arrow keys move between pills
      dock.addEventListener('keydown', (e) => {
        const pills = Array.from(dock.querySelectorAll('.hy-mode-pill'));
        const current = document.activeElement;
        const idx = pills.indexOf(current);
        if (idx === -1) return;

        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
          e.preventDefault();
          const next = pills[(idx + 1) % pills.length];
          next.focus();
        } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
          e.preventDefault();
          const prev = pills[(idx - 1 + pills.length) % pills.length];
          prev.focus();
        } else if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          current.click();
        }
      });
    }

    /**
     * Update the active pill highlight in the dock.
     * @private
     * @param {string} modeId
     */
    _updateDockActive(modeId) {
      if (!this._dock) return;
      this._dock.querySelectorAll('.hy-mode-pill').forEach(pill => {
        const isActive = pill.dataset.mode === modeId;
        pill.classList.toggle('active', isActive);
        pill.setAttribute('aria-pressed', String(isActive));
      });
    }

    /**
     * Externally sync the dock when 3D is toggled from elsewhere (e.g. Layer Manager).
     * @param {string} engineMode - '2d' or '3d'
     */
    syncFromEngineMode(engineMode) {
      const state = root.HYMapState;
      if (engineMode === '3d' && state.getMapMode() !== 'terrain3d') {
        state.setMapMode('terrain3d');
        this._updateDockActive('terrain3d');
      } else if (engineMode === '2d' && state.getMapMode() === 'terrain3d') {
        // Returning from 3D — revert to Normal
        state.setMapMode('normal');
        this._updateDockActive('normal');
        this._applyLeafletMode(MAP_MODES.normal);
      }
    }

    /* ── Cleanup ───────────────────────────────────── */

    destroy() {
      this._removeLabelOverlay();
      if (this._dock && this._dock.parentElement) {
        this._dock.parentElement.removeChild(this._dock);
      }
      this._dock = null;
    }
  }

  // Exports
  root.HY_MAP_MODES = MAP_MODES;
  root.HY_MODE_ORDER = MODE_ORDER;
  root.HYMapModeManager = MapModeManager;

})(window);
