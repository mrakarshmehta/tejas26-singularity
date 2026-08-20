/* ═══════════════════════════════════════════════════════════════════
   HiddenYatra — MapTransition (2D ↔ 3D Smooth Crossfade)
   Handles the visual transition between Leaflet and MapLibre engines
   ═══════════════════════════════════════════════════════════════════ */

(function (root) {
  'use strict';

  class MapTransition {
    constructor() {
      /** @type {boolean} */
      this._transitioning = false;

      /** @type {HTMLElement|null} */
      this._loadingOverlay = null;
    }

    /**
     * Transition from 2D (Leaflet) to 3D (MapLibre).
     * @param {Object} leafletAdapter   - HYMapLeafletAdapter instance
     * @param {Object} maplibreAdapter  - HYMapMaplibreAdapter instance
     * @param {HTMLElement} maplibreContainer - The 3D canvas container element
     * @param {Array} places - Tourist places data for 3D markers
     * @returns {Promise<boolean>} True if transition succeeded
     */
    async transitionTo3D(leafletAdapter, maplibreAdapter, maplibreContainer, places) {
      if (this._transitioning) return false;
      this._transitioning = true;

      const state = root.HYMapState;

      try {
        // Step 1: Show loading state
        this._showLoading(maplibreContainer.parentElement, 'Entering 3D Terrain...');

        // Step 2: Read current Leaflet viewport
        const currentView = {
          lat: leafletAdapter.getCenter().lat,
          lng: leafletAdapter.getCenter().lng,
          zoom: leafletAdapter.getZoom(),
          pitch: 0,
          bearing: 0,
        };

        // Step 3: Initialize MapLibre (lazy-load CDN + create instance)
        if (!maplibreAdapter.isLoaded()) {
          maplibreContainer.style.opacity = '0';
          maplibreContainer.style.position = 'absolute';
          maplibreContainer.style.top = '0';
          maplibreContainer.style.left = '0';
          maplibreContainer.style.width = '100%';
          maplibreContainer.style.height = '100%';
          maplibreContainer.style.zIndex = '0';

          await maplibreAdapter.init(maplibreContainer, currentView);
        }

        // Step 4: Transfer active GeoJSON layers
        await this._transferLayers(leafletAdapter, maplibreAdapter);

        // Step 5: Add tourist place markers to 3D map
        if (places && places.length > 0) {
          maplibreAdapter.addPlaceMarkers(places);
        }

        // Step 6: Hide loading overlay
        this._hideLoading();

        // Step 7: Crossfade — fade out Leaflet, fade in MapLibre
        await Promise.all([
          leafletAdapter.fadeOut(500),
          maplibreAdapter.fadeIn(500),
        ]);

        // Step 8: Animate pitch up for 3D effect
        await maplibreAdapter.animatePitchIn(50, 1500);

        // Step 9: Update state
        if (state) {
          state.setMode('3d');
          const view = state.getView();
          state.setView({ ...view, pitch: 50, bearing: -15 }, 'transition');
        }

        // Step 10: Show 3D-specific controls
        this._show3DControls();

        this._transitioning = false;
        return true;

      } catch (err) {
        console.error('[MapTransition] 3D transition failed:', err);
        this._hideLoading();

        // Fallback: ensure Leaflet is visible
        leafletAdapter.show();
        maplibreAdapter.hide();

        // Determine granular diagnostic reason
        let userMsg = '3D Terrain could not be started. Continuing in 2D.';
        if (err && err.code === 'WEBGL_UNAVAILABLE') {
          userMsg = 'WebGL hardware acceleration is disabled or unsupported. Continuing in 2D.';
        } else if (err && err.code === 'MAPLIBRE_SCRIPT_LOAD_FAILED') {
          userMsg = 'Unable to download 3D map engine library. Please check your internet connection.';
        } else if (err && err.code === 'DEM_LOAD_FAILED') {
          userMsg = 'Elevation terrain service temporarily unavailable. Continuing in 2D.';
        } else if (err && err.code === 'MAPLIBRE_INIT_FAILED') {
          userMsg = `3D engine initialization failed: ${err.message || 'Unknown error'}`;
        } else if (err && err.message) {
          userMsg = `3D Terrain error: ${err.message}`;
        }

        // Show user-friendly error
        this._showToast(userMsg, 'warning');

        this._transitioning = false;
        return false;
      }
    }

    /**
     * Transition from 3D (MapLibre) back to 2D (Leaflet).
     * @param {Object} leafletAdapter   - HYMapLeafletAdapter instance
     * @param {Object} maplibreAdapter  - HYMapMaplibreAdapter instance
     * @returns {Promise<boolean>}
     */
    async transitionTo2D(leafletAdapter, maplibreAdapter) {
      if (this._transitioning) return false;
      this._transitioning = true;

      const state = root.HYMapState;

      try {
        // Step 1: Animate pitch back to flat
        await maplibreAdapter.animatePitchOut(800);

        // Step 2: Read MapLibre viewport for sync
        if (maplibreAdapter.map) {
          const center = maplibreAdapter.map.getCenter();
          const zoom = maplibreAdapter.map.getZoom();

          // Sync Leaflet view to match
          leafletAdapter.map.setView([center.lat, center.lng], zoom, { animate: false });
        }

        // Step 3: Crossfade — fade out MapLibre, fade in Leaflet
        await Promise.all([
          maplibreAdapter.fadeOut(500),
          leafletAdapter.fadeIn(500),
        ]);

        // Step 4: Destroy MapLibre instance (free GPU memory)
        maplibreAdapter.destroy();

        // Step 5: Update state
        if (state) {
          state.setMode('2d');
          state.setView({ pitch: 0, bearing: 0 }, 'transition');
        }

        // Step 6: Hide 3D controls, restore 2D controls
        this._hide3DControls();

        this._transitioning = false;
        return true;

      } catch (err) {
        console.error('[MapTransition] 2D transition failed:', err);

        // Ensure Leaflet is visible
        leafletAdapter.show();

        this._transitioning = false;
        return false;
      }
    }

    /** @returns {boolean} */
    isTransitioning() {
      return this._transitioning;
    }

    /* ── Private Helpers ───────────────────────────── */

    /**
     * Transfer active GeoJSON layers from Leaflet to MapLibre.
     * @private
     */
    async _transferLayers(leafletAdapter, maplibreAdapter) {
      const registry = root.HYLayerRegistry;
      const state = root.HYMapState;
      if (!registry || !state) return;

      const visibleLayers = state.getVisibleLayers();
      for (const layerId of visibleLayers) {
        const def = registry.get(layerId);
        if (!def || (def.sourceType !== 'geojson' && def.type !== 'geojson') || !def.source) continue;

        // Fetch data (returns instantly from cache if already loaded)
        const data = await registry.fetchData(layerId);
        if (data) {
          maplibreAdapter.addGeoJSONLayer(layerId, data, def.style);
        }
      }
    }

    /**
     * Show loading overlay during 3D engine initialization.
     * @private
     */
    _showLoading(parentEl, message) {
      if (this._loadingOverlay) this._hideLoading();

      this._loadingOverlay = document.createElement('div');
      this._loadingOverlay.className = 'hy-map-loading-overlay';
      this._loadingOverlay.innerHTML = `
        <div class="hy-map-loading-content">
          <div class="hy-map-loading-spinner"></div>
          <div class="hy-map-loading-text">${message || 'Loading 3D Terrain...'}</div>
          <div class="hy-map-loading-sub">Loading terrain data from AWS</div>
        </div>
      `;

      if (parentEl) {
        parentEl.appendChild(this._loadingOverlay);
      } else {
        document.body.appendChild(this._loadingOverlay);
      }

      // Animate in
      requestAnimationFrame(() => {
        this._loadingOverlay.style.opacity = '1';
      });
    }

    /** @private */
    _hideLoading() {
      if (this._loadingOverlay) {
        this._loadingOverlay.style.opacity = '0';
        setTimeout(() => {
          if (this._loadingOverlay && this._loadingOverlay.parentElement) {
            this._loadingOverlay.parentElement.removeChild(this._loadingOverlay);
          }
          this._loadingOverlay = null;
        }, 300);
      }
    }

    /** @private */
    _show3DControls() {
      const ctrl = document.getElementById('hy-3d-controls');
      if (ctrl) ctrl.style.display = 'flex';

      // Update toggle button state
      const toggle = document.getElementById('hy-3d-toggle');
      if (toggle) {
        toggle.classList.add('active');
        const label = toggle.querySelector('.btn-label');
        if (label) label.textContent = 'Exit 3D';
      }
    }

    /** @private */
    _hide3DControls() {
      const ctrl = document.getElementById('hy-3d-controls');
      if (ctrl) ctrl.style.display = 'none';

      const toggle = document.getElementById('hy-3d-toggle');
      if (toggle) {
        toggle.classList.remove('active');
        const label = toggle.querySelector('.btn-label');
        if (label) label.textContent = '3D Terrain';
      }
    }

    /**
     * Show a toast notification.
     * @private
     */
    _showToast(message, type) {
      const toast = document.createElement('div');
      toast.className = `hy-map-toast hy-map-toast--${type || 'info'}`;
      toast.textContent = message;
      toast.style.cssText = `
        position: fixed; bottom: 80px; left: 50%; transform: translateX(-50%);
        background: ${type === 'warning' ? '#f59e0b' : '#6366f1'}; color: #fff;
        padding: 12px 24px; border-radius: 12px; font-size: 0.85rem;
        font-weight: 600; z-index: 10000; box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        animation: hyToastIn 0.3s ease;
      `;
      document.body.appendChild(toast);
      setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.3s';
        setTimeout(() => toast.remove(), 300);
      }, 4000);
    }
  }

  root.HYMapTransition = new MapTransition();

})(window);
