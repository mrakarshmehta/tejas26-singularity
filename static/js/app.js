/* ═══════════════════════════════════════════════
   HiddenYatra — App JavaScript v2.0
   Theme, search, scroll, animations, carousel
   ═══════════════════════════════════════════════ */

(function() {
  'use strict';

  // ── THEME TOGGLE ──
  const themeToggle = document.getElementById('theme-toggle');
  const html = document.documentElement;

  function setTheme(theme) {
    html.setAttribute('data-theme', theme);
    localStorage.setItem('hy-theme', theme);
    // Update browser chrome color
    const metaTC = document.getElementById('meta-theme-color');
    if (metaTC) metaTC.setAttribute('content', theme === 'dark' ? '#000000' : '#FF7A18');
  }

  const saved = localStorage.getItem('hy-theme');
  if (saved) setTheme(saved);
  else setTheme('light');

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const current = html.getAttribute('data-theme');
      setTheme(current === 'dark' ? 'light' : 'dark');
    });
  }

  // ── MOBILE MENU ──
  const mobileToggle = document.getElementById('mobile-toggle');
  const navLinks = document.getElementById('nav-links');

  if (mobileToggle && navLinks) {
    mobileToggle.addEventListener('click', () => {
      navLinks.classList.toggle('active');
      mobileToggle.classList.toggle('active');
    });

    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('active');
        mobileToggle.classList.remove('active');
      });
    });
  }

  // ── DROPDOWNS (PROFILE & DISCOVER) ──
  const profileDropdown = document.getElementById('nav-profile-dropdown');
  const profileBtn = document.getElementById('profile-dropdown-btn');
  const discoverDropdown = document.getElementById('nav-discover-dropdown');
  const discoverBtn = document.getElementById('discover-dropdown-btn');

  if (profileBtn && profileDropdown) {
    profileBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (discoverDropdown) {
        discoverDropdown.classList.remove('open');
        if (discoverBtn) discoverBtn.setAttribute('aria-expanded', 'false');
      }
      profileDropdown.classList.toggle('open');
    });

    document.addEventListener('click', (e) => {
      if (!profileDropdown.contains(e.target)) {
        profileDropdown.classList.remove('open');
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') profileDropdown.classList.remove('open');
    });
  }

  if (discoverBtn && discoverDropdown) {
    discoverBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (profileDropdown) profileDropdown.classList.remove('open');
      const isOpen = discoverDropdown.classList.toggle('open');
      discoverBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    document.addEventListener('click', (e) => {
      if (!discoverDropdown.contains(e.target)) {
        discoverDropdown.classList.remove('open');
        discoverBtn.setAttribute('aria-expanded', 'false');
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        discoverDropdown.classList.remove('open');
        discoverBtn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // ── NAVBAR SCROLL ──
  const navbar = document.getElementById('navbar');

  window.addEventListener('scroll', () => {
    const scrollY = window.scrollY;
    if (navbar) {
      navbar.classList.toggle('scrolled', scrollY > 50);
    }

    const scrollBtn = document.getElementById('scroll-top-btn');
    if (scrollBtn) {
      scrollBtn.classList.toggle('visible', scrollY > 400);
    }
  }, { passive: true });

  // Scroll to top
  const scrollTopBtn = document.getElementById('scroll-top-btn');
  if (scrollTopBtn) {
    scrollTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ── HTML ESCAPE UTILITY (XSS prevention) ──
  function _esc(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // ── SEARCH: Handled by search.js module ──

  // ── SCROLL REVEAL ──
  const revealSelectors = '.reveal, .reveal-left, .reveal-right, .reveal-scale';
  const revealElements = document.querySelectorAll(revealSelectors);
  if (revealElements.length > 0) {
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

    revealElements.forEach(el => revealObserver.observe(el));
  }

  // ── FLASH MESSAGES AUTO-DISMISS ──
  document.querySelectorAll('.flash-message').forEach(msg => {
    setTimeout(() => {
      msg.style.opacity = '0';
      msg.style.transform = 'translateX(100%)';
      setTimeout(() => msg.remove(), 300);
    }, 5000);
  });

  // ── BUTTON RIPPLE EFFECT ──
  document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      const ripple = document.createElement('span');
      ripple.classList.add('btn-ripple');
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      ripple.style.width = ripple.style.height = size + 'px';
      ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
      ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';
      this.appendChild(ripple);
      setTimeout(() => ripple.remove(), 600);
    });
  });

  // ── MOBILE BOTTOM NAV ACTIVE STATE ──
  const currentPath = window.location.pathname;
  document.querySelectorAll('.mobile-nav-item').forEach(item => {
    item.classList.remove('active');
    const href = item.getAttribute('href');
    if (currentPath === href || (href === '/' && currentPath === '/')) {
      item.classList.add('active');
    }
  });
  // ── ANIMATED STAT COUNTERS ──
  const statNumbers = document.querySelectorAll('.stat-number[data-target]');
  if (statNumbers.length) {
    const counterObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.dataset.target) || 0;
          const duration = 1500;
          const start = performance.now();
          function tick(now) {
            const elapsed = now - start;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            el.textContent = Math.floor(eased * target);
            if (progress < 1) requestAnimationFrame(tick);
            else el.textContent = target;
          }
          requestAnimationFrame(tick);
          counterObserver.unobserve(el);
        }
      });
    }, { threshold: 0.5 });
    statNumbers.forEach(el => counterObserver.observe(el));
  }

})();

// ── CAROUSEL (global) ──
function scrollCarousel(id, direction) {
  const track = document.getElementById(id);
  if (!track) return;
  const cardWidth = track.querySelector('.place-card')?.offsetWidth || 340;
  track.scrollBy({ left: direction * (cardWidth + 24), behavior: 'smooth' });
}


// Network Status Monitor
window.addEventListener('online', function() {
  console.log('[Network] Back online');
  document.body.classList.remove('is-offline');
});

window.addEventListener('offline', function() {
  console.log('[Network] Connection lost');
  document.body.classList.add('is-offline');
});


// ── MULTILINGUAL AUDIO GUIDE CONTROLLER ──
(function() {
  let isPlaying = false;
  let currentSpeed = 1.0;
  const speeds = [1.0, 1.25, 1.5];
  let speedIdx = 0;

  window.HY_toggleAudioPlay = function() {
    const btn = document.getElementById('audio-play-btn');
    if (!btn) return;
    isPlaying = !isPlaying;
    if (isPlaying) {
      btn.textContent = '⏸ Pause Audio';
      btn.style.background = '#059669';
    } else {
      btn.textContent = '▶ Play Audio';
      btn.style.background = 'var(--accent-orange, #ff7a18)';
    }
  };

  window.HY_switchAudioLang = function(lang) {
    console.log('[AudioGuide] Switching language to:', lang);
    const transcriptEl = document.getElementById('audio-transcript-text');
    if (!transcriptEl) return;
    if (lang === 'hi') {
      transcriptEl.textContent = 'लोड हो रहा है... ऐतिहासिक वृत्तांत और पावन इतिहास।';
    } else if (lang === 'bho') {
      transcriptEl.textContent = 'सुनीं भोजपुरी में... एह ऐतिहासिक स्थल के पावन कथा।';
    } else {
      transcriptEl.textContent = 'Loading audio narration and verified historical records...';
    }
  };

  window.HY_toggleAudioSpeed = function() {
    speedIdx = (speedIdx + 1) % speeds.length;
    currentSpeed = speeds[speedIdx];
    const btn = document.getElementById('audio-speed-btn');
    if (btn) btn.textContent = currentSpeed + 'x';
  };
})();
