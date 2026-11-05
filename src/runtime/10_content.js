/* OPSIS runtime — contenu : instantané embarqué + mises à jour incrémentales depuis la base */
(function(){
var OPSIS=window.OPSIS,CFG=OPSIS.cfg;
var SERIES=['ar','cs','fa','pa','sv','cb','ev','im','es','pn','ex','ce','fi','di','pr','ld','vc','du','tm'];
function dname(s){return s.toUpperCase()+'D';}

function headers(extra){var h={apikey:CFG.supabaseAnonKey,Authorization:'Bearer '+((OPSIS.auth&&OPSIS.auth.token())||CFG.supabaseAnonKey)};for(var k in extra)h[k]=extra[k];return h;}
OPSIS.api=function(path,opts){
  opts=opts||{};
  var h=headers(opts.headers||{});if(opts.body&&!h['Content-Type'])h['Content-Type']='application/json';
  return fetch(CFG.supabaseUrl+path,{method:opts.method||'GET',headers:h,body:opts.body?JSON.stringify(opts.body):undefined}).then(function(r){
    if(!r.ok)return r.text().then(function(t){var e=new Error('HTTP '+r.status+' '+t.slice(0,200));e.status=r.status;throw e;});
    if(r.status===204)return null;
    return r.text().then(function(t){return t?JSON.parse(t):null;});
  });
};

/* instantané embarqué : balise JSON (app autonome) ou fichiers data/*.json */
function loadSnapshot(){
  var el=document.getElementById('opsis-data');
  if(el)return Promise.resolve(JSON.parse(el.textContent));
  var base=(CFG.dataUrl||'data/');
  return Promise.all([fetch(base+'content.json'),fetch(base+'covers.json')]).then(function(r){
    if(!r[0].ok||!r[1].ok)throw new Error('données introuvables');
    return Promise.all([r[0].json(),r[1].json()]);
  }).then(function(a){var c=a[0];c.COVERS=a[1];return c;});
}

/* applique des lignes {id,series,pos,status,data,lens,cover} au contenu */
function applyRows(DATA,rows){
  var touched={};
  rows.forEach(function(r){
    var n=dname(r.series),arr=DATA.D[n]||(n==='DJD'?(DATA.D[n]=[]):null);if(!arr)return;
    var pos=DATA._pos[n]||(DATA._pos[n]=arr.map(function(_,i){return i;}));
    var i=-1;for(var k=0;k<arr.length;k++)if(arr[k].id===r.id){i=k;break;}
    if(r.status==='archived'){if(i>=0){arr.splice(i,1);pos.splice(i,1);}delete DATA.LENS[r.id];return;}
    if(i>=0){arr[i]=r.data;pos[i]=r.pos;}
    else if(n!=='DJD'&&arr.length>=30){if(window.console)console.warn('OPSIS : série '+r.series+' complète (30), '+r.id+' ignorée — utilisez la série « dj »');return;}
    else{var j=0;while(j<pos.length&&pos[j]<=r.pos)j++;arr.splice(j,0,r.data);pos.splice(j,0,r.pos);}
    if(r.lens)DATA.LENS[r.id]=r.lens;
    if(n==='DJD'){var di=arr.indexOf(r.data);if(di>=0)arr[di].published_at=arr[di].published_at||r.published_at;}
    if(r.cover)DATA.COVERS[r.id]=r.cover;
    touched[r.id]=1;
  });
  return touched;
}

function fetchDelta(cursor){
  var out=[],page=500;
  function next(off){
    var q='/rest/v1/stories?select=id,series,pos,status,data,lens,cover,sync_at,published_at&sync_at=gt.'+encodeURIComponent(cursor)+'&order=sync_at.asc&limit='+page+'&offset='+off;
    return OPSIS.api(q).then(function(rows){out=out.concat(rows||[]);return rows&&rows.length===page?next(off+page):out;});
  }
  return next(0);
}

OPSIS.loadContent=function(){
  return loadSnapshot().then(function(DATA){
    DATA._pos={};DATA.builtAt=DATA.builtAt||'2000-01-01T00:00:00Z';DATA.meta=DATA.meta||{};
    DATA.source='snapshot';
    if(!OPSIS.live)return DATA;
    return OPSIS.idb.get('delta').then(function(cache){
      cache=cache&&cache.builtAt===DATA.builtAt?cache:{builtAt:DATA.builtAt,cursor:DATA.builtAt,rows:{},meta:{}};
      var rows=Object.keys(cache.rows).map(function(k){return cache.rows[k];});
      if(rows.length){applyRows(DATA,rows);DATA.source='cache';}
      Object.keys(cache.meta||{}).forEach(function(k){DATA[k]=cache.meta[k];});
      return OPSIS.timeout(Promise.all([fetchDelta(cache.cursor),OPSIS.api('/rest/v1/content_meta?select=key,value,updated_at&updated_at=gt.'+encodeURIComponent(cache.cursor))]),CFG.contentTimeoutMs||2500).then(function(res){
        var fresh=res[0]||[],meta=res[1]||[];
        if(fresh.length||meta.length){
          applyRows(DATA,fresh);
          meta.forEach(function(m){DATA[m.key]=m.value;cache.meta[m.key]=m.value;});
          fresh.forEach(function(r){cache.rows[r.id]=r;if(r.sync_at>cache.cursor)cache.cursor=r.sync_at;});
          meta.forEach(function(m){if(m.updated_at>cache.cursor)cache.cursor=m.updated_at;});
          DATA.source='live';DATA.fresh=fresh.length;
          OPSIS.idb.set('delta',cache);
        }
        return DATA;
      },function(){return DATA;});
    });
  });
};
})();
