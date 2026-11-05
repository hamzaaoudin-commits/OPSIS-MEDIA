#!/usr/bin/env node
/* OPSIS — charge les histoires dans Supabase (une seule fois, puis à chaque nouveauté éditoriale).
     SUPABASE_URL=https://xxxx.supabase.co SUPABASE_SERVICE_KEY=eyJ... node tools/seed.js [--future-from=2027-01-04]
   - Sans option : tout est publié immédiatement (published_at = 2020-01-01).
   - --future-from=AAAA-MM-JJ : étale la publication, une histoire par jour à partir de cette date.
   La clé service_role ne doit JAMAIS être mise dans l'application. */
const fs=require('fs'),path=require('path');
const root=path.join(__dirname,'..');
const URL_=process.env.SUPABASE_URL,KEY=process.env.SUPABASE_SERVICE_KEY;
if(!URL_||!KEY){console.error('SUPABASE_URL et SUPABASE_SERVICE_KEY sont requis.');process.exit(1);}
const content=JSON.parse(fs.readFileSync(path.join(root,'data/content.json'),'utf8'));
const covers=JSON.parse(fs.readFileSync(path.join(root,'data/covers.json'),'utf8'));
const SERIES=['ar','cs','fa','pa','sv','cb','ev','im','es','pn','ex','ce','fi','di','pr','ld','vc','du','tm'];
const from=(process.argv.find(a=>a.startsWith('--future-from='))||'').split('=')[1];
const rows=[];let n=0;
SERIES.forEach(s=>(content.D[s.toUpperCase()+'D']||[]).forEach((d,i)=>{
  const pub=from?new Date(Date.parse(from+'T05:00:00Z')+(n++)*864e5).toISOString():'2020-01-01T00:00:00Z';
  rows.push({id:d.id,series:s,pos:i,status:'live',data:d,lens:content.LENS[d.id]||null,cover:covers[d.id]||null,published_at:pub,updated_at:content.builtAt});
}));
async function post(table,batch,conflict){
  const r=await fetch(URL_+'/rest/v1/'+table+'?on_conflict='+conflict,{method:'POST',headers:{apikey:KEY,Authorization:'Bearer '+KEY,'Content-Type':'application/json',Prefer:'resolution=merge-duplicates,return=minimal'},body:JSON.stringify(batch)});
  if(!r.ok)throw new Error(table+' '+r.status+' '+(await r.text()).slice(0,300));
}
(async()=>{
  for(let i=0;i<rows.length;i+=25){await post('stories',rows.slice(i,i+25),'id');process.stdout.write('\r'+Math.min(i+25,rows.length)+'/'+rows.length+' histoires');}
  console.log();
  await post('content_meta',[{key:'BOOK',value:content.BOOK,updated_at:content.builtAt},{key:'BSRC',value:content.BSRC,updated_at:content.builtAt}],'key');
  console.log('terminé :',rows.length,'histoires,',from?'publication étalée dès '+from:'toutes publiées');
})().catch(e=>{console.error(e.message);process.exit(1);});
