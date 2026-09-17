/* ═══════════════════════════════════════════════════════════════════
   HiddenYatra — MapLayers (Layer Registry & Definitions)
   Manages geographic data layers for both Leaflet & MapLibre engines
   ═══════════════════════════════════════════════════════════════════ */

(function (root) {
  'use strict';

  /* ── Tile Source Definitions ──────────────────────── */
  const TILE_SOURCES = {
    carto_light: {
      id: 'carto_light',
      name: 'Light',
      emoji: '☀️',
      url: 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/">CARTO</a>',
      maxZoom: 19,
      subdomains: 'abcd',
    },
    carto_dark: {
      id: 'carto_dark',
      name: 'Dark',
      emoji: '🌙',
      url: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/">CARTO</a>',
      maxZoom: 19,
      subdomains: 'abcd',
    },
    esri_satellite: {
      id: 'esri_satellite',
      name: 'Satellite',
      emoji: '🛰️',
      url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
      attribution: '&copy; Esri, USGS, NOAA',
      maxZoom: 18,
      subdomains: null,
    },
    opentopomap: {
      id: 'opentopomap',
      name: 'Terrain',
      emoji: '🏔️',
      url: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
      maxZoom: 17,
      subdomains: 'abc',
    },
    carto_labels: {
      id: 'carto_labels',
      name: 'Labels',
      emoji: '🏷️',
      url: 'https://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}{r}.png',
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/">CARTO</a>',
      maxZoom: 19,
      subdomains: 'abcd',
      isOverlay: true,
    },
  };

  /* ── Layer Definitions ───────────────────────────── */

  /**
   * @typedef {Object} LayerDefinition
   * @property {string} id              - Unique layer identifier
   * @property {string} label           - Display label
   * @property {string} group           - Layer group category
   * @property {string} icon            - Display emoji/icon
   * @property {boolean} defaultVisible - Initial visibility state
   * @property {number} [minZoom]       - Minimum zoom to display
   * @property {number} [maxZoom]       - Maximum zoom to display
   * @property {string[]} engineSupport - ['leaflet', 'maplibre']
   * @property {'geojson'|'raster'|'raster-dem'|'markers'|'vector'|'virtual'} sourceType
   * @property {string|null} [source]   - URL to data source (null for virtual/client layers)
   * @property {boolean} interactive    - Whether layer features are clickable
   * @property {number} [opacity]       - Default opacity (0.0 - 1.0)
   * @property {number} [renderOrder]   - Stacking order
   * @property {string|null} [parent]   - Parent layer ID for hierarchical control
   * @property {string[]} [children]    - Child layer IDs if parent
   * @property {string} [description]   - Tooltip description
   * @property {Object} [style]         - Default vector/raster styling
   */

  const LAYER_DEFINITIONS = [
    // ═══════════════════════════════════════════════════
    // 1. TERRAIN (group: 'terrain')
    // ═══════════════════════════════════════════════════
    {
      id: 'terrain_relief',
      label: 'Terrain Relief',
      name: 'Terrain Relief',
      group: 'terrain',
      icon: '⛰️',
      emoji: '⛰️',
      defaultVisible: false,
      minZoom: 5,
      maxZoom: 18,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'raster',
      source: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
      interactive: false,
      opacity: 0.8,
      renderOrder: 10,
      parent: null,
      description: 'Topographic contour and elevation shading',
    },
    {
      id: 'hillshade',
      label: 'Hillshade',
      name: 'Hillshade',
      group: 'terrain',
      icon: '🌄',
      emoji: '🌄',
      defaultVisible: false,
      minZoom: 5,
      maxZoom: 18,
      engineSupport: ['maplibre'],
      sourceType: 'raster',
      source: null,
      interactive: false,
      opacity: 0.5,
      renderOrder: 11,
      parent: null,
      description: 'Sun-illuminated 3D mountain relief shading',
      style: {
        shadowColor: '#000000',
        highlightColor: '#ffffff',
        exaggeration: 0.5,
      },
    },
    {
      id: '3d_terrain',
      label: '3D Terrain',
      name: '3D Terrain',
      group: 'terrain',
      icon: '🏔️',
      emoji: '🏔️',
      defaultVisible: false,
      minZoom: 6,
      maxZoom: 18,
      engineSupport: ['maplibre'],
      sourceType: 'raster-dem',
      source: 'https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png',
      interactive: false,
      opacity: 1.0,
      renderOrder: 12,
      parent: null,
      description: 'True 3D digital elevation mesh displacement',
      style: {
        encoding: 'terrarium',
        exaggeration: 1.5,
        tileSize: 256,
      },
    },

    // ═══════════════════════════════════════════════════
    // 2. NATURAL GEOGRAPHY (group: 'natural_geography')
    // ═══════════════════════════════════════════════════
    {
      id: 'natural_geography',
      label: 'Natural Geography',
      name: 'Natural Geography',
      group: 'natural_geography',
      icon: '🌿',
      emoji: '🌿',
      defaultVisible: true,
      minZoom: 5,
      maxZoom: 18,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'virtual',
      source: null,
      interactive: false,
      opacity: 1.0,
      renderOrder: 20,
      parent: null,
      children: ['rivers', 'lakes_dams', 'forests', 'waterfalls_geo', 'hills_mountains'],
      description: 'All natural geographical bodies and ecological zones',
    },
    {
      id: 'rivers',
      label: 'Rivers',
      name: 'Rivers',
      group: 'natural_geography',
      icon: '🌊',
      emoji: '🌊',
      defaultVisible: true,
      minZoom: 6,
      maxZoom: 18,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'geojson',
      source: '/static/data/bihar/rivers.geojson',
      interactive: true,
      opacity: 0.85,
      renderOrder: 21,
      parent: 'natural_geography',
      description: 'Ganga, Gandak, Kosi, Son, Falgu and major Bihar river networks',
      style: { stroke: '#0284c7', strokeWidth: 3, strokeOpacity: 0.85 },
    },
    {
      id: 'lakes_dams',
      label: 'Lakes & Dams',
      name: 'Lakes & Dams',
      group: 'natural_geography',
      icon: '💧',
      emoji: '💧',
      defaultVisible: true,
      minZoom: 7,
      maxZoom: 18,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'geojson',
      source: '/static/data/bihar/lakes_dams.geojson',
      interactive: true,
      opacity: 0.85,
      renderOrder: 22,
      parent: 'natural_geography',
      description: 'Kanwar Lake, Nagi-Nakti, Durgavati, and major reservoir dams',
      style: { fillColor: '#06b6d4', fillOpacity: 0.40, stroke: '#0891b2', strokeWidth: 1.8, strokeOpacity: 0.9 },
    },
    {
      id: 'forests',
      label: 'Forests',
      name: 'Forests',
      group: 'natural_geography',
      icon: '🌲',
      emoji: '🌲',
      defaultVisible: true,
      minZoom: 7,
      maxZoom: 18,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'geojson',
      source: '/static/data/bihar/forests.geojson',
      interactive: true,
      opacity: 0.85,
      renderOrder: 23,
      parent: 'natural_geography',
      description: 'Valmiki Tiger Reserve, Kaimur forest covers and sanctuaries',
      style: { fillColor: '#15803d', fillOpacity: 0.28, stroke: '#166534', strokeWidth: 1.8, strokeOpacity: 0.85 },
    },
    {
      id: 'waterfalls_geo',
      label: 'Waterfalls',
      name: 'Waterfalls',
      group: 'natural_geography',
      icon: '💦',
      emoji: '💦',
      defaultVisible: true,
      minZoom: 7,
      maxZoom: 18,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'geojson',
      source: '/static/data/bihar/waterfalls.geojson',
      interactive: true,
      opacity: 0.9,
      renderOrder: 24,
      parent: 'natural_geography',
      description: 'Kakolat, Telhar, Tutla Bhawani, and Kaimur plateau falls',
      style: { color: '#06b6d4', radius: 7, fillOpacity: 0.9 },
    },
    {
      id: 'hills_mountains',
      label: 'Hills & Mountains',
      name: 'Hills & Mountains',
      group: 'natural_geography',
      icon: '⛰️',
      emoji: '⛰️',
      defaultVisible: false,
      disabled: true,
      minZoom: 7,
      maxZoom: 18,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'geojson',
      source: null,
      interactive: false,
      opacity: 0.85,
      renderOrder: 25,
      parent: 'natural_geography',
      description: 'Rajgir Hills, Mandar Hill, Brahmayoni, and Someshwar range (planned)',
    },

    // ═══════════════════════════════════════════════════
    // 3. BOUNDARIES (group: 'boundaries')
    // ═══════════════════════════════════════════════════
    {
      id: 'boundaries',
      label: 'Boundaries',
      name: 'Boundaries',
      group: 'boundaries',
      icon: '🗺️',
      emoji: '🗺️',
      defaultVisible: false,
      minZoom: 5,
      maxZoom: 18,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'virtual',
      source: null,
      interactive: false,
      opacity: 1.0,
      renderOrder: 30,
      parent: null,
      children: ['state_boundary', 'district_boundaries', 'block_boundaries'],
      description: 'Administrative borders and jurisdictions',
    },
    {
      id: 'state_boundary',
      label: 'State Boundary',
      name: 'State Boundary',
      group: 'boundaries',
      icon: '🗺️',
      emoji: '🗺️',
      defaultVisible: false,
      minZoom: 5,
      maxZoom: 12,
      engineSupport: ['google', 'leaflet', 'maplibre'],
      sourceType: 'geojson',
      source: '/static/data/bihar/state_boundary.geojson',
      interactive: true,
      opacity: 0.9,
      renderOrder: 31,
      parent: 'boundaries',
      description: 'Outer perimeter boundary of the State of Bihar',
      style: { stroke: '#f59e0b', strokeWidth: 3, strokeOpacity: 0.9, fillOpacity: 0 },
    },
    {
      id: 'district_boundaries',
      label: 'District Boundaries',
      name: 'District Boundaries',
      group: 'boundaries',
      icon: '📍',
      emoji: '📍',
      defaultVisible: false,
      minZoom: 6,
      maxZoom: 18,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'geojson',
      source: '/static/data/bihar/districts.geojson',
      interactive: true,
      opacity: 0.7,
      renderOrder: 32,
      parent: 'boundaries',
      description: '38 districts of Bihar with polygon highlights and stats',
      style: {
        stroke: '#6366f1',
        strokeWidth: 2,
        strokeOpacity: 0.7,
        fillColor: '#6366f1',
        fillOpacity: 0.06,
        hoverFillOpacity: 0.15,
        hoverStroke: '#818cf8',
      },
    },
    {
      id: 'block_boundaries',
      label: 'Block Boundaries',
      name: 'Block Boundaries',
      group: 'boundaries',
      icon: '🔲',
      emoji: '🔲',
      defaultVisible: false,
      minZoom: 10,
      maxZoom: 18,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'geojson',
      source: '/static/data/bihar/blocks.geojson',
      interactive: true,
      opacity: 0.5,
      renderOrder: 33,
      parent: 'boundaries',
      description: '534 block-level administrative divisions (Census of India / Survey of India)',
      attribution: 'Boundaries derived from Census of India 2011 & Survey of India via datta07/INDIAN-SHAPEFILES (MIT License)',
      style: { stroke: '#94a3b8', strokeWidth: 1, strokeOpacity: 0.5, fillOpacity: 0.02, hoverStroke: '#f59e0b' },
    },

    // ═══════════════════════════════════════════════════
    // 4. TOURISM (group: 'tourism')
    // ═══════════════════════════════════════════════════
    {
      id: 'tourist_places',
      label: 'Tourist Places',
      name: 'Tourist Places',
      group: 'tourism',
      icon: '📍',
      emoji: '📍',
      defaultVisible: true,
      minZoom: 6,
      maxZoom: 19,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'markers',
      source: null,
      interactive: true,
      opacity: 1.0,
      renderOrder: 40,
      parent: null,
      children: [
        'temple',
        'fort',
        'waterfall',
        'historical',
        'religious',
        'nature',
        'hidden_gem',
        'viewpoint',
        'hotels',
        'homestays',
        'restaurants',
        'local_food',
        'user_submitted',
      ],
      description: 'All tourist destinations, heritage landmarks, and experiences',
    },
    {
      id: 'temple',
      label: 'Temples',
      name: 'Temples',
      group: 'tourism',
      icon: '🛕',
      emoji: '🛕',
      defaultVisible: true,
      minZoom: 6,
      maxZoom: 19,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'markers',
      source: null,
      interactive: true,
      opacity: 1.0,
      renderOrder: 41,
      parent: 'tourist_places',
      description: 'Ancient shrines, Mahabodhi, Vishnupad, Mundeshwari and temples',
      style: { markerColor: '#f59e0b' },
    },
    {
      id: 'fort',
      label: 'Forts',
      name: 'Forts',
      group: 'tourism',
      icon: '🏰',
      emoji: '🏰',
      defaultVisible: true,
      minZoom: 6,
      maxZoom: 19,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'markers',
      source: null,
      interactive: true,
      opacity: 1.0,
      renderOrder: 42,
      parent: 'tourist_places',
      description: 'Rohtasgarh, Munger Fort, Shergarh, and historic citadels',
      style: { markerColor: '#d97706' },
    },
    {
      id: 'waterfall',
      label: 'Waterfalls',
      name: 'Waterfalls',
      group: 'tourism',
      icon: '💧',
      emoji: '💧',
      defaultVisible: true,
      minZoom: 6,
      maxZoom: 19,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'markers',
      source: null,
      interactive: true,
      opacity: 1.0,
      renderOrder: 43,
      parent: 'tourist_places',
      description: 'Kakolat, Telhar Kund, Tutla Bhawani waterfalls',
      style: { markerColor: '#06b6d4' },
    },
    {
      id: 'historical',
      label: 'Historical',
      name: 'Historical',
      group: 'tourism',
      icon: '🏛️',
      emoji: '🏛️',
      defaultVisible: true,
      minZoom: 6,
      maxZoom: 19,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'markers',
      source: null,
      interactive: true,
      opacity: 1.0,
      renderOrder: 44,
      parent: 'tourist_places',
      description: 'Nalanda University ruins, Vikramshila, Barabar Caves, Golghar',
      style: { markerColor: '#8b5cf6' },
    },
    {
      id: 'religious',
      label: 'Religious',
      name: 'Religious',
      group: 'tourism',
      icon: '🙏',
      emoji: '🙏',
      defaultVisible: true,
      minZoom: 6,
      maxZoom: 19,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'markers',
      source: null,
      interactive: true,
      opacity: 1.0,
      renderOrder: 45,
      parent: 'tourist_places',
      description: 'Takht Sri Patna Sahib, Pawapuri Jal Mandir, Maner Sharif',
      style: { markerColor: '#f97316' },
    },
    {
      id: 'nature',
      label: 'Nature',
      name: 'Nature',
      group: 'tourism',
      icon: '🌿',
      emoji: '🌿',
      defaultVisible: true,
      minZoom: 6,
      maxZoom: 19,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'markers',
      source: null,
      interactive: true,
      opacity: 1.0,
      renderOrder: 46,
      parent: 'tourist_places',
      description: 'Valmiki National Park, Bhimbandh Wildlife Sanctuary, Pant Wildlife',
      style: { markerColor: '#10b981' },
    },
    {
      id: 'hidden_gem',
      label: 'Hidden Gems',
      name: 'Hidden Gems',
      group: 'tourism',
      icon: '💎',
      emoji: '💎',
      defaultVisible: true,
      minZoom: 6,
      maxZoom: 19,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'markers',
      source: null,
      interactive: true,
      opacity: 1.0,
      renderOrder: 47,
      parent: 'tourist_places',
      description: 'Offbeat rural destinations, secret springs, and undiscovered sites',
      style: { markerColor: '#ec4899' },
    },
    {
      id: 'viewpoint',
      label: 'Viewpoints',
      name: 'Viewpoints',
      group: 'tourism',
      icon: '👁️',
      emoji: '👁️',
      defaultVisible: true,
      minZoom: 7,
      maxZoom: 19,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'markers',
      source: null,
      interactive: true,
      opacity: 1.0,
      renderOrder: 48,
      parent: 'tourist_places',
      description: 'Shanti Stupa, Griddhakuta Peak, and panoramic hill outlooks',
      style: { markerColor: '#6366f1' },
    },
    {
      id: 'hotels',
      label: 'Hotels',
      name: 'Hotels',
      group: 'tourism',
      icon: '🏨',
      emoji: '🏨',
      defaultVisible: false,
      minZoom: 7,
      maxZoom: 18,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'geojson',
      source: '/static/data/bihar/hotels.geojson',
      interactive: true,
      opacity: 1.0,
      renderOrder: 49,
      parent: 'tourist_places',
      description: '12 verified hotel and lodging locations across Bihar',
      style: { color: '#2563eb', stroke: '#ffffff', strokeWidth: 2, radius: 7, fillOpacity: 0.9, markerColor: '#2563eb' },
    },
    {
      id: 'homestays',
      label: 'Homestays',
      name: 'Homestays',
      group: 'tourism',
      icon: '🏡',
      emoji: '🏡',
      defaultVisible: false,
      minZoom: 7,
      maxZoom: 18,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'geojson',
      source: '/static/data/bihar/homestays.geojson',
      interactive: true,
      opacity: 1.0,
      renderOrder: 50,
      parent: 'tourist_places',
      description: '10 verified authentic homestays and eco retreats',
      style: { color: '#059669', stroke: '#ffffff', strokeWidth: 2, radius: 7, fillOpacity: 0.9, markerColor: '#059669' },
    },
    {
      id: 'restaurants',
      label: 'Restaurants',
      name: 'Restaurants',
      group: 'tourism',
      icon: '🍽️',
      emoji: '🍽️',
      defaultVisible: false,
      minZoom: 9,
      maxZoom: 19,
      engineSupport: ['google', 'leaflet', 'maplibre'],
      sourceType: 'markers',
      source: '/api/nearby?category=restaurant',
      interactive: true,
      opacity: 1.0,
      renderOrder: 51,
      parent: 'tourist_places',
      description: 'Dhabas, family eateries, and heritage restaurants',
      style: { markerColor: '#ef4444' },
    },
    {
      id: 'local_food',
      label: 'Local Food',
      name: 'Local Food',
      group: 'tourism',
      icon: '🍲',
      emoji: '🍲',
      defaultVisible: false,
      minZoom: 8,
      maxZoom: 19,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'markers',
      source: null,
      interactive: true,
      opacity: 1.0,
      renderOrder: 52,
      parent: 'tourist_places',
      description: 'Litti Chokha, Silao Khaja, Maner Ladoo, and culinary stops',
      style: { markerColor: '#f97316' },
    },
    {
      id: 'user_submitted',
      label: 'User Submitted Places',
      name: 'User Submitted Places',
      group: 'tourism',
      icon: '👤',
      emoji: '👤',
      defaultVisible: false,
      minZoom: 7,
      maxZoom: 19,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'markers',
      source: null,
      interactive: true,
      opacity: 1.0,
      renderOrder: 53,
      parent: 'tourist_places',
      description: 'Community-contributed discoveries and traveler verified spots',
      style: { markerColor: '#a855f7' },
    },

    // ═══════════════════════════════════════════════════
    // 5. ROADS & TRANSPORT (group: 'roads_transport')
    // ═══════════════════════════════════════════════════
    {
      id: 'roads_transport',
      label: 'Roads & Transport',
      name: 'Roads & Transport',
      group: 'roads_transport',
      icon: '🛣️',
      emoji: '🛣️',
      defaultVisible: false,
      disabled: true,
      minZoom: 6,
      maxZoom: 18,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'virtual',
      source: null,
      interactive: false,
      opacity: 1.0,
      renderOrder: 60,
      parent: null,
      children: ['highways', 'major_roads', 'local_roads', 'railway'],
      description: 'Transit networks, highways, expressways and rail routes (planned)',
    },
    {
      id: 'highways',
      label: 'Highways',
      name: 'Highways',
      group: 'roads_transport',
      icon: '🛣️',
      emoji: '🛣️',
      defaultVisible: false,
      disabled: true,
      minZoom: 6,
      maxZoom: 18,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'geojson',
      source: null,
      interactive: false,
      opacity: 0.9,
      renderOrder: 61,
      parent: 'roads_transport',
      description: 'NH-31, NH-19, Purvanchal Expressway & National Highway arteries (planned)',
      style: { stroke: '#f59e0b', strokeWidth: 3, strokeOpacity: 0.9 },
    },
    {
      id: 'major_roads',
      label: 'Major Roads',
      name: 'Major Roads',
      group: 'roads_transport',
      icon: '🚗',
      emoji: '🚗',
      defaultVisible: false,
      disabled: true,
      minZoom: 8,
      maxZoom: 18,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'geojson',
      source: null,
      interactive: false,
      opacity: 0.8,
      renderOrder: 62,
      parent: 'roads_transport',
      description: 'State highways and inter-district major roads (planned)',
      style: { stroke: '#fbbf24', strokeWidth: 2, strokeOpacity: 0.75 },
    },
    {
      id: 'local_roads',
      label: 'Local Roads',
      name: 'Local Roads',
      group: 'roads_transport',
      icon: '🚲',
      emoji: '🚲',
      defaultVisible: false,
      disabled: true,
      minZoom: 12,
      maxZoom: 18,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'geojson',
      source: null,
      interactive: false,
      opacity: 0.6,
      renderOrder: 63,
      parent: 'roads_transport',
      description: 'Rural village pathways and local city streets (planned)',
      style: { stroke: '#94a3b8', strokeWidth: 1, strokeOpacity: 0.6 },
    },
    {
      id: 'railway',
      label: 'Railway',
      name: 'Railway',
      group: 'roads_transport',
      icon: '🚆',
      emoji: '🚆',
      defaultVisible: false,
      disabled: true,
      minZoom: 7,
      maxZoom: 18,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'geojson',
      source: null,
      interactive: false,
      opacity: 0.85,
      renderOrder: 64,
      parent: 'roads_transport',
      description: 'East Central Railway lines, express junctions, and rail stations (planned)',
      style: { stroke: '#475569', strokeWidth: 2, strokeDasharray: '4,4' },
    },

    // ═══════════════════════════════════════════════════
    // 6. ROUTES & NAVIGATION (group: 'routes')
    // ═══════════════════════════════════════════════════
    {
      id: 'routes',
      label: 'Routes & Navigation',
      name: 'Routes & Navigation',
      group: 'routes',
      icon: '🧭',
      emoji: '🧭',
      defaultVisible: false,
      disabled: true,
      minZoom: 6,
      maxZoom: 18,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'virtual',
      source: null,
      interactive: false,
      opacity: 1.0,
      renderOrder: 70,
      parent: null,
      children: ['my_location', 'active_routes', 'distance_measurement'],
      description: 'GPS positioning, route preview & distance tools (planned)',
    },
    {
      id: 'my_location',
      label: 'My Location',
      name: 'My Location',
      group: 'routes',
      icon: '🎯',
      emoji: '🎯',
      defaultVisible: false,
      disabled: true,
      minZoom: 6,
      maxZoom: 19,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'markers',
      source: null,
      interactive: false,
      opacity: 1.0,
      renderOrder: 71,
      parent: 'routes',
      description: 'Live traveler GPS location marker and accuracy radius (planned)',
    },
    {
      id: 'active_routes',
      label: 'Routes',
      name: 'Routes',
      group: 'routes',
      icon: '🧭',
      emoji: '🧭',
      defaultVisible: false,
      disabled: true,
      minZoom: 6,
      maxZoom: 19,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'geojson',
      source: null,
      interactive: false,
      opacity: 0.9,
      renderOrder: 72,
      parent: 'routes',
      description: 'Active travel itinerary path and driving directions polyline (planned)',
      style: { stroke: '#FF7A18', strokeWidth: 4, strokeOpacity: 0.9 },
    },
    {
      id: 'distance_measurement',
      label: 'Distance',
      name: 'Distance',
      group: 'routes',
      icon: '📏',
      emoji: '📏',
      defaultVisible: false,
      disabled: true,
      minZoom: 6,
      maxZoom: 19,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'virtual',
      source: null,
      interactive: false,
      opacity: 1.0,
      renderOrder: 73,
      parent: 'routes',
      description: 'Point-to-point geodesic distance and travel duration estimation (planned)',
    },

    // ═══════════════════════════════════════════════════
    // 7. ANALYTICS (group: 'analytics')
    // ═══════════════════════════════════════════════════
    {
      id: 'analytics',
      label: 'Analytics & Heatmaps',
      name: 'Analytics & Heatmaps',
      group: 'analytics',
      icon: '📊',
      emoji: '📊',
      defaultVisible: false,
      disabled: true,
      minZoom: 6,
      maxZoom: 18,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'virtual',
      source: null,
      interactive: false,
      opacity: 1.0,
      renderOrder: 80,
      parent: null,
      children: ['heatmap', 'density'],
      description: 'Tourism density intensity heatmaps and cluster analytics (planned)',
    },
    {
      id: 'heatmap',
      label: 'Heatmap',
      name: 'Heatmap',
      group: 'analytics',
      icon: '🔥',
      emoji: '🔥',
      defaultVisible: false,
      disabled: true,
      minZoom: 6,
      maxZoom: 15,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'virtual',
      source: null,
      interactive: false,
      opacity: 0.75,
      renderOrder: 81,
      parent: 'analytics',
      description: 'Tourist footfall and popularity intensity heatmap (planned)',
    },
    {
      id: 'density',
      label: 'Density',
      name: 'Density',
      group: 'analytics',
      icon: '📊',
      emoji: '📊',
      defaultVisible: false,
      disabled: true,
      minZoom: 6,
      maxZoom: 15,
      engineSupport: ['leaflet', 'maplibre'],
      sourceType: 'virtual',
      source: null,
      interactive: false,
      opacity: 0.8,
      renderOrder: 82,
      parent: 'analytics',
      description: 'District-wise tourist attraction cluster density grid (planned)',
    },

    // ═══════════════════════════════════════════════════
    // 8. CULTURE (group: 'culture') — Tejas 2.2
    // ═══════════════════════════════════════════════════
    {
      id: 'culture',
      label: 'Culture',
      name: 'Culture',
      group: 'culture',
      icon: '🏺',
      emoji: '🏺',
      defaultVisible: false,
      minZoom: 6,
      maxZoom: 19,
      engineSupport: ['google', 'leaflet', 'maplibre'],
      sourceType: 'virtual',
      source: null,
      interactive: false,
      opacity: 1.0,
      renderOrder: 90,
      parent: null,
      children: ['culture_heritage', 'culture_festivals', 'culture_crafts', 'culture_performing_arts', 'culture_food'],
      description: 'Bihar cultural heritage — archaeology, festivals, crafts, performing arts & food',
    },
    {
      id: 'culture_heritage',
      label: 'Heritage / Archaeology',
      name: 'Heritage / Archaeology',
      group: 'culture',
      icon: '🏛️',
      emoji: '🏛️',
      defaultVisible: false,
      minZoom: 6,
      maxZoom: 19,
      engineSupport: ['google', 'leaflet', 'maplibre'],
      sourceType: 'markers',
      source: '/api/culture-map?category=heritage',
      interactive: true,
      opacity: 1.0,
      renderOrder: 91,
      parent: 'culture',
      description: 'Ashokan pillars, Mauryan ruins, Pala bronzes, Neolithic sites',
      style: { markerColor: '#b45309' },
    },
    {
      id: 'culture_festivals',
      label: 'Festivals',
      name: 'Festivals',
      group: 'culture',
      icon: '🎪',
      emoji: '🎪',
      defaultVisible: false,
      minZoom: 6,
      maxZoom: 19,
      engineSupport: ['google', 'leaflet', 'maplibre'],
      sourceType: 'markers',
      source: '/api/culture-map?category=festivals',
      interactive: true,
      opacity: 1.0,
      renderOrder: 92,
      parent: 'culture',
      description: 'Chhath Puja, Sonepur Mela, Rajgir Mahotsav and seasonal celebrations',
      style: { markerColor: '#dc2626' },
    },
    {
      id: 'culture_crafts',
      label: 'Crafts',
      name: 'Crafts',
      group: 'culture',
      icon: '🎨',
      emoji: '🎨',
      defaultVisible: false,
      minZoom: 6,
      maxZoom: 19,
      engineSupport: ['google', 'leaflet', 'maplibre'],
      sourceType: 'markers',
      source: '/api/culture-map?category=crafts',
      interactive: true,
      opacity: 1.0,
      renderOrder: 93,
      parent: 'culture',
      description: 'Madhubani painting, Bhagalpuri silk, Sikki grass craft workshops',
      style: { markerColor: '#7c3aed' },
    },
    {
      id: 'culture_performing_arts',
      label: 'Performing Arts',
      name: 'Performing Arts',
      group: 'culture',
      icon: '🎭',
      emoji: '🎭',
      defaultVisible: false,
      minZoom: 6,
      maxZoom: 19,
      engineSupport: ['google', 'leaflet', 'maplibre'],
      sourceType: 'markers',
      source: '/api/culture-map?category=performing_arts',
      interactive: true,
      opacity: 1.0,
      renderOrder: 94,
      parent: 'culture',
      description: 'Bidesiya theater, Chhau dance, Kajari monsoon songs, Sohar chants',
      style: { markerColor: '#db2777' },
    },
    {
      id: 'culture_food',
      label: 'Local Food',
      name: 'Local Food',
      group: 'culture',
      icon: '🍲',
      emoji: '🍲',
      defaultVisible: false,
      minZoom: 6,
      maxZoom: 19,
      engineSupport: ['google', 'leaflet', 'maplibre'],
      sourceType: 'markers',
      source: '/api/culture-map?category=local_food',
      interactive: true,
      opacity: 1.0,
      renderOrder: 95,
      parent: 'culture',
      description: 'Litti Chokha, Silao Khaja, Maner Laddu, heritage gastronomy trails',
      style: { markerColor: '#ea580c' },
    },
  ];

  /** Layer group metadata with UI rendering sequence */
  const LAYER_GROUPS = [
    { id: 'terrain', label: 'Terrain', name: 'Terrain', icon: '⛰️', emoji: '⛰️', description: 'Elevation & Relief' },
    { id: 'natural_geography', label: 'Natural Geography', name: 'Natural Geography', icon: '🌿', emoji: '🌿', description: 'Rivers, Forests & Lakes' },
    { id: 'boundaries', label: 'Boundaries', name: 'Boundaries', icon: '🗺️', emoji: '🗺️', description: 'Districts & Borders' },
    { id: 'tourism', label: 'Tourism', name: 'Tourism', icon: '📍', emoji: '📍', description: 'Destinations & Landmarks' },
    { id: 'culture', label: 'Culture', name: 'Culture', icon: '🏺', emoji: '🏺', description: 'Heritage, Arts & Food' },
    { id: 'roads_transport', label: 'Roads & Transport', name: 'Roads & Transport', icon: '🛣️', emoji: '🛣️', description: 'Highways & Railways' },
    { id: 'routes', label: 'Routes', name: 'Routes & Navigation', icon: '🧭', emoji: '🧭', description: 'Navigation & GPS' },
    { id: 'analytics', label: 'Analytics', name: 'Analytics & Heatmaps', icon: '📊', emoji: '📊', description: 'Heatmaps & Density' },
  ];

  /* ── Layer Registry ──────────────────────────────── */

  class LayerRegistry {
    constructor() {
      /** @type {Map<string, LayerDefinition>} */
      this._layers = new Map();

      /** @type {Map<string, Object>} Leaflet layer instances */
      this._leafletLayers = new Map();

      /** @type {Map<string, Object>} Cached GeoJSON data */
      this._dataCache = new Map();

      // Register built-in layers
      LAYER_DEFINITIONS.forEach(def => this._layers.set(def.id, def));
    }

    /**
     * Register a custom layer definition.
     * @param {LayerDefinition} definition
     */
    register(definition) {
      if (!definition.id) throw new Error('Layer must have an id');
      this._layers.set(definition.id, definition);
    }

    /**
     * Get a layer definition by ID.
     * @param {string} id
     * @returns {LayerDefinition|undefined}
     */
    get(id) {
      return this._layers.get(id);
    }

    /** @returns {LayerDefinition[]} */
    getAll() {
      return Array.from(this._layers.values());
    }

    /**
     * Get all layers in a specific group.
     * @param {string} groupId
     * @returns {LayerDefinition[]}
     */
    getByGroup(groupId) {
      return this.getAll().filter(l => l.group === groupId);
    }

    /**
     * Get layers that support a specific engine.
     * @param {'leaflet'|'maplibre'} engine
     * @returns {LayerDefinition[]}
     */
    getByEngine(engine) {
      return this.getAll().filter(l => l.engineSupport.includes(engine));
    }

    /**
     * Fetch and cache GeoJSON data for a layer.
     * @param {string} layerId
     * @returns {Promise<Object>} GeoJSON FeatureCollection
     */
    async fetchData(layerId) {
      const def = this.get(layerId);
      if (!def || !def.source) return null;

      // Return cached data if available
      if (this._dataCache.has(layerId)) {
        return this._dataCache.get(layerId);
      }

      try {
        const response = await fetch(def.source);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        this._dataCache.set(layerId, data);
        return data;
      } catch (err) {
        console.error(`[LayerRegistry] Failed to fetch data for layer '${layerId}':`, err);
        return null;
      }
    }

    /**
     * Check if data for a layer has been cached.
     * @param {string} layerId
     * @returns {boolean}
     */
    hasData(layerId) {
      return this._dataCache.has(layerId);
    }

    /**
     * Get cached data for a layer synchronously.
     * @param {string} layerId
     * @returns {Object|undefined}
     */
    getData(layerId) {
      return this._dataCache.get(layerId);
    }

    /**
     * Get all top-level root layers (parent === null).
     * @returns {LayerDefinition[]}
     */
    getRoots() {
      return this.getAll().filter(l => !l.parent);
    }

    /**
     * Get all child layer definitions for a given parent layer ID.
     * @param {string} parentId
     * @returns {LayerDefinition[]}
     */
    getChildren(parentId) {
      const parent = this.get(parentId);
      if (!parent || !parent.children) {
        return this.getAll().filter(l => l.parent === parentId);
      }
      return parent.children.map(id => this.get(id)).filter(Boolean);
    }

    /**
     * Check if a layer is a parent with children.
     * @param {string} layerId
     * @returns {boolean}
     */
    isParent(layerId) {
      const def = this.get(layerId);
      return !!(def && def.children && def.children.length > 0);
    }

    /**
     * Get parent layer definition for a child.
     * @param {string} childId
     * @returns {LayerDefinition|null}
     */
    getParent(childId) {
      const child = this.get(childId);
      if (!child || !child.parent) return null;
      return this.get(child.parent) || null;
    }

    /**
     * Store a Leaflet layer instance for later management.
     * @param {string} layerId
     * @param {Object} leafletLayer - L.geoJSON / L.layerGroup instance
     */
    setLeafletLayer(layerId, leafletLayer) {
      this._leafletLayers.set(layerId, leafletLayer);
    }

    /**
     * Get the Leaflet layer instance.
     * @param {string} layerId
     * @returns {Object|undefined}
     */
    getLeafletLayer(layerId) {
      return this._leafletLayers.get(layerId);
    }

    /**
     * Remove a Leaflet layer instance.
     * @param {string} layerId
     */
    removeLeafletLayer(layerId) {
      this._leafletLayers.delete(layerId);
    }
  }

  // Exports
  root.HY_LAYERS = LAYER_DEFINITIONS;
  root.HY_LAYER_GROUPS = LAYER_GROUPS;
  root.HYTileSources = TILE_SOURCES;
  root.HYLayerDefinitions = LAYER_DEFINITIONS;
  root.HYLayerGroups = LAYER_GROUPS;
  root.HYLayerRegistry = new LayerRegistry();
  root.HYLayerRegistryClass = LayerRegistry;

})(window);
