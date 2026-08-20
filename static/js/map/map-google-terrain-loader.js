/**
 * HiddenYatra — Google Maps WebGL 3D Terrain Production Loader (Phase G4B-4 Hardened)
 * High-performance viewport tile selector, LOD coordinator with hysteresis, in-flight
 * request deduplicator, and LRU memory cache manager for chunked 3D terrain meshes.
 */
(function (global) {
    'use strict';

    const DEFAULT_MANIFEST_URL = '/static/data/terrain/bihar/manifest.json';
    const DEFAULT_WORKER_URL = '/static/js/map/map-google-terrain-worker.js';
    const DEFAULT_MAX_CACHE_SIZE = 32;
    const CELL_SIZE = 64;
    const VERTEX_GRID_SIZE = 65;

    /**
     * Converts WGS84 Lat/Lng to Web Mercator tile index (X, Y) at zoom Z.
     * @param {number} lat
     * @param {number} lng
     * @param {number} z
     * @returns {{ x: number, y: number }}
     */
    function latLngToTileXY(lat, lng, z) {
        const n = Math.pow(2, z);
        const x = Math.floor(((lng + 180.0) / 360.0) * n);
        const latRad = (lat * Math.PI) / 180.0;
        const y = Math.floor(((1.0 - Math.asinh(Math.tan(latRad)) / Math.PI) / 2.0) * n);
        return { x: Math.max(0, Math.min(n - 1, x)), y: Math.max(0, Math.min(n - 1, y)) };
    }

    /**
     * Converts vertex grid coordinate (r, c) within tile (z, x, y) to exact WGS84 Lat/Lng.
     * r: 0 (North) to 64 (South)
     * c: 0 (West) to 64 (East)
     * @param {number} z
     * @param {number} x
     * @param {number} y
     * @param {number} r
     * @param {number} c
     * @returns {{ lat: number, lng: number }}
     */
    function tilePointToLatLng(z, x, y, r, c) {
        const n = Math.pow(2, z);
        const xNorm = x + c / CELL_SIZE;
        const yNorm = y + r / CELL_SIZE;

        const lng = (xNorm / n) * 360.0 - 180.0;
        const latRad = Math.atan(Math.sinh(Math.PI * (1.0 - (2.0 * yNorm) / n)));
        const lat = (latRad * 180.0) / Math.PI;
        return { lat, lng };
    }

    /**
     * Computes the bounding box of a tile in WGS84 coordinates.
     * @param {number} z
     * @param {number} x
     * @param {number} y
     * @returns {{ north: number, south: number, east: number, west: number }}
     */
    function getTileBounds(z, x, y) {
        const nw = tilePointToLatLng(z, x, y, 0, 0);
        const se = tilePointToLatLng(z, x, y, CELL_SIZE, CELL_SIZE);
        return {
            north: nw.lat,
            west: nw.lng,
            south: se.lat,
            east: se.lng,
        };
    }

    /**
     * Maps camera zoom to target LOD with hysteresis to prevent thrashing near thresholds.
     * @param {number} cameraZoom
     * @param {number|null} currentLOD
     * @param {Array<number>} availableLODs
     * @returns {number}
     */
    function selectTargetLODWithHysteresis(cameraZoom, currentLOD = null, availableLODs = [9, 10, 11]) {
        if (!availableLODs || availableLODs.length === 0) return 11;
        const sorted = [...availableLODs].sort((a, b) => a - b);

        if (currentLOD === 9) {
            if (cameraZoom >= 9.75) return sorted.includes(10) ? 10 : sorted[sorted.length - 1];
            return 9;
        } else if (currentLOD === 10) {
            if (cameraZoom < 9.25 && sorted.includes(9)) return 9;
            if (cameraZoom >= 10.75 && sorted.includes(11)) return 11;
            return 10;
        } else if (currentLOD === 11) {
            if (cameraZoom < 10.25 && sorted.includes(10)) return 10;
            return 11;
        }

        // Default direct selection if currentLOD is not set
        if (cameraZoom <= 9.5) {
            return sorted.includes(9) ? 9 : sorted[0];
        } else if (cameraZoom <= 10.5) {
            return sorted.includes(10) ? 10 : sorted[0];
        } else {
            return sorted.includes(11) ? 11 : sorted[sorted.length - 1];
        }
    }

    /**
     * Standard non-hysteresis LOD selector for initial calculation.
     */
    function selectTargetLOD(cameraZoom, availableLODs = [9, 10, 11]) {
        return selectTargetLODWithHysteresis(cameraZoom, null, availableLODs);
    }

    /**
     * Least-Recently-Used (LRU) Memory Cache for Decoded Terrain Tiles.
     */
    class TerrainLRUCache {
        constructor(maxSize = DEFAULT_MAX_CACHE_SIZE, onEvictCallback = null) {
            this.maxSize = maxSize;
            this.cache = new Map();
            this.onEvict = onEvictCallback;
            this.stats = {
                hits: 0,
                misses: 0,
                evictions: 0,
            };
        }

        get(key) {
            if (!this.cache.has(key)) {
                this.stats.misses++;
                return null;
            }
            this.stats.hits++;
            const value = this.cache.get(key);
            this.cache.delete(key);
            this.cache.set(key, value);
            return value;
        }

        has(key) {
            return this.cache.has(key);
        }

        set(key, value, protectedKeys = new Set()) {
            if (this.cache.has(key)) {
                this.cache.delete(key);
            } else if (this.cache.size >= this.maxSize) {
                this._evictOldest(protectedKeys);
            }
            this.cache.set(key, value);
        }

        _evictOldest(protectedKeys) {
            for (const [k, v] of this.cache.entries()) {
                if (!protectedKeys.has(k)) {
                    this.cache.delete(k);
                    this.stats.evictions++;
                    if (typeof this.onEvict === 'function') {
                        this.onEvict(k, v);
                    }
                    break;
                }
            }
        }

        clear() {
            if (typeof this.onEvict === 'function') {
                for (const [k, v] of this.cache.entries()) {
                    this.onEvict(k, v);
                }
            }
            this.cache.clear();
        }

        get size() {
            return this.cache.size;
        }
    }

    /**
     * Main Production Terrain Loader.
     */
    class HYGoogleTerrainLoader {
        constructor(options = {}) {
            this.manifestUrl = options.manifestUrl || DEFAULT_MANIFEST_URL;
            this.workerUrl = options.workerUrl || DEFAULT_WORKER_URL;
            this.maxCacheSize = options.maxCacheSize || DEFAULT_MAX_CACHE_SIZE;
            this.onTileEvicted = options.onTileEvicted || null;

            this.manifest = null;
            this.availableTiles = new Set();
            this.availableLODs = [9, 10, 11];

            this.cache = new TerrainLRUCache(this.maxCacheSize, (key, tileData) => {
                if (typeof this.onTileEvicted === 'function') {
                    this.onTileEvicted(key, tileData);
                }
            });

            this._inFlightRequests = new Map();
            this._worker = null;
            this._workerMsgId = 0;
            this._workerCallbacks = new Map();
            this._isInitialized = false;

            this.diagnostics = {
                workerDecodeTimeMs: 0,
                lastLoadedTileKey: null,
                failedTiles: new Set(),
            };

            this._initWorker();
        }

        /**
         * Initializes Web Worker instance.
         */
        _initWorker() {
            if (typeof Worker !== 'undefined' && typeof window !== 'undefined') {
                try {
                    this._worker = new Worker(this.workerUrl);
                    this._worker.onmessage = (e) => this._handleWorkerMessage(e);
                    this._worker.onerror = (err) => {
                        console.warn("[HYTerrainLoader] Worker error, falling back to main-thread decode:", err);
                        this._worker = null;
                    };
                } catch (err) {
                    console.warn("[HYTerrainLoader] Worker initialization failed:", err);
                    this._worker = null;
                }
            }
        }

        /**
         * Dispatches worker message callbacks.
         */
        _handleWorkerMessage(e) {
            const { msgId, success, tileKey, header, elevations, indices, error } = e.data;
            if (this._workerCallbacks.has(msgId)) {
                const { resolve, reject, startTime } = this._workerCallbacks.get(msgId);
                this._workerCallbacks.delete(msgId);

                if (success) {
                    this.diagnostics.workerDecodeTimeMs = performance.now() - startTime;
                    this.diagnostics.lastLoadedTileKey = tileKey;
                    resolve({ header, elevations, indices, tileKey });
                } else {
                    this.diagnostics.failedTiles.add(tileKey);
                    reject(new Error(error || `Failed decoding tile ${tileKey}`));
                }
            }
        }

        /**
         * Loads and parses the authentic DEM manifest.json.
         */
        async init() {
            if (this._isInitialized) return this.manifest;

            try {
                const response = await fetch(this.manifestUrl);
                if (!response.ok) {
                    throw new Error(`Failed to load terrain manifest: HTTP ${response.status}`);
                }
                this.manifest = await response.json();

                if (this.manifest && this.manifest.tiles) {
                    this.availableTiles = new Set(Object.keys(this.manifest.tiles));
                }

                if (this.manifest && this.manifest.lod) {
                    this.availableLODs = Object.keys(this.manifest.lod)
                        .map((k) => parseInt(k.replace('z', ''), 10))
                        .filter((n) => !isNaN(n));
                }

                this._isInitialized = true;
                return this.manifest;
            } catch (err) {
                console.error("[HYTerrainLoader] Manifest initialization failed:", err);
                throw err;
            }
        }

        /**
         * Computes required tile keys with hysteresis-supported LOD mapping.
         * @param {{ north: number, south: number, east: number, west: number }} viewportBounds
         * @param {number} cameraZoom
         * @param {number|null} currentLOD
         * @returns {{ visibleKeys: Array<string>, prefetchKeys: Array<string>, targetLOD: number }}
         */
        calculateViewportTiles(viewportBounds, cameraZoom, currentLOD = null) {
            const targetLOD = selectTargetLODWithHysteresis(cameraZoom, currentLOD, this.availableLODs);
            const { north, south, east, west } = viewportBounds;

            const nw = latLngToTileXY(north, west, targetLOD);
            const se = latLngToTileXY(south, east, targetLOD);

            const minX = Math.min(nw.x, se.x);
            const maxX = Math.max(nw.x, se.x);
            const minY = Math.min(nw.y, se.y);
            const maxY = Math.max(nw.y, se.y);

            const visibleKeys = [];
            const prefetchKeys = [];
            const visibleSet = new Set();

            // 1. Visible core viewport
            for (let x = minX; x <= maxX; x++) {
                for (let y = minY; y <= maxY; y++) {
                    const key = `${targetLOD}/${x}/${y}`;
                    if (this.availableTiles.has(key)) {
                        visibleKeys.push(key);
                        visibleSet.add(key);
                    }
                }
            }

            // 2. 1-ring prefetch buffer
            for (let x = minX - 1; x <= maxX + 1; x++) {
                for (let y = minY - 1; y <= maxY + 1; y++) {
                    const key = `${targetLOD}/${x}/${y}`;
                    if (!visibleSet.has(key) && this.availableTiles.has(key)) {
                        prefetchKeys.push(key);
                    }
                }
            }

            return { visibleKeys, prefetchKeys, targetLOD };
        }

        /**
         * Fetches and decodes a single .hyelev tile (with LRU caching and in-flight deduplication).
         * @param {string} tileKey (e.g. "11/1507/878")
         * @param {Set<string>} [protectedKeys]
         * @returns {Promise<Object>}
         */
        async loadTile(tileKey, protectedKeys = new Set()) {
            // 1. Check LRU Cache
            if (this.cache.has(tileKey)) {
                return this.cache.get(tileKey);
            }

            // 2. Deduplicate in-flight requests
            if (this._inFlightRequests.has(tileKey)) {
                return this._inFlightRequests.get(tileKey);
            }

            // 3. Dispatch new load promise
            const loadPromise = this._fetchAndDecodeTile(tileKey)
                .then((tileData) => {
                    this.cache.set(tileKey, tileData, protectedKeys);
                    this._inFlightRequests.delete(tileKey);
                    return tileData;
                })
                .catch((err) => {
                    this._inFlightRequests.delete(tileKey);
                    throw err;
                });

            this._inFlightRequests.set(tileKey, loadPromise);
            return loadPromise;
        }

        /**
         * Internal fetch and decode implementation (Worker or Main-Thread fallback).
         */
        async _fetchAndDecodeTile(tileKey) {
            if (!this.manifest || !this.manifest.tiles || !this.manifest.tiles[tileKey]) {
                throw new Error(`Tile ${tileKey} is not available in manifest`);
            }

            const meta = this.manifest.tiles[tileKey];
            const tileUrl = `/static/data/terrain/bihar/${meta.file}`;
            const startTime = typeof performance !== 'undefined' ? performance.now() : Date.now();

            if (this._worker) {
                return new Promise((resolve, reject) => {
                    const msgId = ++this._workerMsgId;
                    this._workerCallbacks.set(msgId, { resolve, reject, startTime });
                    this._worker.postMessage({
                        msgId,
                        action: 'FETCH_AND_DECODE',
                        url: tileUrl,
                        tileKey,
                    });
                });
            } else {
                const response = await fetch(tileUrl);
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status} fetching ${tileUrl}`);
                }
                const buffer = await response.arrayBuffer();
                const decoded = this._decodeMainThread(buffer, tileKey);
                this.diagnostics.workerDecodeTimeMs = (typeof performance !== 'undefined' ? performance.now() : Date.now()) - startTime;
                return decoded;
            }
        }

        /**
         * Synchronous main-thread decoder fallback.
         */
        _decodeMainThread(arrayBuffer, tileKey) {
            const dataView = new DataView(arrayBuffer);
            if (
                dataView.getUint8(0) !== 0x48 ||
                dataView.getUint8(1) !== 0x59 ||
                dataView.getUint8(2) !== 0x45 ||
                dataView.getUint8(3) !== 0x4c
            ) {
                throw new Error(`Invalid header magic in tile ${tileKey}`);
            }

            const z = dataView.getUint8(6);
            const x = dataView.getUint32(8, true);
            const y = dataView.getUint32(12, true);
            const gridWidth = dataView.getUint16(16, true);
            const gridHeight = dataView.getUint16(18, true);
            const sampleCount = dataView.getUint32(20, true);
            const minElevation = dataView.getFloat32(24, true);
            const maxElevation = dataView.getFloat32(28, true);
            const offset = dataView.getFloat32(32, true);
            const scale = dataView.getFloat32(36, true);

            const elevations = new Float32Array(sampleCount);
            let byteOffset = 40;
            for (let i = 0; i < sampleCount; i++) {
                const q = dataView.getInt16(byteOffset, true);
                byteOffset += 2;
                elevations[i] = q === -32768 ? NaN : offset + q * scale;
            }

            // Generate index buffer
            const indices = new Uint16Array(64 * 64 * 6);
            let ptr = 0;
            for (let r = 0; r < 64; r++) {
                for (let c = 0; c < 64; c++) {
                    const tl = r * 65 + c;
                    const tr = tl + 1;
                    const bl = (r + 1) * 65 + c;
                    const br = bl + 1;
                    indices[ptr++] = tl;
                    indices[ptr++] = bl;
                    indices[ptr++] = tr;
                    indices[ptr++] = tr;
                    indices[ptr++] = bl;
                    indices[ptr++] = br;
                }
            }

            return {
                header: { z, x, y, gridWidth, gridHeight, sampleCount, minElevation, maxElevation, offset, scale, key: tileKey },
                elevations,
                indices,
                tileKey,
            };
        }

        /**
         * Cleans up worker and cache.
         */
        destroy() {
            if (this._worker) {
                this._worker.terminate();
                this._worker = null;
            }
            this.cache.clear();
            this._inFlightRequests.clear();
            this._workerCallbacks.clear();
        }
    }

    // Export module
    const exports = {
        HYGoogleTerrainLoader,
        TerrainLRUCache,
        latLngToTileXY,
        tilePointToLatLng,
        getTileBounds,
        selectTargetLOD,
        selectTargetLODWithHysteresis,
        VERTEX_GRID_SIZE,
        CELL_SIZE,
    };

    if (typeof module !== 'undefined' && module.exports) {
        module.exports = exports;
    } else {
        global.HYGoogleTerrainLoader = HYGoogleTerrainLoader;
        global.TerrainLRUCache = TerrainLRUCache;
        global.HYTerrainUtils = {
            latLngToTileXY,
            tilePointToLatLng,
            getTileBounds,
            selectTargetLOD,
            selectTargetLODWithHysteresis,
        };
    }
})(typeof window !== 'undefined' ? window : globalThis);
