// Search autocomplete request abort controller and sequence tracking
let activeSearchAbortController = null;
let searchSequenceNumber = 0;

/**
 * HiddenYatra — Production-Grade Ultimate AI Search Module (Phase 2.5)
 * Requirements fulfilled:
 *   1. Intelligent Search API integration
 *   2. Instant results with 250ms debounce
 *   3. Modern Google Maps / Booking.com style dropdown
 *   4. Cards with Cover image, Name, Category icon, District, State, Rating, Distance, Free badge
 *   5. Match word highlighting (<mark>)
 *   6. Loading skeleton animation while searching
 *   7. "No results found" with suggestions
 *   8. "Did you mean..." typo corrections
 *   9. Recent Searches (localStorage)
 *  10. Trending / Popular Searches
 *  11. Keyboard support (Up, Down, Enter, Esc, Tab)
 *  12. Mobile responsive search dropdown
 *  13. Click outside closes dropdown
 *  14. Client-side caching of responses to eliminate duplicate API calls
 *  15. Typo tolerance (Jamuii, Rajgirr, Bodhgya, Gidheshwar)
 *  16. Hindi + Roman Hindi support
 *  17. Natural language search ("best temple in jamui", "waterfall near me", "picnic place", etc.)
 *  18. Search latency indicator ("Results in X ms")
 *  19. Accessibility (ARIA combobox, screen reader labels, WCAG AA focus)
 */
