#!/usr/bin/env node
/* OPSIS — assemble l'application.
     node tools/build.js
   Produit :
     app.html        application autonome (données embarquées) : s'ouvre telle quelle, sans serveur
     app/            version à déployer : index.html léger + data/*.json + sw.js + manifest
   Configuration optionnelle : opsis.config.json { supabaseUrl, supabaseAnonKey, launchDate } */
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=path.join(__dirname,'..');
const rd=p=>fs.readFileSync(path.join(root,p),'utf8');
const wr=(p,c)=>{fs.mkdirSync(path.dirname(path.join(root,p)),{recursive:true});fs.writeFileSync(path.join(root,p),c);};
let cfg={launchDate:'2027-01-04'};
try{Object.assign(cfg,JSON.parse(rd('opsis.config.json')));}catch(e){}
const shell=rd('src/shell.html');
const runtime=fs.readdirSync(path.join(root,'src/runtime')).filter(f=>f.endsWith('.js')).sort().map(f=>rd('src/runtime/'+f)).join('\n');
const content=rd('data/content.json'),covers=rd('data/covers.json');
const ver=crypto.createHash('sha1').update(shell+runtime+content.length+covers.length+JSON.stringify(cfg)).digest('hex').slice(0,10);
const safe=j=>j.replace(/<\//g,'<\\/').replace(/<!--/g,'<\\!--');
const cfgTag=(extra)=>'<script>window.OPSIS_CONFIG=Object.assign('+JSON.stringify(Object.assign({},cfg,extra||{}))+',window.OPSIS_CONFIG||{});</script>';
const rt='<script>\n'+runtime+'\n</script>';
function page(inlineData,extra){
  let h=shell.replace('<!--OPSIS:CONFIG-->',cfgTag(extra)+(extra&&extra.lite?'\n<link rel="manifest" href="manifest.webmanifest">':'')).replace('<!--OPSIS:RUNTIME-->',()=>rt);
  h=h.replace('<!--OPSIS:DATA-->',()=>inlineData?'<script type="application/json" id="opsis-data">'+safe(inlineData)+'</script>':'');
  return h;
}
/* 1) autonome */
const c=JSON.parse(content);c.COVERS=JSON.parse(covers);
wr('app.html',page(JSON.stringify(c),{serviceWorker:false}));
/* 2) déployable */
wr('app/index.html',page(null,{lite:true,dataUrl:'data/'}));
wr('app/data/content.json',content);
wr('app/data/covers.json',covers);
wr('app/manifest.webmanifest',JSON.stringify({name:'OPSIS',short_name:'OPSIS',description:'Une histoire vraie chaque jour.',start_url:'./',scope:'./',display:'standalone',orientation:'portrait',background_color:'#09090A',theme_color:'#09090A',lang:'fr',shortcuts:[{name:"L'histoire du jour",short_name:'Du jour',url:'./?go=jour'},{name:'Une histoire au hasard',short_name:'Au hasard',url:'./?go=hasard'}],icons:[{src:'icons/icon-192.png',sizes:'192x192',type:'image/png',purpose:'any maskable'},{src:'icons/icon-512.png',sizes:'512x512',type:'image/png',purpose:'any maskable'}]},null,2));
['favicon-192.png:icons/icon-192.png','favicon-512.png:icons/icon-512.png','apple-touch-icon.png:apple-touch-icon.png','favicon.svg:favicon.svg'].forEach(p=>{const [a,b]=p.split(':');fs.mkdirSync(path.dirname(path.join(root,'app',b)),{recursive:true});fs.copyFileSync(path.join(root,a),path.join(root,'app',b));});
wr('app/sw.js',`/* OPSIS service worker — généré, version ${ver} */
const V='opsis-${ver}',SHELL=['./','index.html','manifest.webmanifest','icons/icon-192.png'];
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
`);
console.log('build',ver,'app.html',(fs.statSync(path.join(root,'app.html')).size/1e6).toFixed(2)+' Mo','| app/index.html',(fs.statSync(path.join(root,'app/index.html')).size/1e3).toFixed(0)+' Ko');
