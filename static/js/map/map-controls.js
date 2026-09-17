// Mobile touch gesture helper for interactive explore map
if (typeof window !== 'undefined' && 'ontouchstart' in window) {
  window.HY_IS_TOUCH_DEVICE = true;
}

/* ═══════════════════════════════════════════════════════════════════
   HiddenYatra — MapControls (Custom Modular Layer Manager Panel)
   Controls all geographic layers across 7 categories with parent/child
   hierarchies, real-time search, quick actions, accessibility & 2D/3D sync.
   ═══════════════════════════════════════════════════════════════════ */

(function (root) {
  'use strict';

  class MapControls {
    /**
     * @param {Object} options
     * @param {Object} options.leafletAdapter  - HYMapLeafletAdapter instance
     * @param {Object} options.maplibreAdapter - HYMapMaplibreAdapter instance (may be null initially)
     */
    constructor(options) {
      this.leafletAdapter = options.leafletAdapter;
      this.maplibreAdapter = options.maplibreAdapter || null;
      this.googleAdapter = options.googleAdapter || null;

      /** @type {HTMLElement|null} */
      this._panel = null;

      /** @type {HTMLElement|null} */
      this._backdrop = null;

      /** @type {boolean} */
      this._panelOpen = false;

      /** @type {string} Current search query in layer manager */
      this._searchQuery = '';

      /** @type {Function[]} Unsubscribe functions for state listeners */
      this._unsubs = [];
    }

    /* ── Panel Construction ─────────────────────────── */

    /**
     * Build and inject the Layer Manager panel and backdrop into the DOM.
     * @param {HTMLElement} parentEl - Container to append the panel to
     */
    buildPanel(parentEl) {
      if (this._panel) return; // Already built

      // 1. Build backdrop for click-outside & mobile overlay
      const backdrop = document.createElement('div');
      backdrop.id = 'hy-lm-backdrop';
      backdrop.className = 'hy-lm-backdrop';
      parentEl.appendChild(backdrop);
      this._backdrop = backdrop;

      // 2. Build main sliding drawer panel
      const panel = document.createElement('div');
      panel.id = 'hy-layer-manager';
      panel.className = 'hy-layer-manager';
      panel.setAttribute('role', 'dialog');
      panel.setAttribute('aria-modal', 'true');
      panel.setAttribute('aria-label', 'Layer Manager');
      panel.innerHTML = this._buildPanelHTML();

      parentEl.appendChild(panel);
      this._panel = panel;

      // 3. Bind event listeners
      this._bindEvents();

      // 4. Subscribe to HYMapState events
      this._subscribeToState();

      // 5. Initial sync of layer count badge and states
      this._updateActiveBadge();
    }

    /**
     * Build complete HTML markup for the Layer Manager panel.
     * @private
     * @returns {string}
     */
    _buildPanelHTML() {
      const layerGroups = root.HY_LAYER_GROUPS || root.HYLayerGroups || [];
      const registry = root.HYLayerRegistry;
      const state = root.HYMapState;
      const can3D = state ? root.HYMapStateClass.canDo3D() : false;

      // Build 7 Accordion Sections
      let accordionHTML = '';

      layerGroups.forEach(group => {
        const layersInGroup = registry ? registry.getByGroup(group.id) : [];
        if (layersInGroup.length === 0) return;

        // Separate root layers vs child layers
        const rootLayers = layersInGroup.filter(l => !l.parent);

        let groupItemsHTML = '';

        rootLayers.forEach(layer => {
          // Skip 3D-only layer if device does not support WebGL/3D
          if (!can3D && layer.engineSupport.length === 1 && layer.engineSupport[0] === 'maplibre') {
            return;
          }

          const isVisible = state ? state.isLayerVisible(layer.id) : layer.defaultVisible;
          const checkedAttr = isVisible ? 'checked' : '';
          const ariaChecked = isVisible ? 'true' : 'false';
          const is3DOnly = layer.engineSupport.length === 1 && layer.engineSupport[0] === 'maplibre';
          const badge3D = is3DOnly ? '<span class="hy-lm-badge-3d">3D</span>' : '';
          const hasChildren = layer.children && layer.children.length > 0;

          // Build child items if this is a parent layer
          let childrenHTML = '';
          if (hasChildren) {
            const children = registry.getChildren(layer.id);
            const parentDisabled = !isVisible;

            let childListHTML = '';
            children.forEach(child => {
              const childVisible = state ? state.isLayerVisible(child.id) : child.defaultVisible;
              const childChecked = childVisible ? 'checked' : '';
              const childAriaChecked = childVisible ? 'true' : 'false';

              const childSwitch = child.disabled ? `
                <span class="hy-lm-badge-planned" style="font-size:0.65rem;padding:2px 6px;border-radius:4px;background:rgba(148,163,184,0.18);color:#94a3b8;font-weight:600;letter-spacing:0.3px;" title="Dataset planned for future release">Planned</span>
              ` : `
                <label class="hy-lm-switch">
                  <input type="checkbox"
                         id="hy-layer-switch-${child.id}"
                         role="switch"
                         aria-checked="${childAriaChecked}"
                         data-layer="${child.id}"
                         data-parent="${layer.id}"
                         class="hy-lm-switch-input"
                         ${childChecked}>
                  <span class="hy-lm-slider-mark"></span>
                </label>
              `;

              childListHTML += `
                <div class="hy-lm-item hy-lm-child-item ${child.disabled ? 'is-disabled' : ''}" data-layer-id="${child.id}" data-parent-id="${layer.id}">
                  <label class="hy-lm-switch-label" for="hy-layer-switch-${child.id}">
                    <span class="hy-lm-icon">${child.icon || child.emoji || '•'}</span>
                    <span class="hy-lm-name">${this._escHtml(child.label || child.name)}</span>
                  </label>
                  ${childSwitch}
                </div>`;
            });

            childrenHTML = `
              <div class="hy-lm-children-wrapper ${parentDisabled ? 'is-disabled' : ''}" id="hy-lm-children-${layer.id}">
                ${childListHTML}
              </div>`;
          }

          const rootSwitch = layer.disabled ? `
            <span class="hy-lm-badge-planned" style="font-size:0.65rem;padding:2px 6px;border-radius:4px;background:rgba(148,163,184,0.18);color:#94a3b8;font-weight:600;letter-spacing:0.3px;" title="Dataset planned for future release">Planned</span>
          ` : `
            <label class="hy-lm-switch">
              <input type="checkbox"
                     id="hy-layer-switch-${layer.id}"
                     role="switch"
                     aria-checked="${ariaChecked}"
                     data-layer="${layer.id}"
                     class="hy-lm-switch-input"
                     ${checkedAttr}>
              <span class="hy-lm-slider-mark"></span>
            </label>
          `;

          groupItemsHTML += `
            <div class="hy-lm-item-container" data-layer-id="${layer.id}">
              <div class="hy-lm-item hy-lm-root-item ${hasChildren ? 'has-children' : ''} ${layer.disabled ? 'is-disabled' : ''}">
                <label class="hy-lm-switch-label" for="hy-layer-switch-${layer.id}">
                  <span class="hy-lm-icon">${layer.icon || layer.emoji || '📁'}</span>
                  <span class="hy-lm-name ${hasChildren ? 'is-parent-name' : ''}">${this._escHtml(layer.label || layer.name)}</span>
                  ${badge3D}
                </label>
                ${rootSwitch}
              </div>
              ${childrenHTML}
            </div>`;
        });

        // Group active count
        const activeInGroup = layersInGroup.filter(l => state ? state.isLayerEnabled(l.id) : l.defaultVisible).length;

        accordionHTML += `
          <div class="hy-lm-accordion-group" data-group="${group.id}">
            <button class="hy-lm-group-header" aria-expanded="true" data-group-target="${group.id}">
              <div class="hy-lm-group-title">
                <span class="hy-lm-group-icon">${group.icon || group.emoji || '📁'}</span>
                <span class="hy-lm-group-text">${this._escHtml(group.label || group.name)}</span>
              </div>
              <div class="hy-lm-group-meta">
                <span class="hy-lm-group-badge" id="hy-group-badge-${group.id}">${activeInGroup}/${layersInGroup.length}</span>
                <span class="hy-lm-chevron">⌄</span>
              </div>
            </button>
            <div class="hy-lm-group-content" id="hy-group-content-${group.id}">
              ${groupItemsHTML}
            </div>
          </div>`;
      });

      return `
        <!-- Drawer Header -->
        <div class="hy-lm-header">
          <div class="hy-lm-header-top">
            <div class="hy-lm-title-wrap">
              <h3 class="hy-lm-title">🗺️ Layer Manager</h3>
              <span class="hy-lm-total-badge" id="hy-lm-total-badge">0 Active</span>
            </div>
            <button class="hy-lm-close" id="hy-lm-close" aria-label="Close Layer Manager" title="Close (Esc)">✕</button>
          </div>

          <!-- Real-Time Search Bar -->
          <div class="hy-lm-search-container">
            <span class="hy-lm-search-icon">🔍</span>
            <input type="text"
                   id="hy-lm-search"
                   class="hy-lm-search-input"
                   placeholder="Search layers (temples, rivers, borders)..."
                   autocomplete="off"
                   aria-label="Search geographic layers">
            <button class="hy-lm-search-clear" id="hy-lm-search-clear" aria-label="Clear search" style="display: none;">✕</button>
          </div>

          <!-- Quick Action Toolbar -->
          <div class="hy-lm-toolbar">
            <button class="hy-lm-action-btn" id="hy-lm-btn-reset" title="Restore default layers">
              <span class="hy-lm-action-icon">🔄</span> Reset
            </button>
            <button class="hy-lm-action-btn" id="hy-lm-btn-show-all" title="Turn on all layers">
              <span class="hy-lm-action-icon">👁️</span> Show All
            </button>
            <button class="hy-lm-action-btn" id="hy-lm-btn-hide-all" title="Turn off all layers">
              <span class="hy-lm-action-icon">🚫</span> Hide All
            </button>
          </div>
        </div>

        <!-- Scrollable Layer Sections Body -->
        <div class="hy-lm-body" id="hy-lm-body" role="region" aria-label="Geographic Layer Groups">
          ${accordionHTML}
        </div>

        <!-- Drawer Footer -->
        <div class="hy-lm-footer">
          <div class="hy-lm-footer-info">
            <span class="hy-lm-dot-active"></span>
            <span class="hy-lm-footer-text">HiddenYatra GIS Layer Control</span>
          </div>
        </div>
      `;
    }

    /* ── Event Binding ─────────────────────────────── */

    /** @private */
    _bindEvents() {
      if (!this._panel) return;

      // 1. Close Button
      const closeBtn = this._panel.querySelector('#hy-lm-close');
      if (closeBtn) {
        closeBtn.addEventListener('click', () => this.closePanel());
      }

      // 2. Backdrop Click
      if (this._backdrop) {
        this._backdrop.addEventListener('click', () => this.closePanel());
      }

      // 3. Search Filter
      const searchInput = this._panel.querySelector('#hy-lm-search');
      const searchClear = this._panel.querySelector('#hy-lm-search-clear');

      if (searchInput) {
        searchInput.addEventListener('input', (e) => {
          this._searchQuery = (e.target.value || '').trim().toLowerCase();
          if (searchClear) {
            searchClear.style.display = this._searchQuery.length > 0 ? 'flex' : 'none';
          }
          this._filterLayers(this._searchQuery);
        });

        searchInput.addEventListener('keydown', (e) => {
          if (e.key === 'Escape') {
            if (this._searchQuery.length > 0) {
              searchInput.value = '';
              this._searchQuery = '';
              if (searchClear) searchClear.style.display = 'none';
              this._filterLayers('');
              e.stopPropagation();
            } else {
              this.closePanel();
            }
          }
        });
      }

      if (searchClear && searchInput) {
        searchClear.addEventListener('click', () => {
          searchInput.value = '';
          this._searchQuery = '';
          searchClear.style.display = 'none';
          this._filterLayers('');
          searchInput.focus();
        });
      }

      // 4. Quick Action Buttons
      const resetBtn = this._panel.querySelector('#hy-lm-btn-reset');
      if (resetBtn) {
        resetBtn.addEventListener('click', () => {
          if (root.HYMapState) {
            root.HYMapState.resetLayers();
          }
        });
      }

      const showAllBtn = this._panel.querySelector('#hy-lm-btn-show-all');
      if (showAllBtn) {
        showAllBtn.addEventListener('click', () => {
          if (root.HYMapState) {
            root.HYMapState.showAllLayers();
          }
        });
      }

      const hideAllBtn = this._panel.querySelector('#hy-lm-btn-hide-all');
      if (hideAllBtn) {
        hideAllBtn.addEventListener('click', () => {
          if (root.HYMapState) {
            root.HYMapState.hideAllLayers();
          }
        });
      }

      // 5. Accordion Group Toggles
      const groupHeaders = this._panel.querySelectorAll('.hy-lm-group-header');
      groupHeaders.forEach(hdr => {
        hdr.addEventListener('click', () => {
          const groupId = hdr.getAttribute('data-group-target');
          const content = this._panel.querySelector(`#hy-group-content-${groupId}`);
          const isExpanded = hdr.getAttribute('aria-expanded') === 'true';

          hdr.setAttribute('aria-expanded', isExpanded ? 'false' : 'true');
          if (content) {
            content.style.display = isExpanded ? 'none' : 'block';
          }
        });
      });

      // 6. Layer Switch Checkboxes
      const switches = this._panel.querySelectorAll('.hy-lm-switch-input');
      switches.forEach(sw => {
        sw.addEventListener('change', (e) => {
          const layerId = sw.getAttribute('data-layer');
          const visible = sw.checked;
          sw.setAttribute('aria-checked', visible ? 'true' : 'false');
          this._onLayerToggle(layerId, visible);
        });
      });

      // 7. Global Keyboard Accessibility (Escape to close)
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && this._panelOpen) {
          this.closePanel();
        }
      });
    }

    /* ── Reactive State Handling ───────────────────── */

    /** @private */
    _subscribeToState() {
      const state = root.HYMapState;
      if (!state) return;

      // 1. Single Layer Change
      const unsubLayer = state.on('layer', (data) => {
        this._syncLayerUI(data.layerId, data.visible, data.isParent);
        this._updateActiveBadge();
      });
      this._unsubs.push(unsubLayer);

      // 2. Reset Layers
      const unsubReset = state.on('layers:reset', () => {
        this._syncAllLayersUI();
        this._updateActiveBadge();
      });
      this._unsubs.push(unsubReset);

      // 3. Bulk Change (Hide All / Show All)
      const unsubBulk = state.on('layers:bulk', (data) => {
        this._syncAllLayersUI();
        this._updateActiveBadge();
      });
      this._unsubs.push(unsubBulk);
    }

    /**
     * Handle user toggling a layer in the UI.
     * Routes state change to HYMapState and active engines.
     * @private
     * @param {string} layerId
     * @param {boolean} visible
     */
    async _onLayerToggle(layerId, visible) {
      const state = root.HYMapState;
      const registry = root.HYLayerRegistry;

      // Update shared state
      if (state) {
        state.setLayerVisible(layerId, visible);
      }

      const def = registry ? registry.get(layerId) : null;
      if (!def || def.disabled) return;

      // Route to correct map engine
      const isGoogleEngine = (root.MAP_ENGINE === 'google' || Boolean(this.googleAdapter));

      if (isGoogleEngine && this.googleAdapter) {
        // Google Maps Engine
        try {
          await this.googleAdapter.toggleLayer(layerId, visible);
        } catch (e) {
          console.warn(`[MapControls] Google toggleLayer(${layerId}) handled:`, e.message || e);
        }
        return;
      }

      // Leaflet Engine
      if (def.engineSupport.includes('leaflet') && this.leafletAdapter) {
        try {
          await this.leafletAdapter.toggleLayer(layerId, visible);
        } catch (e) {
          console.warn(`[MapControls] Leaflet toggleLayer(${layerId}) handled:`, e.message || e);
        }
      }

      // MapLibre Engine
      if (def.engineSupport.includes('maplibre') && this.maplibreAdapter && this.maplibreAdapter.isLoaded()) {
        try {
          if (visible) {
            const data = await registry.fetchData(layerId);
            if (data) {
              this.maplibreAdapter.addGeoJSONLayer(layerId, data, def.style);
            }
          } else {
            this.maplibreAdapter.removeLayer(layerId);
          }
        } catch (e) {
          console.warn(`[MapControls] MapLibre toggleLayer(${layerId}) handled:`, e.message || e);
        }
      }
    }

    /**
     * Synchronize a specific layer checkbox and its child containers in the UI.
     * @private
     * @param {string} layerId
     * @param {boolean} visible
     * @param {boolean} isParent
     */
    _syncLayerUI(layerId, visible, isParent) {
      if (!this._panel) return;

      const sw = this._panel.querySelector(`#hy-layer-switch-${layerId}`);
      if (sw) {
        sw.checked = !!visible;
        sw.setAttribute('aria-checked', visible ? 'true' : 'false');
      }

      // If parent layer, enable/disable child items container
      const childrenWrapper = this._panel.querySelector(`#hy-lm-children-${layerId}`);
      if (childrenWrapper) {
        if (visible) {
          childrenWrapper.classList.remove('is-disabled');
        } else {
          childrenWrapper.classList.add('is-disabled');
        }
      }
    }

    /**
     * Re-sync all layer checkboxes in the DOM with HYMapState.
     * @private
     */
    _syncAllLayersUI() {
      if (!this._panel) return;

      const state = root.HYMapState;
      const registry = root.HYLayerRegistry;
      if (!state || !registry) return;

      registry.getAll().forEach(def => {
        const visible = state.isLayerVisible(def.id);
        const sw = this._panel.querySelector(`#hy-layer-switch-${def.id}`);
        if (sw) {
          sw.checked = visible;
          sw.setAttribute('aria-checked', visible ? 'true' : 'false');
        }

        const childrenWrapper = this._panel.querySelector(`#hy-lm-children-${def.id}`);
        if (childrenWrapper) {
          if (visible) {
            childrenWrapper.classList.remove('is-disabled');
          } else {
            childrenWrapper.classList.add('is-disabled');
          }
        }
      });
    }

    /**
     * Update active layer count badge in header and each group header.
     * @private
     */
    _updateActiveBadge() {
      if (!this._panel) return;

      const state = root.HYMapState;
      const registry = root.HYLayerRegistry;
      const layerGroups = root.HY_LAYER_GROUPS || root.HYLayerGroups || [];
      if (!state || !registry) return;

      const totalActive = state.getActiveLayerCount();
      const totalBadge = this._panel.querySelector('#hy-lm-total-badge');
      if (totalBadge) {
        totalBadge.textContent = `${totalActive} Active`;
      }

      // Also update button in top bar if present
      const topBtnBadge = document.getElementById('hy-layers-btn-badge');
      if (topBtnBadge) {
        topBtnBadge.textContent = totalActive > 0 ? String(totalActive) : '';
        topBtnBadge.style.display = totalActive > 0 ? 'inline-flex' : 'none';
      }

      // Update each group badge
      layerGroups.forEach(group => {
        const layers = registry.getByGroup(group.id);
        const active = layers.filter(l => state.isLayerEnabled(l.id)).length;
        const badge = this._panel.querySelector(`#hy-group-badge-${group.id}`);
        if (badge) {
          badge.textContent = `${active}/${layers.length}`;
        }
      });
    }

    /* ── Search Filtering ──────────────────────────── */

    /**
     * Filter layers in real-time based on query string.
     * @private
     * @param {string} query
     */
    _filterLayers(query) {
      if (!this._panel) return;

      const groups = this._panel.querySelectorAll('.hy-lm-accordion-group');

      groups.forEach(groupEl => {
        const groupId = groupEl.getAttribute('data-group');
        const header = groupEl.querySelector('.hy-lm-group-header');
        const content = groupEl.querySelector('.hy-lm-group-content');
        const itemContainers = groupEl.querySelectorAll('.hy-lm-item-container');

        let groupHasMatch = false;

        itemContainers.forEach(container => {
          const rootItem = container.querySelector('.hy-lm-root-item');
          const rootNameEl = rootItem ? rootItem.querySelector('.hy-lm-name') : null;
          const rootText = rootNameEl ? rootNameEl.textContent.toLowerCase() : '';

          const childItems = container.querySelectorAll('.hy-lm-child-item');
          let childMatched = false;

          childItems.forEach(child => {
            const childNameEl = child.querySelector('.hy-lm-name');
            const childText = childNameEl ? childNameEl.textContent.toLowerCase() : '';

            if (!query || childText.includes(query)) {
              child.style.display = 'flex';
              childMatched = true;
            } else {
              child.style.display = 'none';
            }
          });

          const rootMatched = !query || rootText.includes(query) || childMatched;

          if (rootMatched) {
            container.style.display = 'block';
            groupHasMatch = true;
          } else {
            container.style.display = 'none';
          }
        });

        // Show/hide entire group
        if (!query || groupHasMatch) {
          groupEl.style.display = 'block';
          if (query && groupHasMatch) {
            // Auto-expand matching groups
            if (header) header.setAttribute('aria-expanded', 'true');
            if (content) content.style.display = 'block';
          }
        } else {
          groupEl.style.display = 'none';
        }
      });
    }

    /* ── Panel Visibility ──────────────────────────── */

    openPanel() {
      if (this._panel) {
        this._panel.classList.add('open');
        this._panelOpen = true;
      }
      if (this._backdrop) {
        this._backdrop.classList.add('open');
      }

      // Focus the search input for seamless keyboard search
      const searchInput = this._panel ? this._panel.querySelector('#hy-lm-search') : null;
      if (searchInput) {
        setTimeout(() => searchInput.focus(), 150);
      }
    }

    closePanel() {
      if (this._panel) {
        this._panel.classList.remove('open');
        this._panelOpen = false;
      }
      if (this._backdrop) {
        this._backdrop.classList.remove('open');
      }
    }

    togglePanel() {
      if (this._panelOpen) {
        this.closePanel();
      } else {
        this.openPanel();
      }
    }

    /* ── Utility ───────────────────────────────────── */

    /** @private */
    _escHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    }

    /* ── Cleanup ───────────────────────────────────── */

    destroy() {
      this._unsubs.forEach(unsub => {
        try { unsub(); } catch (e) {}
      });
      this._unsubs = [];

      if (this._panel && this._panel.parentElement) {
        this._panel.parentElement.removeChild(this._panel);
      }
      if (this._backdrop && this._backdrop.parentElement) {
        this._backdrop.parentElement.removeChild(this._backdrop);
      }
      this._panel = null;
      this._backdrop = null;
    }
  }

  // Exports
  root.HYMapControls = MapControls;

})(window);

// Category SVG Marker Definitions
window.HY_CATEGORY_MARKERS = {
  heritage: { color: '#e11d48', icon: '🏛️' },
  nature: { color: '#059669', icon: '🌿' },
  spiritual: { color: '#d97706', icon: '🕉️' },
  food: { color: '#ea580c', icon: '🍲' },
  default: { color: '#6366f1', icon: '📍' }
};

window.HY_GET_MARKER_STYLE = function(category) {
  const cat = (category || '').toLowerCase();
  return window.HY_CATEGORY_MARKERS[cat] || window.HY_CATEGORY_MARKERS.default;
};