(function () {
  'use strict';

  const DEBOUNCE_MS = 250;
  const MIN_QUERY_LEN = 1;
  const MAX_RECENT = 5;
  const STORAGE_KEY = 'hy_recent_searches';
  const MAX_QUERY_LEN = 200;

  // Client-side response cache (Map: url -> data)
  const clientCache = new Map();
  const CACHE_MAX_SIZE = 100;

  function getCachedResponse(url) {
    return clientCache.get(url) || null;
  }

  function setCachedResponse(url, data) {
    if (clientCache.size >= CACHE_MAX_SIZE) {
      const firstKey = clientCache.keys().next().value;
      clientCache.delete(firstKey);
    }
    clientCache.set(url, data);
  }

  // ── CATEGORY EMOJI ──
  const EMOJI = {
    tourist_spot: '📸', temple: '🛕', food_place: '🍽️', hidden_gem: '💎',
    nature: '🌿', historical: '🏛️', beach: '🏖️', mountain: '⛰️',
    market: '🛍️', adventure: '🧗', cultural: '🎭', waterfall: '💧',
    lake: '🌊', other: '📌', district: '🗺️', state: '🏛️',
    block: '🏘️', food: '🍛', service: '🏨',
    hospital: '🏥', police_station: '🚔', bus_stand: '🚌',
    railway_station: '🚂', hotel: '🏨', restaurant: '🍽️',
    petrol_pump: '⛽', pharmacy: '💊', atm: '🏧', parking: '🅿️',
  };

  const TYPE_LABELS = {
    place: 'Place', district: 'District', state: 'State',
    block: 'Block', service: 'Service', food: 'Food',
  };

  // ── UTILITY ──
  function esc(str) {
    if (!str) return '';
    const d = document.createElement('div');
    d.textContent = str;
    return d.innerHTML;
  }

  function getRecentSearches() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]').slice(0, MAX_RECENT); }
    catch { return []; }
  }

  function saveRecentSearch(query) {
    if (!query || query.length < 2) return;
    try {
      let recent = getRecentSearches().filter(r => r.toLowerCase() !== query.toLowerCase());
      recent.unshift(query);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(recent.slice(0, MAX_RECENT)));
    } catch { /* ignore */ }
  }

  function clearRecentSearches() {
    try { localStorage.removeItem(STORAGE_KEY); } catch { /* ignore */ }
  }

  // ── USER LOCATION ──
  let userLocation = null;

  function getUserLocation() {
    return new Promise((resolve) => {
      if (window.HY && window.HY.userLoc) {
        userLocation = window.HY.userLoc;
        resolve(userLocation);
        return;
      }
      if (!navigator.geolocation) { resolve(null); return; }
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          userLocation = { lat: pos.coords.latitude, lng: pos.coords.longitude };
          resolve(userLocation);
        },
        () => resolve(null),
        { timeout: 5000, enableHighAccuracy: false }
      );
    });
  }

  // ── SEARCH CONTROLLER ──
  class SearchController {
    constructor(inputEl, dropdownEl, formEl, options = {}) {
      this.input = inputEl;
      this.dropdown = dropdownEl;
      this.form = formEl;
      this.timer = null;
      this.activeIdx = -1;
      this.results = [];
      this.isOpen = false;
      this.abortCtrl = null;
      this.activeFilters = {};
      this.isHero = options.isHero || false;

      this._bindEvents();
    }

    _bindEvents() {
      this.input.addEventListener('input', () => this._onInput());
      this.input.addEventListener('keydown', (e) => this._onKeydown(e));
      this.input.addEventListener('focus', () => {
        if (this.input.value.trim().length >= MIN_QUERY_LEN) {
          this._onInput();
        } else {
          this._showEmptyState();
        }
      });

      document.addEventListener('click', (e) => {
        if (!e.target.closest('.hy-search-wrapper') && !e.target.closest('.hy-search-dropdown')) {
          this._close();
        }
      });

      if (this.form) {
        this.form.addEventListener('submit', () => {
          const q = this.input.value.trim();
          if (q) saveRecentSearch(q);
        });
      }
    }

    _onInput() {
      clearTimeout(this.timer);
      const q = this.input.value.trim().slice(0, MAX_QUERY_LEN);
      if (q.length < MIN_QUERY_LEN) {
        this._showEmptyState();
        return;
      }
      // Build URL to check cache before showing skeleton
      const url = this._buildSearchUrl(q);
      const cached = getCachedResponse(url);
      if (cached) {
        // Instant render from cache — no skeleton flash
        this.results = cached.results || [];
        this._render(cached);
        return;
      }
      this._showLoading();
      this.timer = setTimeout(() => this._fetchResults(q), DEBOUNCE_MS);
    }

    _showLoading() {
      this.dropdown.innerHTML = `<div class="hy-search-loading">
        <div class="hy-search-spinner"></div>
        <span>Searching places & food...</span>
      </div>`;
      this._open();
    }

    _buildSearchUrl(query) {
      let url = '/api/search/instant?q=' + encodeURIComponent(query) + '&limit=12';
      const f = this.activeFilters;
      if (f.category) url += '&category=' + encodeURIComponent(f.category);
      if (f.district) url += '&district=' + encodeURIComponent(f.district);
      if (f.family_friendly) url += '&family_friendly=1';
      if (f.free_entry) url += '&free_entry=1';
      if (f.has_parking) url += '&has_parking=1';
      if (f.radius_km) url += '&radius_km=' + f.radius_km;
      if (userLocation) {
        url += '&lat=' + userLocation.lat + '&lng=' + userLocation.lng;
      }
      return url;
    }

    async _fetchResults(query) {
      if (this.abortCtrl) this.abortCtrl.abort();
      this.abortCtrl = new AbortController();

      const url = this._buildSearchUrl(query);

      // Check client-side cache first
      const cached = getCachedResponse(url);
      if (cached) {
        this.results = cached.results || [];
        this._render(cached);
        return;
      }

      try {
        const res = await fetch(url, { signal: this.abortCtrl.signal });
        const data = await res.json();
        setCachedResponse(url, data);
        this.results = data.results || [];
        this._render(data);
      } catch (err) {
        if (err.name !== 'AbortError') console.error('Search error:', err);
      }
    }

    _render(data) {
      const results = data.results || [];
      const didYouMean = data.did_you_mean;
      const ms = data.ms;
      const hasFilters = Object.keys(this.activeFilters).length > 0;

      if (results.length === 0 && !didYouMean) {
        this._showNoResults(data.query);
        return;
      }

      let html = '';
      html += this._renderFilterBar();

      if (didYouMean) {
        html += `<div class="hy-search-dym" data-query="${esc(didYouMean)}">
          💡 Did you mean: <strong>${esc(didYouMean)}</strong>
        </div>`;
      }

      if (hasFilters) {
        const filterNames = Object.entries(this.activeFilters)
          .filter(([k, v]) => v)
          .map(([k]) => k.replace('_', ' '))
          .join(', ');
        html += `<div class="hy-search-filter-active">🔽 Filtered by: ${esc(filterNames)} <button class="hy-clear-filters" type="button">✕ Clear</button></div>`;
      }

      html += '<div class="hy-search-results" role="listbox">';
      results.forEach((r, idx) => {
        const emoji = r.category_emoji || EMOJI[r.category] || EMOJI[r.type] || '📍';
        const typeBadge = TYPE_LABELS[r.type] || r.type;
        const subtitle = [r.district_name, r.state_name].filter(Boolean).join(', ');
        const highlighted = r.highlighted_name || esc(r.name);
        const url = r.url || '#';
        const distanceHtml = r.distance_km != null
          ? `<span class="hy-search-distance">📍 ${r.distance_km} km</span>` : '';
        const ratingHtml = r.avg_rating && r.avg_rating > 0
          ? `<span class="hy-search-rating">⭐ ${r.avg_rating.toFixed(1)}</span>` : '';
        const freeTag = r.entry_fee && r.entry_fee.toLowerCase().includes('free')
          ? '<span class="hy-search-free-tag">Free</span>' : '';

        let thumbHtml = `<div class="hy-search-item-icon">${emoji}</div>`;
        if (r.cover_image && r.type === 'place') {
          const imgUrl = r.cover_image.startsWith('http')
            ? r.cover_image
            : '/static/uploads/places/' + r.cover_image;
          thumbHtml = `<div class="hy-search-item-thumb">
            <img src="${esc(imgUrl)}" alt="" loading="lazy" onerror="this.parentElement.innerHTML='${emoji}'">
          </div>`;
        }

        html += `<a href="${esc(url)}" class="hy-search-item" id="hy-opt-${idx}" data-idx="${idx}" data-name="${esc(r.name)}" role="option" aria-selected="false">
          ${thumbHtml}
          <div class="hy-search-item-body">
            <div class="hy-search-item-name">${highlighted}${freeTag}</div>
            <div class="hy-search-item-meta">
              <span class="hy-search-type-badge hy-badge-${r.type}">${typeBadge}</span>
              ${subtitle ? `<span class="hy-search-subtitle">${esc(subtitle)}</span>` : ''}
              ${distanceHtml}${ratingHtml}
            </div>
          </div>
          ${r.match_type === 'fuzzy' || r.match_type === 'phonetic' ? '<span class="hy-search-fuzzy-tag">~' + r.match_type + '</span>' : ''}
        </a>`;
      });
      html += '</div>';

      if (ms !== undefined) {
        html += `<div class="hy-search-footer">${results.length} result${results.length !== 1 ? 's' : ''} in ${ms} ms</div>`;
      }

      this.dropdown.innerHTML = html;
      this.activeIdx = -1;
      this._open();
      this._bindDropdownEvents();
    }

    _renderFilterBar() {
      const filters = [
        { key: 'near_me', label: '📍 Near Me', type: 'toggle' },
        { key: 'category', label: '🏷️ Category', type: 'select' },
        { key: 'family_friendly', label: '👨‍👩‍👧 Family', type: 'toggle' },
        { key: 'free_entry', label: '🆓 Free Entry', type: 'toggle' },
      ];

      let html = '<div class="hy-filter-bar">';
      filters.forEach(f => {
        const isActive = this.activeFilters[f.key];
        html += `<button type="button" class="hy-filter-chip ${isActive ? 'active' : ''}" data-filter="${f.key}">
          ${f.label}
        </button>`;
      });
      html += '</div>';
      return html;
    }

    _bindDropdownEvents() {
      const dym = this.dropdown.querySelector('.hy-search-dym');
      if (dym) {
        dym.addEventListener('click', () => {
          this.input.value = dym.dataset.query;
          this._fetchResults(dym.dataset.query);
        });
      }

      this.dropdown.querySelectorAll('.hy-search-item').forEach(item => {
        item.addEventListener('click', () => saveRecentSearch(this.input.value.trim()));
      });

      this.dropdown.querySelectorAll('.hy-filter-chip').forEach(chip => {
        chip.addEventListener('click', (e) => {
          e.stopPropagation();
          const key = chip.dataset.filter;
          if (key === 'near_me') {
            if (!this.activeFilters.near_me) {
              getUserLocation().then(() => {
                this.activeFilters.near_me = true;
                this.activeFilters.radius_km = 25;
                this._refetch();
              });
            } else {
              delete this.activeFilters.near_me;
              delete this.activeFilters.radius_km;
              this._refetch();
            }
          } else if (key === 'category') {
            this._showCategoryPicker();
          } else {
            this.activeFilters[key] = !this.activeFilters[key];
            if (!this.activeFilters[key]) delete this.activeFilters[key];
            this._refetch();
          }
        });
      });

      const clearBtn = this.dropdown.querySelector('.hy-clear-filters');
      if (clearBtn) {
        clearBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          this.activeFilters = {};
          this._refetch();
        });
      }
    }

    _showCategoryPicker() {
      fetch('/api/search/filters')
        .then(r => r.json())
        .then(data => {
          const cats = data.categories || [];
          let html = '<div class="hy-category-picker">';
          html += '<div class="hy-search-section-title">🏷️ Filter by Category</div>';
          html += `<button type="button" class="hy-cat-option ${!this.activeFilters.category ? 'active' : ''}" data-cat="">All Categories</button>`;
          cats.forEach(c => {
            const isActive = this.activeFilters.category === c.code;
            html += `<button type="button" class="hy-cat-option ${isActive ? 'active' : ''}" data-cat="${esc(c.code)}">${c.emoji} ${esc(c.label)}</button>`;
          });
          html += '</div>';
          this.dropdown.innerHTML = html;
          this._open();

          this.dropdown.querySelectorAll('.hy-cat-option').forEach(btn => {
            btn.addEventListener('click', () => {
              const cat = btn.dataset.cat;
              if (cat) {
                this.activeFilters.category = cat;
              } else {
                delete this.activeFilters.category;
              }
              this._refetch();
            });
          });
        });
    }

    _refetch() {
      const q = this.input.value.trim();
      if (q.length >= MIN_QUERY_LEN) {
        this._fetchResults(q);
      }
    }

    _showNoResults(query) {
      let html = this._renderFilterBar();
      html += `<div class="hy-search-empty">
        <div class="hy-search-empty-icon">🔍</div>
        <div class="hy-search-empty-text">No results for "<strong>${esc(query)}</strong>"</div>
        <div class="hy-search-empty-hint">Try checking your spelling, using different keywords, or searching in Hindi</div>
      </div>`;
      this.dropdown.innerHTML = html;
      this.activeIdx = -1;
      this._open();
      this._bindDropdownEvents();
    }

    _showEmptyState() {
      const recent = getRecentSearches();
      let html = '';

      if (recent.length > 0) {
        html += '<div class="hy-search-section-title">🕐 Recent Searches <button class="hy-clear-recent" type="button">Clear</button></div>';
        html += '<div class="hy-search-recent">';
        recent.forEach(q => {
          html += `<button class="hy-recent-item" type="button" data-query="${esc(q)}">
            <span class="hy-recent-icon">🔍</span>${esc(q)}
          </button>`;
        });
        html += '</div>';
      }

      html += '<div class="hy-search-section-title">⚡ Quick Search</div>';
      html += '<div class="hy-quick-chips">';
      ['🛕 Temples', '⛰️ Hills', '💧 Waterfalls', '🏛️ Historical', '🌿 Nature', '🍽️ Food'].forEach(label => {
        const cat = label.split(' ')[1].toLowerCase();
        html += `<button type="button" class="hy-quick-chip" data-query="${cat}">${label}</button>`;
      });
      html += '</div>';

      html += '<div class="hy-search-section-title">🔥 Popular Places</div>';
      html += '<div class="hy-search-popular" id="hy-search-popular">';
      html += '<div class="hy-search-loading-inline">';
      html += '<div class="hy-search-spinner-sm"></div>';
      html += '<span>Loading popular places...</span>';
      html += '</div></div>';

      this.dropdown.innerHTML = html;
      this.activeIdx = -1;
      this._open();

      this.dropdown.querySelectorAll('.hy-recent-item').forEach(btn => {
        btn.addEventListener('click', () => {
          this.input.value = btn.dataset.query;
          this._fetchResults(btn.dataset.query);
        });
      });

      this.dropdown.querySelectorAll('.hy-quick-chip').forEach(btn => {
        btn.addEventListener('click', () => {
          this.input.value = btn.dataset.query;
          this._fetchResults(btn.dataset.query);
        });
      });

      const clearBtn = this.dropdown.querySelector('.hy-clear-recent');
      if (clearBtn) {
        clearBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          clearRecentSearches();
          this._showEmptyState();
        });
      }

      fetch('/api/search/instant?q=&limit=6')
        .then(r => r.json())
        .then(data => {
          const popEl = document.getElementById('hy-search-popular');
          if (!popEl) return;
          const suggestions = data.suggestions || [];
          if (suggestions.length === 0) {
            popEl.innerHTML = '<div class="hy-search-empty-hint">Start typing to search...</div>';
            return;
          }
          popEl.innerHTML = suggestions.map(s => {
            const emoji = EMOJI[s.category] || '📍';
            return `<a href="${esc(s.url)}" class="hy-popular-item">
              <span class="hy-popular-emoji">${emoji}</span>
              <span class="hy-popular-name">${esc(s.name)}</span>
              ${s.district_name ? `<span class="hy-popular-district">${esc(s.district_name)}</span>` : ''}
            </a>`;
          }).join('');
        })
        .catch(() => {
          const popEl = document.getElementById('hy-search-popular');
          if (popEl) popEl.innerHTML = '<div class="hy-search-empty-hint">Start typing to search...</div>';
        });
    }

    _onKeydown(e) {
      if (!this.isOpen) return;
      const items = this.dropdown.querySelectorAll('.hy-search-item');
      const count = items.length;

      switch (e.key) {
        case 'ArrowDown':
          e.preventDefault();
          this.activeIdx = (this.activeIdx + 1) % count;
          this._highlightItem(items);
          break;
        case 'ArrowUp':
          e.preventDefault();
          this.activeIdx = this.activeIdx <= 0 ? count - 1 : this.activeIdx - 1;
          this._highlightItem(items);
          break;
        case 'Enter':
          if (this.activeIdx >= 0 && this.activeIdx < count) {
            e.preventDefault();
            const href = items[this.activeIdx].getAttribute('href');
            if (href && href !== '#') {
              saveRecentSearch(this.input.value.trim());
              window.location.href = href;
            }
          } else {
            saveRecentSearch(this.input.value.trim());
          }
          break;
        case 'Escape':
          e.preventDefault();
          this._close();
          this.input.blur();
          break;
        case 'Tab':
          this._close();
          break;
      }
    }

    _highlightItem(items) {
      items.forEach((el, i) => {
        const isSel = i === this.activeIdx;
        el.classList.toggle('hy-search-item-active', isSel);
        el.setAttribute('aria-selected', isSel ? 'true' : 'false');
        if (isSel) {
          el.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
          this.input.setAttribute('aria-activedescendant', el.id);
        }
      });
    }


    _open() {
      this.dropdown.classList.add('active');
      this.isOpen = true;
      this.input.setAttribute('aria-expanded', 'true');
      document.body.classList.add('hy-dropdown-open');
    }

    _close() {
      this.dropdown.classList.remove('active');
      this.isOpen = false;
      this.activeIdx = -1;
      this.input.setAttribute('aria-expanded', 'false');
      this.input.removeAttribute('aria-activedescendant');
      document.body.classList.remove('hy-dropdown-open');
    }
  }

  // ── INITIALIZATION ──
  function init() {
    if (window.HY && window.HY.userLoc) {
      userLocation = window.HY.userLoc;
    }

    const navInput = document.getElementById('nav-search-input');
    const navDropdown = document.getElementById('nav-autocomplete');
    const navForm = navInput?.closest('form');
    if (navInput && navDropdown) {
      const navSearch = navInput.closest('.nav-search');
      if (navSearch) navSearch.classList.add('hy-search-wrapper');
      navDropdown.classList.add('hy-search-dropdown');

      navInput.setAttribute('role', 'combobox');
      navInput.setAttribute('aria-expanded', 'false');
      navInput.setAttribute('aria-autocomplete', 'list');
      navInput.setAttribute('aria-haspopup', 'listbox');
      navInput.setAttribute('aria-label', 'Search places, districts, food');

      new SearchController(navInput, navDropdown, navForm);
    }

    const heroInput = document.getElementById('hero-search-input');
    if (heroInput) {
      const heroForm = heroInput.closest('form');
      let heroDropdown = document.getElementById('hero-search-dropdown');
      if (!heroDropdown) {
        heroDropdown = document.createElement('div');
        heroDropdown.id = 'hero-search-dropdown';
        heroDropdown.className = 'hy-search-dropdown';
        // Append to .hero-search (the form), NOT .hero-search-wrapper (the pill)
        // to prevent border-radius clipping
        const heroSearchForm = heroInput.closest('.hero-search');
        const wrapper = heroSearchForm || heroInput.closest('.hero-search-wrapper');
        if (wrapper) {
          wrapper.style.position = 'relative';
          wrapper.classList.add('hy-search-wrapper');
          wrapper.appendChild(heroDropdown);
        }
      }

      heroInput.setAttribute('role', 'combobox');
      heroInput.setAttribute('aria-expanded', 'false');
      heroInput.setAttribute('aria-autocomplete', 'list');
      heroInput.setAttribute('aria-label', 'Search places, districts, food');

      new SearchController(heroInput, heroDropdown, heroForm, { isHero: true });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
