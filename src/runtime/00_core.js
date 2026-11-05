/* OPSIS runtime — noyau : configuration, stockage local, utilitaires */
(function(){
var CFG=window.OPSIS_CONFIG||{};
var OPSIS=window.OPSIS=window.OPSIS||{};
OPSIS.cfg=CFG;
OPSIS.live=!!(CFG.supabaseUrl&&CFG.supabaseAnonKey);
OPSIS.now=function(){return Date.now();};
/* stockage local : toujours entouré de try/catch (navigation privée, aperçus, quotas) */
OPSIS.kv={
  get:function(k){try{var v=window.localStorage.getItem(k);return v==null?null:JSON.parse(v);}catch(e){return null;}},
  set:function(k,v){try{window.localStorage.setItem(k,JSON.stringify(v));return true;}catch(e){return false;}},
  del:function(k){try{window.localStorage.removeItem(k);}catch(e){}}
};
/* IndexedDB : cache du contenu distant (trop gros pour localStorage) */
function idb(){return new Promise(function(res,rej){
  try{var r=indexedDB.open('opsis',1);r.onupgradeneeded=function(){r.result.createObjectStore('kv');};
  r.onsuccess=function(){res(r.result);};r.onerror=function(){rej(r.error);};}catch(e){rej(e);}});}
OPSIS.idb={
  get:function(k){return idb().then(function(d){return new Promise(function(res){var q=d.transaction('kv').objectStore('kv').get(k);q.onsuccess=function(){res(q.result||null);};q.onerror=function(){res(null);};});}).catch(function(){return null;});},
  set:function(k,v){return idb().then(function(d){return new Promise(function(res){var t=d.transaction('kv','readwrite');t.objectStore('kv').put(v,k);t.oncomplete=function(){res(true);};t.onerror=function(){res(false);};});}).catch(function(){return false;});}
};
/* jour local au format AAAA-MM-JJ */
OPSIS.day=function(t){var d=new Date(t==null?OPSIS.now():t);function p(n){return (n<10?'0':'')+n;}return d.getFullYear()+'-'+p(d.getMonth()+1)+'-'+p(d.getDate());};
OPSIS.dayAdd=function(day,n){var a=day.split('-');var d=new Date(+a[0],+a[1]-1,+a[2]+n,12,0,0);return OPSIS.day(d.getTime());};
OPSIS.timeout=function(p,ms){return new Promise(function(res,rej){var t=setTimeout(function(){rej(new Error('timeout'));},ms);p.then(function(v){clearTimeout(t);res(v);},function(e){clearTimeout(t);rej(e);});});};
OPSIS.events={};
OPSIS.on=function(n,f){(OPSIS.events[n]=OPSIS.events[n]||[]).push(f);};
OPSIS.emit=function(n,a){(OPSIS.events[n]||[]).forEach(function(f){try{f(a);}catch(e){if(window.console)console.error(e);}});};
})();
