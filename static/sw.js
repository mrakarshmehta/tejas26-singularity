// HiddenYatra Service Worker - Offline Caching for Regional Discovery & Traveler Safety
const CACHE_NAME = 'hiddenyatra-v7';
const STATIC_ASSETS = [
  '/',
  '/offline',
  '/safety',
  '/transport',
  '/circuits',
  '/festivals',
  '/crafts',
  '/gastronomy',
  '/wildlife',
  '/virtual-tours',
  '/volunteer',
  '/static/css/main.min.css',
  '/static/css/components.min.css',
  '/static/css/animations.min.css',
  '/static/js/app.min.js',
  '/static/icon-192.png',
  '/static/icon-512.png',
];

// Install - cache static assets & essential offline guides
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting();
});

// Activate - clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    })
  );
  self.clients.claim();
});

// Fetch - network first, fallback to cache
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);
  // Skip API requests and admin pages
  if (url.pathname.startsWith('/api/') || url.pathname.startsWith('/admin/')) return;

  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          if (response.ok) {
            const copy = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
          }
          return response;
        })
        .catch(() => {
          return caches.match(event.request).then((cached) => cached || caches.match('/offline'));
        })
    );
    return;
  }

  event.respondWith(
    fetch(event.request)
      .then((response) => {
        if (response.ok && url.pathname.startsWith('/static/')) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
        }
        return response;
      })
      .catch(() => {
        return caches.match(event.request);
      })
  );
});