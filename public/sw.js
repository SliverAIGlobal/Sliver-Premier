const CACHE_VERSION = 'v1';
const CACHE_NAME = `prism9-${CACHE_VERSION}`;

const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/favicon.svg',
  '/offline.html',
  '/pkg/prism9_wasm_bg.wasm',
  '/pkg/prism9_wasm.js',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS))
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((names) =>
      Promise.all(names.filter((name) => name !== CACHE_NAME).map((name) => caches.delete(name)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);

  if (url.pathname.startsWith('/api/')) {
    event.respondWith(handleApiRequest(event));
  } else if (url.pathname.endsWith('.wasm')) {
    event.respondWith(staleWhileRevalidate(event));
  } else {
    event.respondWith(networkFirst(event));
  }
});

async function handleApiRequest(event) {
  const cache = await caches.open('api-cache');
  const cached = await cache.match(event.request);

  if (cached) {
    const timestamp = cached.headers.get('x-cache-timestamp');
    if (timestamp && (Date.now() - parseInt(timestamp, 10)) < 60000) {
      return cached.clone();
    }
  }

  try {
    const networkResponse = await fetch(event.request);
    if (networkResponse.ok) {
      const clone = networkResponse.clone();
      const headers = new Headers(clone.headers);
      headers.set('x-cache-timestamp', Date.now().toString());
      await cache.put(event.request, new Response(clone.body, { headers }));
    }
    return networkResponse;
  } catch {
    return cached || new Response(JSON.stringify({ error: 'Network error and no cached API response available' }), { status: 503 });
  }
}

async function staleWhileRevalidate(event) {
  const cache = await caches.open(CACHE_NAME);
  const cached = await cache.match(event.request);
  const fetchPromise = fetch(event.request)
    .then((response) => {
      if (response.ok) cache.put(event.request, response.clone());
      return response;
    })
    .catch(() => cached);

  return cached || fetchPromise;
}

async function networkFirst(event) {
  try {
    const response = await fetch(event.request);
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(event.request, response.clone());
    }
    return response;
  } catch {
    return (await caches.match(event.request)) || (await caches.match('/offline.html'));
  }
}
