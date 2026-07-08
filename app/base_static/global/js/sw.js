const CACHE_NAME = 'social-network-v1';
const STATIC_ASSETS = [
    // Array of static files to cache initially if you want
];

self.addEventListener('install', (event) => {
    // Force the waiting service worker to become the active service worker
    self.skipWaiting();
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('[Service Worker] Caching App Shell');
                return cache.addAll(STATIC_ASSETS);
            })
    );
});

self.addEventListener('activate', (event) => {
    // Delete old caches when a new service worker is activated
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('[Service Worker] Removing old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    // Tell the active service worker to take control of the page immediately
    self.clients.claim();
});

self.addEventListener('fetch', (event) => {
    // Only intercept GET requests
    if (event.request.method !== 'GET') return;
    
    // Ignore non-http/https requests (e.g. chrome-extension://)
    if (!event.request.url.startsWith('http')) return;

    const requestUrl = new URL(event.request.url);

    // Strategy: Stale-While-Revalidate for static assets (CSS, JS, Images, Fonts)
    if (
        requestUrl.pathname.startsWith('/static/') ||
        requestUrl.pathname.startsWith('/media/') ||
        event.request.destination === 'style' ||
        event.request.destination === 'script' ||
        event.request.destination === 'image' ||
        event.request.destination === 'font'
    ) {
        event.respondWith(
            caches.match(event.request).then(cachedResponse => {
                const fetchPromise = fetch(event.request).then(networkResponse => {
                    // Update the cache with the new network response in the background
                    if (networkResponse.ok) {
                        caches.open(CACHE_NAME).then(cache => {
                            cache.put(event.request, networkResponse.clone());
                        });
                    }
                    return networkResponse;
                }).catch(() => {
                    // Network fetch failed, we will just rely on the cached response if it exists
                });

                // Return the cached response immediately if available, otherwise wait for network
                return cachedResponse || fetchPromise;
            })
        );
        return;
    }

    // Strategy: Network First, falling back to cache for HTML Navigation and everything else
    if (event.request.mode === 'navigate' || event.request.destination === 'document') {
        event.respondWith(
            fetch(event.request)
                .then(networkResponse => {
                    return caches.open(CACHE_NAME).then(cache => {
                        cache.put(event.request, networkResponse.clone());
                        return networkResponse;
                    });
                })
                .catch(() => {
                    return caches.match(event.request).then(cachedResponse => {
                        if (cachedResponse) {
                            return cachedResponse;
                        }
                        // Optionally return a fallback offline page here
                        // return caches.match('/offline/');
                    });
                })
        );
        return;
    }

    // Default Fallback
    event.respondWith(
        fetch(event.request).catch(() => caches.match(event.request))
    );
});
