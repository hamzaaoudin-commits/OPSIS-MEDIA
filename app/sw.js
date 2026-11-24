/* OPSIS service worker — généré, version 3a4d4f26be */
const V='opsis-3a4d4f26be',SHELL=['./','index.html','manifest.webmanifest','icons/icon-192.png'],OFFLINE=["data/content.json","data/covers.json","fonts/atkinson-hyperlegible-latin-400-normal.woff2","fonts/atkinson-hyperlegible-latin-700-normal.woff2","fonts/big-shoulders-display-latin-600-normal.woff2","fonts/big-shoulders-display-latin-800-normal.woff2","fonts/big-shoulders-display-latin-900-normal.woff2","fonts/eb-garamond-latin-400-normal.woff2","fonts/eb-garamond-latin-500-normal.woff2","fonts/hanken-grotesk-latin-400-normal.woff2","fonts/hanken-grotesk-latin-500-normal.woff2","fonts/hanken-grotesk-latin-600-normal.woff2","fonts/hanken-grotesk-latin-700-normal.woff2","fonts/lexend-latin-300-normal.woff2","fonts/lexend-latin-400-normal.woff2","fonts/lexend-latin-500-normal.woff2","fonts/literata-latin-400-normal.woff2","fonts/literata-latin-500-normal.woff2","fonts/lora-latin-400-italic.woff2","fonts/lora-latin-400-normal.woff2","fonts/lora-latin-500-normal.woff2","fonts/merriweather-latin-300-normal.woff2","fonts/merriweather-latin-400-normal.woff2","fonts/merriweather-latin-700-normal.woff2","fonts/newsreader-latin-400-italic.woff2","fonts/newsreader-latin-400-normal.woff2","fonts/newsreader-latin-500-normal.woff2","fonts/source-serif-4-latin-400-normal.woff2","fonts/source-serif-4-latin-500-normal.woff2"];
/* installation : la coque, puis toutes les histoires et les polices, pour lire sans réseau */
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(SHELL).then(()=>c.addAll(OFFLINE).catch(()=>{}))).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x.startsWith('opsis-')&&x!==V).map(x=>caches.delete(x)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{
  const r=e.request,u=new URL(r.url);
  if(r.method!=='GET')return;
  /* l'API et l'authentification ne sont jamais mises en cache */
  if(u.pathname.indexOf('/rest/v1/')>=0||u.pathname.indexOf('/auth/v1/')>=0)return;
  /* demande explicite de mise à jour : on va chercher la dernière version sur le réseau et on la range */
  if(r.cache==='reload'&&u.origin===location.origin){e.respondWith(fetch(r).then(x=>{if(x.ok){const y=x.clone();caches.open(V).then(c=>c.put(r,y));}return x;}));return;}
  if(u.origin===location.origin&&u.pathname.indexOf('/data/')>=0){
    /* données : on répond tout de suite avec la copie locale, et on la rafraîchit en arrière-plan */
    e.respondWith(caches.open(V).then(c=>c.match(r).then(m=>{const n=fetch(r).then(x=>{if(x.ok)c.put(r,x.clone());return x;}).catch(()=>m);return m||n;})));return;
  }
  if(u.origin===location.origin||u.hostname.indexOf('fonts.g')===0){
    e.respondWith(caches.open(V).then(c=>c.match(r).then(m=>m||fetch(r).then(x=>{if(x.ok)c.put(r,x.clone());return x;}).catch(()=>m))));
  }
});
