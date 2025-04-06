const CACHE_NAME = "todo-app-cache-v1";
const urlsToCache = [
  "/",  
  "/static/manifest.json",
  "/static/test.js",
  "/static/icons/icon-192x192.png",
  "/static/icons/icon-512x512.png",
];

// Install and cache all assets
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

// Intercept fetch and serve from cache or fetch fallback
self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        return response || fetch(event.request).catch(() =>
          // Offline fallback for HTML requests
          event.request.mode === 'navigate' ? caches.match("/") : null
        );
      })
  );
});

// Clean up old caches if needed
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keyList =>
      Promise.all(
        keyList.filter(key => key !== CACHE_NAME)
          .map(key => caches.delete(key))
      )
    )
  );
});
