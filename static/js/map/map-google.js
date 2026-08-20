/* ═══════════════════════════════════════════════════════════════════
   HiddenYatra — MapGoogle (Google Maps Engine Adapter)
   Wraps a google.maps.Map instance for the HYMap hybrid system.
   Mirrors the same public interface as MapLeafletAdapter so
   map-core.js can use either engine interchangeably.

   Phase G1: Basic map rendering (pan, zoom, tilt, rotation).
   GeoJSON layers, markers, and full Layer Manager wiring
   will be added in Phases G2–G4.
   ═══════════════════════════════════════════════════════════════════ */

(function (root) {
  'use strict';

  class MapGoogleAdapter {
    /**
     * @param {google.maps.Map} googleMap - An already-initialized Google Map
     */
    constructor(googleMap) {
      if (!googleMap) throw new Error('[MapGoogleAdapter] Missing Google Maps instance');

      /** @type {google.maps.Map} */
      this.map = googleMap;

      /** @type {HTMLElement} The map container element */
      this.container = googleMap.getDiv();

      /** @type {Map<string, google.maps.Data>} Active GeoJSON data layers */
      this._dataLayers = new Map();

      /** @type {Map<number|string, google.maps.marker.AdvancedMarkerElement>} Tourist place markers */
      this._placesMarkers = new Map();

      /** @type {Map<string, Map<string|number, google.maps.marker.AdvancedMarkerElement>>} Point layer markers (hotels, homestays, waterfalls) */
      this._pointLayersMarkers = new Map();

      /** @type {google.maps.InfoWindow|null} Singleton InfoWindow instance */
      this._infoWindow = null;

      /** @type {google.maps.marker.AdvancedMarkerElement|null} Currently selected place marker */
      this._selectedMarker = null;

      /** @type {Function|null} Selection callback */
      this._onPlaceSelect = null;

      /** @type {google.maps.marker.AdvancedMarkerElement[]} Legacy marker array */
      this._markers = [];

      /** @type {Map<string, Object>} Overlay layer references (layerId → layer info) */
      this._overlays = new Map();

      /** @type {boolean} Track if map tiles have finished loading */
      this._loaded = false;

      /** @type {string|null} Current basemap source ID */
      this._currentBasemapId = null;

      /** @type {root.HYGoogleGeoLayerManager|null} Geographic Vector Layer Manager (Phase G3) */
      this.geoLayerManager = root.HYGoogleGeoLayerManager ? new root.HYGoogleGeoLayerManager(this.map, { infoWindow: this.getInfoWindow() }) : null;

      /** @type {root.HYGoogleTerrainManager|null} Custom 3D Terrain Manager (Phase G4A) */
      this.terrainManager = root.HYGoogleTerrainManager ? new root.HYGoogleTerrainManager(this.map) : null;

      // Mark loaded once tiles are ready
      google.maps.event.addListenerOnce(this.map, 'tilesloaded', () => {
        this._loaded = true;
        console.log('[MapGoogleAdapter] Tiles loaded — map ready');
      });

      // Bind to HYMapState for view sync
      this._bindStateSync();
    }

    /* ── State Synchronization ─────────────────────── */

    /** @private */
    _bindStateSync() {
      const state = root.HYMapState;
      if (!state) return;

      // Google Maps → HYMapState: sync view on idle
      this.map.addListener('idle', () => {
        if (state.activeEngine !== 'google') return;
        const center = this.map.getCenter();
        if (!center) return;
        state.setView({
          lat: center.lat(),
          lng: center.lng(),
          zoom: this.map.getZoom(),
          pitch: this.map.getTilt ? this.map.getTilt() : 0,
          bearing: this.map.getHeading ? this.map.getHeading() : 0,
        }, 'google');
      });

      // HYMapState → Google Maps: respond to view changes from other engines
      state.on('view', (data) => {
        if (data.source === 'google') return; // Don't echo our own changes
        if (state.activeEngine !== 'google') return;
        this.map.moveCamera({
          center: { lat: data.state.lat, lng: data.state.lng },
          zoom: data.state.zoom,
        });
      });
    }

    /* ── Base Map Switching ────────────────────────── */

    /**
     * Switch the base map style.
     * Google Maps uses Map IDs or built-in mapTypeIds for styling.
     * @param {string} sourceId - Key from HYTileSources (best-effort mapping)
     */
    setBasemap(sourceId) {
      this._currentBasemapId = sourceId;

      // Map HYTileSources keys to Google Maps mapTypeIds where possible
      const typeMap = {
        'satellite': google.maps.MapTypeId.SATELLITE,
        'hybrid': google.maps.MapTypeId.HYBRID,
        'terrain': google.maps.MapTypeId.TERRAIN,
        'roadmap': google.maps.MapTypeId.ROADMAP,
        // Defaults for OSM/CARTO styles → use roadmap (styled via Map ID)
        'carto_light': google.maps.MapTypeId.ROADMAP,
        'carto_dark': google.maps.MapTypeId.ROADMAP,
        'osm': google.maps.MapTypeId.ROADMAP,
        'esri_satellite': google.maps.MapTypeId.SATELLITE,
        'opentopomap': google.maps.MapTypeId.TERRAIN,
      };

      const mapType = typeMap[sourceId] || google.maps.MapTypeId.ROADMAP;
      this.map.setMapTypeId(mapType);
    }

    /** @returns {string|null} The current base map source ID */
    getCurrentBasemap() {
      return this._currentBasemapId || 'roadmap';
    }

    /* ── GeoJSON Layer Management ──────────────────── */

    /**
     * Add a GeoJSON layer to the map.
     * Phase G1: Basic implementation — loads features onto google.maps.Data.
     * @param {string} layerId
     * @param {Object} geojsonData - GeoJSON FeatureCollection
     * @param {Object} [styleOpts] - Style options from layer definition
     * @returns {google.maps.Data} The created Data layer
     */
    addGeoJSONLayer(layerId, geojsonData, styleOpts) {
      // Remove existing layer with same ID if present
      this.removeLayer(layerId);

      const def = root.HYLayerRegistry ? root.HYLayerRegistry.get(layerId) : null;
      const style = styleOpts || (def ? def.style : {});

      // Create a new Data layer
      const dataLayer = new google.maps.Data({ map: this.map });

      // Add GeoJSON features
      try {
        dataLayer.addGeoJson(geojsonData);
      } catch (err) {
        console.error(`[MapGoogleAdapter] Failed to add GeoJSON for ${layerId}:`, err);
        return null;
      }

      // Apply style
      dataLayer.setStyle((feature) => {
        const geomType = feature.getGeometry().getType();
        const isPoint = geomType === 'Point' || geomType === 'MultiPoint';
        const isLine = geomType === 'LineString' || geomType === 'MultiLineString';

        if (isPoint) {
          // Style point features as circles
          const color = this._resolvePointColor(layerId, style);
          return {
            icon: {
              path: google.maps.SymbolPath.CIRCLE,
              scale: style.radius || 7,
              fillColor: color,
              fillOpacity: style.fillOpacity !== undefined ? style.fillOpacity : 0.9,
              strokeColor: '#ffffff',
              strokeWeight: 2,
            },
          };
        }

        return {
          strokeColor: style.stroke || '#6366f1',
          strokeWeight: style.strokeWidth || 2,
          strokeOpacity: style.strokeOpacity || 0.8,
          fillColor: style.fillColor || style.stroke || '#6366f1',
          fillOpacity: isLine ? 0 : (style.fillOpacity !== undefined ? style.fillOpacity : 0.2),
        };
      });

      // Hover highlighting
      dataLayer.addListener('mouseover', (event) => {
        const geomType = event.feature.getGeometry().getType();
        const isLine = geomType === 'LineString' || geomType === 'MultiLineString';
        const isPoint = geomType === 'Point' || geomType === 'MultiPoint';

        if (isLine) {
          dataLayer.overrideStyle(event.feature, {
            strokeWeight: (style.strokeWidth || 3) + 2,
            strokeOpacity: 1.0,
          });
        } else if (isPoint) {
          const color = this._resolvePointColor(layerId, style);
          dataLayer.overrideStyle(event.feature, {
            icon: {
              path: google.maps.SymbolPath.CIRCLE,
              scale: (style.radius || 7) + 2,
              fillColor: color,
              fillOpacity: 1.0,
              strokeColor: '#ffffff',
              strokeWeight: 2,
            },
          });
        } else {
          dataLayer.overrideStyle(event.feature, {
            fillOpacity: Math.min(1.0, (style.fillOpacity || 0.35) + 0.25),
            strokeColor: style.hoverStroke || style.stroke || '#0891b2',
            strokeWeight: (style.strokeWidth || 2) + 1,
          });
        }
      });

      dataLayer.addListener('mouseout', (event) => {
        dataLayer.revertStyle(event.feature);
      });

      // Click handler — zoom to feature
      if (def && def.interactive) {
        dataLayer.addListener('click', (event) => {
          const geom = event.feature.getGeometry();
          const bounds = new google.maps.LatLngBounds();
          geom.forEachLatLng((latLng) => bounds.extend(latLng));

          if (!bounds.isEmpty()) {
            this.map.fitBounds(bounds, { top: 40, right: 40, bottom: 40, left: 40 });
          }

          // Emit selection event
          if (root.HYMapState) {
            root.HYMapState._notify('layer', {
              layerId,
              event: 'feature-click',
              feature: { properties: this._extractProperties(event.feature) },
            });
          }
        });
      }

      // Info windows for tooltips
      const infoWindow = new google.maps.InfoWindow();
      dataLayer.addListener('click', (event) => {
        const props = this._extractProperties(event.feature);
        const name = props.name || props.NAME || props.district || 'Region';
        infoWindow.setContent(`<strong>${name}</strong>`);
        infoWindow.setPosition(event.latLng);
        infoWindow.open(this.map);
      });

      this._dataLayers.set(layerId, dataLayer);
      this._overlays.set(layerId, { type: 'data', layer: dataLayer });

      // Register in LayerRegistry if available
      if (root.HYLayerRegistry) {
        root.HYLayerRegistry.setLeafletLayer(layerId, dataLayer);
      }

      return dataLayer;
    }

    /**
     * Extract properties from a google.maps.Data.Feature.
     * @private
     * @param {google.maps.Data.Feature} feature
     * @returns {Object}
     */
    _extractProperties(feature) {
      const props = {};
      feature.forEachProperty((value, key) => {
        props[key] = value;
      });
      return props;
    }

    /**
     * Resolve the point marker color for a given layer.
     * @private
     * @param {string} layerId
     * @param {Object} style
     * @returns {string}
     */
    _resolvePointColor(layerId, style) {
      if (layerId === 'hotels') return '#2563eb';
      if (layerId === 'homestays') return '#059669';
      return style.fillColor || style.color || '#06b6d4';
    }

    /**
     * Remove a layer from the map.
     * @param {string} layerId
     */
    removeLayer(layerId) {
      if (this._pointLayersMarkers.has(layerId)) {
        const pMap = this._pointLayersMarkers.get(layerId);
        pMap.forEach((m) => { m.map = null; });
        this._pointLayersMarkers.delete(layerId);
        this._overlays.delete(layerId);
        return;
      }

      if (this.geoLayerManager && this.geoLayerManager._layers.has(layerId)) {
        this.geoLayerManager.toggleLayer(layerId, false);
        return;
      }

      const dataLayer = this._dataLayers.get(layerId);
      if (dataLayer) {
        dataLayer.setMap(null);
        this._dataLayers.delete(layerId);
        this._overlays.delete(layerId);
        if (root.HYLayerRegistry) {
          root.HYLayerRegistry.removeLeafletLayer(layerId);
        }
      }
    }

    /* ── InfoWindow Singleton ──────────────────────── */

    /**
     * Get or create the shared InfoWindow singleton.
     * @returns {google.maps.InfoWindow|null}
     */
    getInfoWindow() {
      if (!this._infoWindow && typeof google !== 'undefined' && google.maps && google.maps.InfoWindow) {
        this._infoWindow = new google.maps.InfoWindow({
          maxWidth: 280,
          minWidth: 200,
        });
      }
      return this._infoWindow;
    }

    /* ── Tourist Places Markers ────────────────────── */

    /**
     * Render all tourist place markers on the Google Map.
     * @param {Array<Object>} places - List of place objects
     * @param {Function} [onSelectCallback] - Callback when a marker is clicked
     * @returns {number} Number of markers created
     */
    renderPlacesMarkers(places, onSelectCallback) {
      if (typeof onSelectCallback === 'function') {
        this._onPlaceSelect = onSelectCallback;
      }

      // Clear existing places markers
      this._placesMarkers.forEach((m) => { m.map = null; });
      this._placesMarkers.clear();

      if (!places || !places.length) return 0;
      if (!root.HYGoogleMarkerFactory) {
        console.warn('[MapGoogleAdapter] HYGoogleMarkerFactory not found');
        return 0;
      }

      places.forEach((place) => {
        const lat = parseFloat(place.latitude);
        const lng = parseFloat(place.longitude);
        if (isNaN(lat) || isNaN(lng) || lat < -90 || lat > 90 || lng < -180 || lng > 180) return;

        const marker = root.HYGoogleMarkerFactory.createMarker(this.map, place, {
          type: 'place',
          onClick: (data, m) => this.handlePlaceMarkerClick(data, m),
        });

        if (marker) {
          this._placesMarkers.set(place.id, marker);
        }
      });

      console.log(`[MapGoogleAdapter] Rendered ${this._placesMarkers.size} tourist place markers`);
      return this._placesMarkers.size;
    }

    /**
     * Handle click on a place marker.
     * @param {Object} place
     * @param {google.maps.marker.AdvancedMarkerElement} marker
     */
    handlePlaceMarkerClick(place, marker) {
      // Update selected visual
      if (this._selectedMarker && this._selectedMarker !== marker) {
        root.HYGoogleMarkerFactory.setSelected(this._selectedMarker, false);
      }
      this._selectedMarker = marker;
      root.HYGoogleMarkerFactory.setSelected(marker, true);

      // Pan smoothly to marker
      const lat = parseFloat(place.latitude);
      const lng = parseFloat(place.longitude);
      if (!isNaN(lat) && !isNaN(lng)) {
        this.map.panTo({ lat, lng });
      }

      // Open shared InfoWindow
      const infoWindow = this.getInfoWindow();
      if (infoWindow && root.HYGoogleMarkerFactory) {
        infoWindow.setContent(root.HYGoogleMarkerFactory.buildPlacePopupHTML(place));
        infoWindow.open({
          map: this.map,
          anchor: marker,
          shouldFocus: false,
        });
      }

      // Trigger callback to update sidebar & preview drawer
      if (typeof this._onPlaceSelect === 'function') {
        this._onPlaceSelect(place, marker);
      }

      // Notify HYMapState
      if (root.HYMapState) {
        root.HYMapState._notify('layer', {
          layerId: 'tourist_places',
          event: 'place-select',
          place: place,
        });
      }
    }

    /**
     * Focus and select a place by ID.
     * @param {number|string} placeId
     */
    selectPlaceById(placeId) {
      const marker = this._placesMarkers.get(placeId);
      if (marker && marker._hyData) {
        this.handlePlaceMarkerClick(marker._hyData, marker);
      }
    }

    /**
     * Filter tourist place markers by predicate or visible IDs.
     * @param {Set|Array|Function} predicateOrIds
     */
    filterPlacesMarkers(predicateOrIds) {
      if (typeof predicateOrIds === 'function') {
        this._placesMarkers.forEach((marker) => {
          const isVis = predicateOrIds(marker._hyData);
          marker.map = isVis ? this.map : null;
        });
      } else {
        const idSet = predicateOrIds instanceof Set ? predicateOrIds : new Set(predicateOrIds);
        this._placesMarkers.forEach((marker, id) => {
          const isVis = idSet.has(id);
          marker.map = isVis ? this.map : null;
        });
      }
    }

    /* ── Point Layer Markers (Hotels, Homestays, OSM Waterfalls) ── */

    /**
     * Add GeoJSON point features as Google Advanced Markers.
     * @param {string} layerId - 'hotels' | 'homestays' | 'waterfalls_geo' | 'waterfalls'
     * @param {Object} geojsonData
     */
    addPointMarkerLayer(layerId, geojsonData) {
      if (this._pointLayersMarkers.has(layerId)) {
        // Already instantiated — restore visibility
        const pMap = this._pointLayersMarkers.get(layerId);
        pMap.forEach((m) => { m.map = this.map; });
        return;
      }

      if (!geojsonData || !geojsonData.features || !root.HYGoogleMarkerFactory) return;

      const markerMap = new Map();
      geojsonData.features.forEach((feature, idx) => {
        const marker = root.HYGoogleMarkerFactory.createMarker(this.map, feature, {
          type: layerId,
          onClick: (feat, m) => this.handlePointMarkerClick(feat, layerId, m),
        });

        if (marker) {
          const fid = (feature.properties && (feature.properties.id || feature.properties.osm_id || feature.properties.slug)) || idx;
          markerMap.set(fid, marker);
        }
      });

      this._pointLayersMarkers.set(layerId, markerMap);
      this._overlays.set(layerId, { type: 'point-markers', markers: markerMap });
      console.log(`[MapGoogleAdapter] Added ${markerMap.size} point markers for layer: ${layerId}`);
    }

    /**
     * Handle click on a point layer marker.
     * @param {Object} feature
     * @param {string} layerId
     * @param {google.maps.marker.AdvancedMarkerElement} marker
     */
    handlePointMarkerClick(feature, layerId, marker) {
      const coords = feature.geometry ? feature.geometry.coordinates : null;
      if (coords) {
        this.map.panTo({ lat: coords[1], lng: coords[0] });
      }

      let html = '';
      const props = feature.properties || {};

      if (layerId === 'hotels') {
        html = root.HYGoogleMarkerFactory.buildHotelPopupHTML(props, coords);
      } else if (layerId === 'homestays') {
        html = root.HYGoogleMarkerFactory.buildHomestayPopupHTML(props, coords);
      } else if (layerId === 'waterfalls_geo' || layerId === 'waterfalls') {
        html = root.HYGoogleMarkerFactory.buildWaterfallPopupHTML(props, coords);
      } else {
        html = `<div style="padding:4px;"><strong>${props.name || 'Location'}</strong></div>`;
      }

      const infoWindow = this.getInfoWindow();
      if (infoWindow) {
        infoWindow.setContent(html);
        infoWindow.open({
          map: this.map,
          anchor: marker,
          shouldFocus: false,
        });
      }

      // Notify HYMapState
      if (root.HYMapState) {
        root.HYMapState._notify('layer', {
          layerId,
          event: 'feature-click',
          feature: feature,
        });
      }
    }

    /**
     * Toggle layer visibility.
     * @param {string} layerId
     * @param {boolean} visible
     */
    async toggleLayer(layerId, visible) {
      const isPointLayer = (layerId === 'hotels' || layerId === 'homestays' || layerId === 'waterfalls_geo' || layerId === 'waterfalls');

      if (isPointLayer) {
        if (visible) {
          if (this._pointLayersMarkers.has(layerId)) {
            const pMap = this._pointLayersMarkers.get(layerId);
            pMap.forEach((m) => { m.map = this.map; });
          } else {
            const def = root.HYLayerRegistry ? root.HYLayerRegistry.get(layerId) : null;
            if (def && def.source) {
              const data = await root.HYLayerRegistry.fetchData(layerId);
              if (data) {
                this.addPointMarkerLayer(layerId, data);
              }
            }
          }
        } else {
          if (this._pointLayersMarkers.has(layerId)) {
            const pMap = this._pointLayersMarkers.get(layerId);
            pMap.forEach((m) => { m.map = null; });
          }
        }
        return;
      }

      if (layerId === 'tourist_places') {
        this._placesMarkers.forEach((m) => { m.map = visible ? this.map : null; });
        return;
      }

      // Geographic Polygon and Line Layers (Phase G3)
      if (this.geoLayerManager) {
        await this.geoLayerManager.toggleLayer(layerId, visible);
        return;
      }

      // Fallback for direct Data layer
      if (visible) {
        if (this._dataLayers.has(layerId)) {
          const dataLayer = this._dataLayers.get(layerId);
          dataLayer.setMap(this.map);
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
        const dataLayer = this._dataLayers.get(layerId);
        if (dataLayer) {
          dataLayer.setMap(null);
        }
      }
    }

    /**
     * Set opacity for a layer.
     * @param {string} layerId
     * @param {number} opacity - 0.0 to 1.0
     */
    setLayerOpacity(layerId, opacity) {
      if (this.geoLayerManager) {
        this.geoLayerManager.setLayerOpacity(layerId, opacity);
      }

      const dataLayer = this._dataLayers.get(layerId);
      if (!dataLayer) return;

      const def = root.HYLayerRegistry ? root.HYLayerRegistry.get(layerId) : null;
      const baseStyle = def ? def.style : {};

      dataLayer.setStyle((feature) => {
        const geomType = feature.getGeometry().getType();
        const isLine = geomType === 'LineString' || geomType === 'MultiLineString';

        return {
          strokeOpacity: (baseStyle.strokeOpacity !== undefined ? baseStyle.strokeOpacity : 0.85) * opacity,
          fillOpacity: isLine ? 0 : (baseStyle.fillOpacity !== undefined ? baseStyle.fillOpacity : 0.25) * opacity,
        };
      });
    }

    /* ── Visibility Control ────────────────────────── */

    /** Show the Google Map container */
    show() {
      this.container.style.opacity = '1';
      this.container.style.pointerEvents = 'auto';
      this.container.style.zIndex = '1';
      google.maps.event.trigger(this.map, 'resize');
    }

    /** Hide the Google Map container */
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
          google.maps.event.trigger(this.map, 'resize');
          resolve();
        }, durationMs);
      });
    }

    /* ── Utility ───────────────────────────────────── */

    /** @returns {{lat:number, lng:number}} */
    getCenter() {
      const c = this.map.getCenter();
      return c ? { lat: c.lat(), lng: c.lng() } : { lat: 25.0961, lng: 85.3131 };
    }

    /** @returns {number} */
    getZoom() {
      return this.map.getZoom();
    }

    /**
     * Set the map view without animation.
     * @param {number} lat
     * @param {number} lng
     * @param {number} zoom
     */
    setView(lat, lng, zoom) {
      this.map.moveCamera({
        center: { lat, lng },
        zoom: zoom || this.map.getZoom(),
      });
    }

    /**
     * Fly to a location with smooth animation.
     * @param {number} lat
     * @param {number} lng
     * @param {number} [zoom]
     * @param {number} [durationSec=1.2]
     */
    flyTo(lat, lng, zoom, durationSec = 1.2) {
      this.map.panTo({ lat, lng });
      if (zoom && zoom !== this.map.getZoom()) {
        this.map.setZoom(zoom);
      }
    }

    /** @returns {boolean} */
    isLoaded() {
      return this._loaded;
    }

    /* ── Google-Specific Helpers ───────────────────── */

    /**
     * Set map tilt (pitch) in degrees.
     * @param {number} degrees - 0 to 67.5 for Vector maps
     */
    setTilt(degrees) {
      if (this.map.setTilt) {
        this.map.setTilt(degrees);
      }
    }

    /**
     * Set map heading (bearing/rotation) in degrees.
     * @param {number} degrees - 0 to 360
     */
    setHeading(degrees) {
      if (this.map.setHeading) {
        this.map.setHeading(degrees);
      }
    }

    /** Trigger resize (call after container resize) */
    invalidateSize() {
      google.maps.event.trigger(this.map, 'resize');
    }

    /**
     * Clean up all resources.
     */
    destroy() {
      // Remove all data layers
      this._dataLayers.forEach((layer) => {
        layer.setMap(null);
      });
      this._dataLayers.clear();
      this._overlays.clear();

      // Clear tourist place markers
      this._placesMarkers.forEach((marker) => {
        marker.map = null;
      });
      this._placesMarkers.clear();

      // Clear point layers markers
      this._pointLayersMarkers.forEach((pMap) => {
        pMap.forEach((m) => { m.map = null; });
      });
      this._pointLayersMarkers.clear();

      // Close and clear InfoWindow
      if (this._infoWindow) {
        this._infoWindow.close();
        this._infoWindow = null;
      }
      this._selectedMarker = null;

      // Clean up Geographic Vector Layer Manager (Phase G3)
      if (this.geoLayerManager) {
        this.geoLayerManager.destroy();
        this.geoLayerManager = null;
      }

      // Clean up Custom 3D Terrain Manager (Phase G4A)
      if (this.terrainManager) {
        this.terrainManager.destroy();
        this.terrainManager = null;
      }

      this._loaded = false;
    }
  }

  root.HYMapGoogleAdapter = MapGoogleAdapter;

})(window);
