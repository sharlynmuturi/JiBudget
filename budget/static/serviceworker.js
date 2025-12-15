const CACHE_NAME = 'jibudget-cache-v1';
const OFFLINE_URL = '/static/budget/offline.html';

const urlsToCache = [
  '/',
  OFFLINE_URL,
  '/static/manifest.json',
  '/static/icons/logoicon-192x192.png',
  '/static/icons/icon-192x192.png',
  '/static/icons/logoicon-512x512.png',
  '/static/icons/icon-512x512.png',
  '/static/budget/screenshots/nairobi-hero.jpg',
  '/static/budget/screenshots/transactions111.jpg',
  '/static/budget/screenshots/transactions222.jpg',
  '/static/budget/screenshots/budgets.jpg',
  '/static/budget/screenshots/budgets2.jpg',
  '/static/budget/screenshots/wallets111.jpg',
  '/static/budget/screenshots/savings111.jpg',
  '/static/budget/screenshots/reports11.jpg',
  '/static/budget/screenshots/reports222.jpg',
  '/static/budget/screenshots/dashboardslide4.png',
  '/static/budget/screenshots/transactionsslide4.png',
  '/static/budget/screenshots/budgetsslide4.png',
  '/static/budget/screenshots/walletsslide4.png',
  '/static/budget/screenshots/savingsslide4.png',
  '/static/budget/screenshots/reportsslide4.png',
  '/static/budget/screenshots/vitalstour.png',
  '/static/budget/screenshots/myvitals.png',
  '/static/budget/screenshots/vitalshome.png',
  '/static/budget/screenshots/dashboardtour4.png',

  '/static/budget/screenshots/vitalstour1.png',
  '/static/budget/screenshots/myvitals1.png',
  '/static/budget/screenshots/vitalshome1.png',
  '/static/budget/screenshots/mytransactions10.png',
  '/static/budget/screenshots/mybudgets7.png',
  '/static/budget/screenshots/myvitals2.png',
  '/static/budget/screenshots/myvitals4.png',

  '/static/budget/screenshots/loantour.png',
  '/static/budget/screenshots/myloans.png',
 
  '/static/budget/screenshots/myloans1.png',
  '/static/budget/screenshots/mytransactions11.png',
    '/static/budget/screenshots/mytransactions12.png',

  '/static/budget/screenshots/mybudgets8.png',
  '/static/budget/screenshots/myvitals3.png',
  '/static/budget/screenshots/mydashboard8.png',
  '/static/budget/screenshots/mydashboard9.png',
  '/static/budget/screenshots/mydashboard10.png',

  '/static/budget/screenshots/mydashboard.png',
  '/static/budget/screenshots/mytransactions.png',
  '/static/budget/screenshots/mybudgets.png',
  '/static/budget/screenshots/mywallets.png',
  '/static/budget/screenshots/mysavings.png',
  '/static/budget/screenshots/myinsights.png',
  '/static/budget/screenshots/mytransactions7.png',
  '/static/budget/screenshots/mytransactions8.png',
  '/static/budget/screenshots/mybudgets5.png',
  '/static/budget/screenshots/myinsights6.png',
  '/static/budget/screenshots/mysavings4.png',

  '/static/budget/screenshots/mytransactions5.png',
  '/static/budget/screenshots/transactionstour1.png',
  '/static/budget/screenshots/transactionstour2.png',
  '/static/budget/screenshots/transactionstour3.png',
  '/static/budget/screenshots/transactionstour4.png',
  '/static/budget/screenshots/transactionstour5.png',
  '/static/budget/screenshots/transactionstour6.png',

  '/static/budget/screenshots/tipstour.png',
  '/static/budget/screenshots/tipstour1.png',
  '/static/budget/screenshots/tipstour2.png',
  '/static/budget/screenshots/tipstour3.png',
  '/static/budget/screenshots/tipstour4.png',
  '/static/budget/screenshots/tipstour5.png',
  '/static/budget/screenshots/tipstour6.png',
  '/static/budget/screenshots/tipstour7.png',
  '/static/budget/screenshots/tipstour8.png',
  '/static/budget/screenshots/tipstour9.png',
  '/static/budget/screenshots/tipstour10.png',
  '/static/budget/screenshots/tipstour11.png',
  '/static/budget/screenshots/tipstour12.png',

  '/static/budget/screenshots/savingstour6.png',

  '/static/budget/screenshots/mydashboard3.png',
  '/static/budget/screenshots/mytransactions3.png',
  '/static/budget/screenshots/mybudgets3.png',
  '/static/budget/screenshots/mywallets3.png',
  '/static/budget/screenshots/myinsights3.png',
  '/static/budget/screenshots/myinsights5.png',
  '/static/budget/screenshots/transactionshome.png',
  '/static/budget/screenshots/transactionshome1.png',
  '/static/budget/screenshots/budgetshome.png',
  '/static/budget/screenshots/budgetshome1.png',
  '/static/budget/screenshots/budgetshome2.png',


  '/static/budget/screenshots/insightstour7.png',
  '/static/budget/screenshots/transactionshome2.png',
  '/static/budget/screenshots/savingshome.png',
  '/static/budget/screenshots/savingshome1.png',
  '/static/budget/screenshots/transactionshome3.png',
  '/static/budget/screenshots/transactionshome4.png',

  '/static/budget/screenshots/mytransactions4.png',
  '/static/budget/screenshots/mydashboard1.png',
  '/static/budget/screenshots/mydashboard4.png',
  '/static/budget/screenshots/mydashboard5.png',
  '/static/budget/screenshots/dashboardtour2.png',
  '/static/budget/screenshots/dashboardtour3.png',
  '/static/budget/screenshots/mydashboard6.png',
  '/static/budget/screenshots/mywallets4.png',
  '/static/budget/screenshots/walletstour1.png',
  '/static/budget/screenshots/walletstour2.png',
  '/static/budget/screenshots/walletstour3.png',
  
  '/static/budget/screenshots/mydashboard7.png',
  '/static/budget/screenshots/mytransactions6.png',
  '/static/budget/screenshots/mybudgets4.png',
  '/static/budget/screenshots/mywallets5.png',
  '/static/budget/screenshots/mysavings2.png',
  '/static/budget/screenshots/myinsights4.png',
  '/static/budget/screenshots/mysavings3.png',

  '/static/budget/screenshots/mytransactions1.png',
  '/static/budget/screenshots/mybudgets1.png',
  '/static/budget/screenshots/mywallets1.png',
  '/static/budget/screenshots/mysavings1.png',
  '/static/budget/screenshots/myinsights1.png',
  '/static/budget/screenshots/myinsights2.png',
  '/static/budget/screenshots/mydashboard2.png',
  '/static/budget/screenshots/mywallets2.png',
  '/static/budget/screenshots/mytransactions2.png',
  '/static/budget/screenshots/savingsphone10.png',
  '/static/budget/screenshots/budgetstour0.png',
  '/static/budget/screenshots/dashboardtour0.png',
  '/static/budget/screenshots/dashboardtour1.png',
  '/static/budget/screenshots/insightstour.png',
  '/static/budget/screenshots/insightstour2.png',
  '/static/budget/screenshots/insightstour3.png',
  '/static/budget/screenshots/insightstour4.png',
  '/static/budget/screenshots/insightstour6.png',

  '/static/budget/screenshots/myinvestment.png',
  '/static/budget/screenshots/investmenthome.png',

  '/static/budget/screenshots/mydashboard11.png',
  '/static/budget/screenshots/mytransactions13.png',
  '/static/budget/screenshots/myinvestment1.png',
  '/static/budget/screenshots/myloans2.png',
  '/static/budget/screenshots/myvitals5.png',


  '/static/budget/screenshots/savingsphone.png',
  '/static/budget/screenshots/savingsphone1.png',
  '/static/budget/screenshots/savingsphone2.png',
  '/static/budget/screenshots/image1.jpg',
  '/static/budget/screenshots/image2.jpg',
  '/static/budget/screenshots/image5.jpg',
  '/static/budget/screenshots/image6.jpg',
  '/static/budget/screenshots/image7.jpg',
  '/static/budget/screenshots/image8.jpg',

  '/static/budget/screenshots/insights0.png',

  '/static/budget/screenshots/logoicon.ico',
  '/static/budget/screenshots/favicon5.ico'
];

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      console.log('[ServiceWorker] Caching assets');
      return cache.addAll(urlsToCache);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(name) {
          if (name !== CACHE_NAME) {
            console.log('[ServiceWorker] Deleting old cache:', name);
            return caches.delete(name);
          }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // If the request succeeds, clone it and cache it (optional)
        return response;
      })
      .catch(() => {
        // If the request fails (i.e. offline), serve fallback
        return caches.match(event.request).then(cachedResponse => {
          return cachedResponse || caches.match('/offline.html');  // your custom fallback
        });
      })
  );
});



