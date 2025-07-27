const CACHE_NAME = 'bluewave-cache-v1';
const ASSETS_TO_CACHE = [
  '/',                                 // root HTML
  '/static/css/main.css',              // your main stylesheet
  '/static/js/main.js',                // your main JS bundle
  '/static/icons/icon-192.png',        // PWA icons
  '/static/icons/icon-512.png',
  // add any other static assets you want cached offline…
];

// Install event: cache files
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(ASSETS_TO_CACHE))
  );
});

// Activate event: clean up old caches (optional but recommended)
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(key => key !== CACHE_NAME)
            .map(key => caches.delete(key))
      )
    )
  );
});

// Fetch event: serve from cache, fall back to network
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(cached => cached || fetch(event.request))
  );
});
