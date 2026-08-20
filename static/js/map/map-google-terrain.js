/* ═══════════════════════════════════════════════════════════════════
   HiddenYatra — Google Custom 3D Terrain Manager (Phase G4B-4 Hardened)
   Orchestrates google.maps.WebGLOverlayView, Three.js shared WebGL
   rendering, viewport-driven multi-chunk terrain streaming, LOD hysteresis,
   stale-response rejection, zero-seam precision, and performance diagnostics.
   ═══════════════════════════════════════════════════════════════════ */

(function (root) {
  'use strict';

  /**
   * Explicit Chunk Lifecycle States
   */
  const CHUNK_STATE = {
    UNLOADED: 'UNLOADED',
    LOADING: 'LOADING',
    CPU_READY: 'CPU_READY',
    GPU_READY: 'GPU_READY',
    VISIBLE: 'VISIBLE',
    DISPOSING: 'DISPOSING',
    DISPOSED: 'DISPOSED',
  };

  class GoogleTerrainManager {
    /**
     * @param {google.maps.Map} googleMap
     * @param {Object} [options]
     * @param {number} [options.exaggeration=1.0]
     */
    constructor(googleMap, options = {}) {
      if (!googleMap) throw new Error('[HYGoogleTerrainManager] Missing Google Maps instance');

      /** @type {google.maps.Map} */
      this.map = googleMap;

      /** @type {number} Vertical terrain exaggeration (1.0, 1.5, 2.0, 2.5) */
      this._exaggeration = options.exaggeration !== undefined ? options.exaggeration : 1.0;

      /** @type {boolean} Whether terrain overlay is currently active */
      this._enabled = false;

      /** @type {boolean} Track if WebGL context was lost */
      this._contextLost = false;

      /** @type {google.maps.WebGLOverlayView|null} */
      this.overlay = null;

      /** @type {THREE.Scene|null} */
      this.scene = null;

      /** @type {THREE.PerspectiveCamera|null} */
      this.camera = null;

      /** @type {THREE.WebGLRenderer|null} */
      this.renderer = null;

      /** @type {THREE.Group|null} */
      this.terrainGroup = null;

      /** @type {THREE.Mesh|null} Legacy single-tile mesh for backward compatibility */
      this.legacyRajgirMesh = null;

      /** @type {THREE.DirectionalLight|null} */
      this.sunLight = null;

      /** @type {THREE.AmbientLight|null} */
      this.ambientLight = null;

      /** @type {Map<string, THREE.Mesh>} Active terrain chunk meshes by tileKey */
      this.activeChunks = new Map();

      /** @type {Map<string, string>} Chunk lifecycle status */
      this.chunkStatus = new Map();

      /** @type {number|null} Current active LOD level */
      this.currentLOD = null;

      /** @type {number} Monotonic request generation for stale response rejection */
      this._requestGeneration = 0;

      /** @type {google.maps.MapsEventListener|null} */
      this._cameraIdleListener = null;

      /** @type {google.maps.MapsEventListener|null} */
      this._cameraBoundsListener = null;

      /** @type {HYGoogleTerrainLoader} */
      const LoaderClass = root.HYGoogleTerrainLoader || (typeof HYGoogleTerrainLoader !== 'undefined' ? HYGoogleTerrainLoader : null);
      if (LoaderClass) {
        this.loader = new LoaderClass({
          onTileEvicted: (tileKey, tileData) => this._onTileEvicted(tileKey, tileData),
        });
      } else {
        this.loader = null;
      }

      this._initWebGLOverlay();
      this._exposeDiagnostics();
    }

    /**
     * Check if client browser and map support WebGL Vector overlays.
     * @returns {boolean}
     */
    static isWebGLSupported() {
      try {
        const canvas = document.createElement('canvas');
        return Boolean(window.WebGLRenderingContext && (canvas.getContext('webgl') || canvas.getContext('experimental-webgl')));
      } catch (e) {
        return false;
      }
    }

    /**
     * Expose lightweight performance diagnostics for debugging/testing.
     * @private
     */
    _exposeDiagnostics() {
      if (typeof window !== 'undefined') {
        window.__HY_TERRAIN_DIAGNOSTICS__ = {
          get visibleChunksCount() {
            return this.parent ? this.parent.activeChunks.size : 0;
          },
          get activeGpuChunksCount() {
            return this.parent ? this.parent.activeChunks.size : 0;
          },
          get currentLOD() {
            return this.parent ? this.parent.currentLOD : null;
          },
          get cameraZoom() {
            return this.parent && this.parent.map ? this.parent.map.getZoom() : null;
          },
          get cacheHits() {
            return this.parent && this.parent.loader ? this.parent.loader.cache.stats.hits : 0;
          },
          get cacheMisses() {
            return this.parent && this.parent.loader ? this.parent.loader.cache.stats.misses : 0;
          },
          get workerDecodeTimeMs() {
            return this.parent && this.parent.loader ? this.parent.loader.diagnostics.workerDecodeTimeMs : 0;
          },
          parent: this,
        };
      }
    }

    /**
     * Initialize the WebGLOverlayView instance.
     * @private
     */
    _initWebGLOverlay() {
      if (typeof google === 'undefined' || !google.maps || !google.maps.WebGLOverlayView) {
        console.warn('[HYGoogleTerrainManager] google.maps.WebGLOverlayView not available');
        return;
      }

      this.overlay = new google.maps.WebGLOverlayView();

      // ── Lifecycle Hook 1: onAdd ──
      this.overlay.onAdd = () => {
        if (typeof THREE === 'undefined') {
          console.warn('[HYGoogleTerrainManager] Three.js not loaded, cannot build 3D scene');
          return;
        }

        this.scene = new THREE.Scene();
        this.scene.matrixAutoUpdate = false;

        this.camera = new THREE.PerspectiveCamera();
        this.camera.matrixAutoUpdate = false;

        // Container group for all chunk meshes
        this.terrainGroup = new THREE.Group();
        this.terrainGroup.matrixAutoUpdate = false;
        this.scene.add(this.terrainGroup);

        // Ambient lighting for soft valley fill
        this.ambientLight = new THREE.AmbientLight(0xffffff, 0.70);
        this.scene.add(this.ambientLight);

        // Directional Sun lighting (North-West azimuth 315°, 45° altitude)
        this.sunLight = new THREE.DirectionalLight(0xfffaed, 0.85);
        this.sunLight.position.set(-5000, 5000, 8000);
        this.scene.add(this.sunLight);

        // Initialize loader manifest
        if (this.loader) {
          this.loader.init().then(() => {
            this._onCameraChange();
          }).catch(err => {
            console.warn('[HYGoogleTerrainManager] Loader manifest init error:', err);
          });
        }

        // Camera movement listeners for viewport-driven streaming
        this._bindCameraListeners();

        console.log('[HYGoogleTerrainManager] WebGLOverlayView onAdd: 3D scene initialized');
      };

      // ── Lifecycle Hook 2: onContextRestored ──
      this.overlay.onContextRestored = ({ gl }) => {
        if (typeof THREE === 'undefined') return;

        this.renderer = new THREE.WebGLRenderer({
          context: gl,
          autoClear: false,
          antialias: true,
        });
        this.renderer.autoClear = false;
        this._contextLost = false;

        if (this._enabled && this.overlay) {
          this.overlay.requestRedraw();
        }

        console.log('[HYGoogleTerrainManager] WebGLOverlayView onContextRestored: Shared renderer ready');
      };

      // ── Lifecycle Hook 3: onDraw ──
      this.overlay.onDraw = ({ gl, transformer }) => {
        if (!this._enabled || this._contextLost || !this.renderer || !this.scene || !this.camera) {
          return;
        }

        // Synchronize Three.js camera projection matrix from Google Vector Camera
        const camParams = transformer.getCameraParams();
        if (camParams && camParams.projectionMatrix) {
          this.camera.projectionMatrix.fromArray(camParams.projectionMatrix);
          if (this.camera.projectionMatrixInverse) {
            this.camera.projectionMatrixInverse.copy(this.camera.projectionMatrix).invert();
          }
        }

        // Position and orient every active terrain chunk using its exact WGS84 anchor
        for (const [tileKey, mesh] of this.activeChunks.entries()) {
          if (mesh && mesh.userData && mesh.userData.centerLat !== undefined) {
            const anchor = {
              lat: mesh.userData.centerLat,
              lng: mesh.userData.centerLng,
              altitude: 0,
            };
            const matrix = transformer.fromLatLngAltitude(anchor);
            mesh.matrix.fromArray(matrix);
            mesh.matrixWorldNeedsUpdate = true;
          }
        }

        // Enable standard WebGL depth testing with Google vector basemap
        gl.enable(gl.DEPTH_TEST);
        gl.depthFunc(gl.LEQUAL);

        // Reset Three.js internal state to prevent conflicts with Google basemap
        this.renderer.resetState();

        // Render terrain scene
        this.renderer.render(this.scene, this.camera);
      };

      // ── Lifecycle Hook 4: onContextLost ──
      this.overlay.onContextLost = () => {
        this._contextLost = true;
        console.warn('[HYGoogleTerrainManager] WebGL Context Lost: Pausing terrain rendering');
      };

      // ── Lifecycle Hook 5: onRemove ──
      this.overlay.onRemove = () => {
        this._unbindCameraListeners();
        this._disposeScene();
        console.log('[HYGoogleTerrainManager] WebGLOverlayView onRemove: 3D scene disposed');
      };
    }

    /**
     * Bind camera change listeners to Google Maps instance.
     * @private
     */
    _bindCameraListeners() {
      if (!this.map || this._cameraIdleListener) return;

      this._cameraIdleListener = google.maps.event.addListener(this.map, 'idle', () => {
        if (this._enabled) {
          this._onCameraChange();
        }
      });

      this._cameraBoundsListener = google.maps.event.addListener(this.map, 'bounds_changed', () => {
        if (this._enabled) {
          this._onCameraChange();
        }
      });
    }

    /**
     * Unbind camera change listeners.
     * @private
     */
    _unbindCameraListeners() {
      if (this._cameraIdleListener) {
        google.maps.event.removeListener(this._cameraIdleListener);
        this._cameraIdleListener = null;
      }
      if (this._cameraBoundsListener) {
        google.maps.event.removeListener(this._cameraBoundsListener);
        this._cameraBoundsListener = null;
      }
    }

    /**
     * Triggered on Google camera movement to calculate and stream visible terrain chunks.
     * @private
     */
    _onCameraChange() {
      if (!this._enabled || !this.loader || !this.map) return;

      const bounds = this.map.getBounds();
      if (!bounds) return;

      const ne = bounds.getNorthEast();
      const sw = bounds.getSouthWest();
      const viewportBounds = {
        north: ne.lat(),
        south: sw.lat(),
        east: ne.lng(),
        west: sw.lng(),
      };

      const zoom = this.map.getZoom() || 11;
      const { visibleKeys, prefetchKeys, targetLOD } = this.loader.calculateViewportTiles(viewportBounds, zoom, this.currentLOD);
      this.currentLOD = targetLOD;

      const currentGen = ++this._requestGeneration;
      const requiredSet = new Set([...visibleKeys, ...prefetchKeys]);
      const visibleSet = new Set(visibleKeys);
      const protectedKeys = new Set(this.activeChunks.keys());

      // 1. Prune chunks from previous LODs to avoid overlapping duplicate coverage
      for (const [tileKey, mesh] of this.activeChunks.entries()) {
        const chunkLOD = parseInt(tileKey.split('/')[0], 10);
        if (chunkLOD !== targetLOD && !requiredSet.has(tileKey)) {
          this._disposeChunk(tileKey);
        }
      }

      // 2. Load missing visible chunks
      for (const tileKey of visibleKeys) {
        if (!this.activeChunks.has(tileKey) && this.chunkStatus.get(tileKey) !== CHUNK_STATE.LOADING) {
          this.chunkStatus.set(tileKey, CHUNK_STATE.LOADING);

          this.loader.loadTile(tileKey, protectedKeys)
            .then((tileData) => {
              // Stale response rejection: verify overlay is still enabled and tile is still required
              if (!this._enabled || !this.scene || !this.terrainGroup) {
                this.chunkStatus.set(tileKey, CHUNK_STATE.DISPOSED);
                return;
              }

              const latestBounds = this.map.getBounds();
              if (latestBounds) {
                const lne = latestBounds.getNorthEast();
                const lsw = latestBounds.getSouthWest();
                const curView = { north: lne.lat(), south: lsw.lat(), east: lne.lng(), west: lsw.lng() };
                const curCalc = this.loader.calculateViewportTiles(curView, this.map.getZoom() || 11, this.currentLOD);
                const curReq = new Set([...curCalc.visibleKeys, ...curCalc.prefetchKeys]);

                if (!curReq.has(tileKey)) {
                  this.chunkStatus.set(tileKey, CHUNK_STATE.DISPOSED);
                  return;
                }
              }

              this.chunkStatus.set(tileKey, CHUNK_STATE.CPU_READY);

              // Avoid duplicate mesh instantiation
              if (this.activeChunks.has(tileKey)) {
                return;
              }

              // Create chunk mesh via MeshFactory
              if (root.HYGoogleTerrainMeshFactory && root.HYGoogleTerrainMeshFactory.createTileTerrainMesh) {
                this.chunkStatus.set(tileKey, CHUNK_STATE.GPU_READY);
                const mesh = root.HYGoogleTerrainMeshFactory.createTileTerrainMesh(tileData, {
                  exaggeration: this._exaggeration,
                });

                this.activeChunks.set(tileKey, mesh);
                this.terrainGroup.add(mesh);
                this.chunkStatus.set(tileKey, CHUNK_STATE.VISIBLE);

                if (this.overlay) {
                  this.overlay.requestRedraw();
                }
              }
            })
            .catch((err) => {
              this.chunkStatus.delete(tileKey);
              console.warn(`[HYGoogleTerrainManager] Failed loading chunk ${tileKey}:`, err.message || err);
            });
        }
      }

      // 3. Prefetch 1-ring buffer off-thread into LRU cache
      for (const tileKey of prefetchKeys) {
        if (!this.loader.cache.has(tileKey)) {
          this.loader.loadTile(tileKey, protectedKeys).catch(() => {});
        }
      }

      // 4. Evict stale meshes that left the viewport & prefetch buffer
      for (const [tileKey, mesh] of this.activeChunks.entries()) {
        if (!requiredSet.has(tileKey)) {
          this._disposeChunk(tileKey);
        }
      }
    }

    /**
     * Disposes a specific chunk mesh from scene and memory.
     * @private
     * @param {string} tileKey
     */
    _disposeChunk(tileKey) {
      if (this.activeChunks.has(tileKey)) {
        this.chunkStatus.set(tileKey, CHUNK_STATE.DISPOSING);
        const mesh = this.activeChunks.get(tileKey);
        if (this.terrainGroup) {
          this.terrainGroup.remove(mesh);
        }
        if (mesh.geometry) mesh.geometry.dispose();
        if (mesh.material) {
          if (Array.isArray(mesh.material)) {
            mesh.material.forEach((m) => m.dispose());
          } else {
            mesh.material.dispose();
          }
        }
        this.activeChunks.delete(tileKey);
        this.chunkStatus.set(tileKey, CHUNK_STATE.DISPOSED);
      }
    }

    /**
     * Callback from LRU Cache when a tile is evicted from cache.
     * @private
     * @param {string} tileKey
     * @param {Object} tileData
     */
    _onTileEvicted(tileKey, tileData) {
      this._disposeChunk(tileKey);
    }

    /* ── Controls & Public Methods ─────────────────── */

    /**
     * Enable 3D terrain overlay on the Google Map.
     */
    enable() {
      if (!this.overlay) return;
      this._enabled = true;
      this.overlay.setMap(this.map);
      this._bindCameraListeners();
      this._onCameraChange();
      if (this.overlay) this.overlay.requestRedraw();
      console.log('[HYGoogleTerrainManager] 3D Terrain enabled');
    }

    /**
     * Disable 3D terrain overlay from the Google Map.
     */
    disable() {
      if (!this.overlay) return;
      this._enabled = false;
      this._unbindCameraListeners();
      this.overlay.setMap(null);

      // Clear all active chunk meshes
      for (const tileKey of Array.from(this.activeChunks.keys())) {
        this._disposeChunk(tileKey);
      }

      console.log('[HYGoogleTerrainManager] 3D Terrain disabled');
    }

    /**
     * Set terrain vertical exaggeration factor across all active chunks.
     * @param {number} factor - e.g. 1.0, 1.5, 2.0, 2.5
     */
    setExaggeration(factor) {
      this._exaggeration = Math.max(0.5, Math.min(5.0, factor));

      // Update all active chunk meshes
      if (root.HYGoogleTerrainMeshFactory && root.HYGoogleTerrainMeshFactory.updateTileExaggeration) {
        for (const mesh of this.activeChunks.values()) {
          root.HYGoogleTerrainMeshFactory.updateTileExaggeration(mesh, this._exaggeration);
        }
      }

      // Update legacy mesh if present
      if (this.legacyRajgirMesh && root.HYGoogleTerrainMeshFactory) {
        root.HYGoogleTerrainMeshFactory.updateExaggeration(this.legacyRajgirMesh, this._exaggeration);
      }

      if (this.overlay && this._enabled) {
        this.overlay.requestRedraw();
      }
    }

    /**
     * Get current vertical exaggeration factor.
     * @returns {number}
     */
    getExaggeration() {
      return this._exaggeration;
    }

    /**
     * Check runtime rendering type of Google Map.
     * @returns {string} e.g. 'VECTOR' or 'RASTER'
     */
    getRenderingType() {
      if (this.map && typeof this.map.getRenderingType === 'function') {
        return this.map.getRenderingType();
      }
      return 'VECTOR';
    }

    /**
     * Get actual current camera tilt in degrees.
     * @returns {number}
     */
    getCurrentTilt() {
      if (this.map && typeof this.map.getTilt === 'function') {
        return this.map.getTilt();
      }
      return 0;
    }

    /**
     * Get actual current camera heading in degrees.
     * @returns {number}
     */
    getCurrentHeading() {
      if (this.map && typeof this.map.getHeading === 'function') {
        return this.map.getHeading();
      }
      return 0;
    }

    /**
     * Check if terrain is currently enabled.
     * @returns {boolean}
     */
    isEnabled() {
      return this._enabled;
    }

    /**
     * Fly and focus camera onto Rajgir Hills with optimal 3D pitch and heading.
     * @param {number} [durationSec=1.5]
     */
    focusRajgir(durationSec = 1.5) {
      if (this.map.moveCamera) {
        this.map.moveCamera({
          center: { lat: 25.00, lng: 85.43 },
          zoom: 12,
          tilt: 50,
          heading: 330,
        });
      } else {
        this.map.panTo({ lat: 25.00, lng: 85.43 });
        this.map.setZoom(12);
        if (this.map.setTilt) this.map.setTilt(50);
        if (this.map.setHeading) this.map.setHeading(330);
      }
    }

    /* ── Cleanup ───────────────────────────────────── */

    /** @private */
    _disposeScene() {
      for (const tileKey of Array.from(this.activeChunks.keys())) {
        this._disposeChunk(tileKey);
      }

      if (this.legacyRajgirMesh) {
        if (this.legacyRajgirMesh.geometry) this.legacyRajgirMesh.geometry.dispose();
        if (this.legacyRajgirMesh.material) {
          if (Array.isArray(this.legacyRajgirMesh.material)) {
            this.legacyRajgirMesh.material.forEach((m) => m.dispose());
          } else {
            this.legacyRajgirMesh.material.dispose();
          }
        }
        this.legacyRajgirMesh = null;
      }

      this.terrainGroup = null;
      this.scene = null;
      this.camera = null;
      this.renderer = null;
      this.ambientLight = null;
      this.sunLight = null;
    }

    /**
     * Full teardown of terrain manager.
     */
    destroy() {
      this.disable();
      if (this.loader) {
        this.loader.destroy();
        this.loader = null;
      }
      if (this.overlay) {
        this.overlay.setMap(null);
        this.overlay = null;
      }
      this._disposeScene();
    }
  }

  root.HYGoogleTerrainManager = GoogleTerrainManager;

})(window);
