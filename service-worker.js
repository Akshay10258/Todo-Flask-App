const CACHE_NAME = "todo-app-cache-v1";
const urlsToCache = [
  "/",  
  "/static/manifest.json",
  "/static/test.js",
  "/static/icons/icon-192x192.png",
  "/static/icons/icon-512x512.png",
];
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache))
  );
});


self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => response || fetch(event.request))
  );
});