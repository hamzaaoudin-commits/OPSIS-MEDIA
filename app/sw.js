/* OPSIS service worker — généré, version 584640d192 */
const V='opsis-584640d192',SHELL=['./','index.html','manifest.webmanifest','icons/icon-192.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x.startsWith('opsis-')&&x!==V).map(x=>caches.delete(x)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{
  const r=e.request,u=new URL(r.url);
  if(r.method!=='GET')return;
  /* l'API et l'authentification ne sont jamais mises en cache */
  if(u.pathname.indexOf('/rest/v1/')>=0||u.pathname.indexOf('/auth/v1/')>=0)return;
  if(u.origin===location.origin&&u.pathname.indexOf('/data/')>=0){
    /* données : on répond tout de suite avec la copie locale, et on la rafraîchit en arrière-plan */
    e.respondWith(caches.open(V).then(c=>c.match(r).then(m=>{const n=fetch(r).then(x=>{if(x.ok)c.put(r,x.clone());return x;}).catch(()=>m);return m||n;})));return;
  }
  if(u.origin===location.origin||u.hostname.indexOf('fonts.g')===0){
    e.respondWith(caches.open(V).then(c=>c.match(r).then(m=>m||fetch(r).then(x=>{if(x.ok)c.put(r,x.clone());return x;}).catch(()=>m))));
  }
});
