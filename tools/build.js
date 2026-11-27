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
let content=rd('data/content.json');const covers=rd('data/covers.json');
/* « Une vie en épisodes » : data/lives.json (id du portrait -> épisodes) est fusionné dans le contenu */
try{const lv=JSON.parse(rd('data/lives.json')),cj=JSON.parse(content);cj.LIVES=lv;content=JSON.stringify(cj);}catch(e){}
const ver=crypto.createHash('sha1').update(shell+runtime+content.length+covers.length+JSON.stringify(cfg)).digest('hex').slice(0,10);
const safe=j=>j.replace(/<\//g,'<\\/').replace(/<!--/g,'<\\!--');
const cfgTag=(extra)=>'<script>window.OPSIS_CONFIG=Object.assign('+JSON.stringify(Object.assign({},cfg,extra||{}))+',window.OPSIS_CONFIG||{});</script>';
const rt='<script>\n'+runtime+'\n</script>';
const fontsCss=rd('src/fonts.css');
const fontsInline=()=>fontsCss.replace(/url\(fonts\/([^)]+)\)/g,(m,f)=>'url(data:font/woff2;base64,'+fs.readFileSync(path.join(root,'src/fonts',f)).toString('base64')+')');
/* images de démarrage iOS : noir plein, pour qu'aucun fond blanc ne précède l'intro */
const STARTUP=[[430,932,3],[428,926,3],[414,896,3],[414,896,2],[393,852,3],[390,844,3],[375,812,3],[375,667,2],[320,568,2],[834,1194,2],[820,1180,2],[810,1080,2],[768,1024,2],[1024,1366,2],[440,956,3],[420,912,3],[402,874,3],[834,1210,2],[1032,1376,2],[744,1133,2],[834,1112,2]];
function blackPng(w,h){const z=require('zlib');const raw=Buffer.alloc((w*3+1)*h);const crcT=[];for(let n=0;n<256;n++){let c=n;for(let k=0;k<8;k++)c=c&1?0xedb88320^(c>>>1):c>>>1;crcT[n]=c>>>0;}
const crc=b=>{let c=0xffffffff;for(const x of b)c=crcT[(c^x)&255]^(c>>>8);return(c^0xffffffff)>>>0;};
const ch=(t,d)=>{const l=Buffer.alloc(4);l.writeUInt32BE(d.length);const td=Buffer.concat([Buffer.from(t),d]);const c=Buffer.alloc(4);c.writeUInt32BE(crc(td));return Buffer.concat([l,td,c]);};
const ih=Buffer.alloc(13);ih.writeUInt32BE(w,0);ih.writeUInt32BE(h,4);ih[8]=8;ih[9]=2;
return Buffer.concat([Buffer.from([137,80,78,71,13,10,26,10]),ch('IHDR',ih),ch('IDAT',z.deflateSync(raw,{level:9})),ch('IEND',Buffer.alloc(0))]);}
STARTUP.forEach(d=>wr('app/startup/'+d[0]*d[2]+'x'+d[1]*d[2]+'.png',blackPng(d[0]*d[2],d[1]*d[2])));
function page(inlineData,extra){
  let h=shell.replace('<!--OPSIS:CONFIG-->',cfgTag(extra)+(extra&&extra.lite?'\n<link rel="manifest" href="manifest.webmanifest">'+STARTUP.map(d=>`<link rel="apple-touch-startup-image" media="(device-width: ${d[0]}px) and (device-height: ${d[1]}px) and (-webkit-device-pixel-ratio: ${d[2]}) and (orientation: portrait)" href="startup/${d[0]*d[2]}x${d[1]*d[2]}.png">`).join('\n'):'')).replace('<!--OPSIS:RUNTIME-->',()=>rt);
  h=h.replace('<!--OPSIS:FONTS-->',()=>'<style>\n'+(inlineData?fontsInline():fontsCss)+'</style>');
  h=h.replace('<!--OPSIS:DATA-->',()=>inlineData?'<script type="application/json" id="opsis-data">'+safe(inlineData)+'</script>':'');
  return h;
}
/* 1) autonome */
const c=JSON.parse(content);c.COVERS=JSON.parse(covers);
wr('app.html',page(JSON.stringify(c),{serviceWorker:false}));
/* 2) déployable */
wr('app/index.html',page(null,{lite:true,dataUrl:'data/'}));
fs.mkdirSync(path.join(root,'app/fonts'),{recursive:true});fs.readdirSync(path.join(root,'src/fonts')).forEach(f=>fs.copyFileSync(path.join(root,'src/fonts',f),path.join(root,'app/fonts',f)));
wr('app/data/content.json',content);
wr('app/data/covers.json',covers);
let feed='{"rows":[]}';try{feed=rd('data/feed.json');JSON.parse(feed);}catch(e){feed='{"rows":[]}';}
wr('app/data/feed.json',feed);   /* histoires publiées après l'instantané : voir tools/publish.js */
wr('app/manifest.webmanifest',JSON.stringify({name:'OPSIS',short_name:'OPSIS',description:'The world is made of stories.',start_url:'./',scope:'./',display:'standalone',orientation:'portrait',background_color:'#09090A',theme_color:'#09090A',lang:'fr',shortcuts:[{name:"L'histoire du jour",short_name:'Du jour',url:'./?go=jour'},{name:'Une histoire au hasard',short_name:'Au hasard',url:'./?go=hasard'}],icons:[{src:'icons/icon-192.png',sizes:'192x192',type:'image/png',purpose:'any maskable'},{src:'icons/icon-512.png',sizes:'512x512',type:'image/png',purpose:'any maskable'}]},null,2));
['favicon-192.png:icons/icon-192.png','favicon-512.png:icons/icon-512.png','apple-touch-icon.png:apple-touch-icon.png','favicon.svg:favicon.svg'].forEach(p=>{const [a,b]=p.split(':');fs.mkdirSync(path.dirname(path.join(root,'app',b)),{recursive:true});fs.copyFileSync(path.join(root,a),path.join(root,'app',b));});
wr('app/sw.js',`/* OPSIS service worker — généré, version ${ver} */
const V='opsis-${ver}',SHELL=['./','index.html','manifest.webmanifest','icons/icon-192.png'],OFFLINE=${JSON.stringify(['data/content.json','data/covers.json'].concat(fs.readdirSync(path.join(root,'src/fonts')).filter(f=>/latin-(300|400|500|600|700|800|900)-(normal|italic)\.woff2$/.test(f)).map(f=>'fonts/'+f)))};
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
  if(u.origin===location.origin&&u.pathname.slice(-14)==='/data/feed.json'){e.respondWith(fetch(r).catch(()=>caches.match(r)));return;}   /* le flux de publication se lit toujours en direct */
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

/* 4) pages légales publiques (URL exigées par l'App Store et Google Play) : /confidentialite /conditions /mentions */
(function(){
  const m=shell.match(/var LEGAL=(\{[\s\S]*?\});\s*\nvar LEGAL_DATE='([^']*)'/);if(!m){console.warn('LEGAL introuvable : pages légales non générées');return;}
  const L=JSON.parse(m[1]),date=m[2];
  const css='body{margin:0;background:#09090A;color:#EDE6DA;font:17px/1.65 Georgia,serif}main{max-width:720px;margin:0 auto;padding:56px 22px 90px}h1{font:800 40px/1.05 Impact,"Arial Narrow",sans-serif;text-transform:uppercase;margin:0 0 8px}h2{font:700 20px/1.3 system-ui,sans-serif;margin:34px 0 8px}p{margin:0 0 12px;color:#d8d2c6}a{color:#E2474C}.d{color:#8d887f;font:14px system-ui,sans-serif;margin-bottom:28px}nav{margin-top:48px;font:15px system-ui,sans-serif}nav a{margin-right:18px}.brand{font:700 13px system-ui,sans-serif;letter-spacing:.3em;color:#E2474C;margin-bottom:26px;display:block;text-decoration:none}';
  for(const k of Object.keys(L)){
    const d=L[k],body=d[1].map(a=>'<section><h2>'+a[0]+'</h2>'+a[1]+'</section>').join('');
    const nav=Object.keys(L).filter(x=>x!==k).map(x=>'<a href="/'+x+'">'+L[x][0]+'</a>').join('');
    const html='<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+d[0]+' · OPSIS</title><meta name="robots" content="index,follow"><style>'+css+'</style></head><body><main><a class="brand" href="/">OPSIS</a><h1>'+d[0]+'</h1><p class="d">Dernière mise à jour : '+date+'</p>'+body+'<nav>'+nav+'</nav></main></body></html>';
    wr('app/'+k+'.html',html);
  }
  console.log('pages légales :',Object.keys(L).join(', '));
})();
