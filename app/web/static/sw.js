self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(cacheName).then(cache => {
            cache.addAll(assets);
        })
    );
});

self.addEventListener('activate', event => {
    console.log('Service worker activation sucessful');
})

self.addEventListener('fetch', event => {
    console.log(event);
})

const cacheName = 'initialCache';
const assets = [
    '/',
	'/index.html',
    '/mapping.js',
	'/map.css',
    '/icons/icon-144.png',
    '/icons/icon-192.png'

];




