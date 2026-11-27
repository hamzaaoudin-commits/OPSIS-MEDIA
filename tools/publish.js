#!/usr/bin/env node
/* Publier une histoire du jour sans mise à jour de l'app : l'ajoute à data/feed.json (lu par l'app web et l'app native).
     node tools/publish.js histoire.json [--replace]
   histoire.json : { "id":"dj001", "name":"Titre", "sub":"Phrase d'accroche", "dates":"1925", "country":"Paris", "job":"…",
                     "terr":"Destins", "c":"#E8B04A", "published_at":"2027-01-04T05:00:00Z", "src":"sources…", "body":["…","!retournement","#intertitre","@lieu, date","…"] }
   Après : node tools/build.js, puis déployer app/ (miroir opsis-app → Vercel). */
const fs=require('fs'),path=require('path');
const root=path.join(__dirname,'..'),FEED=process.env.OPSIS_FEED||path.join(root,'data/feed.json');
const file=process.argv[2],replace=process.argv.includes('--replace');
if(!file){console.error('usage : node tools/publish.js histoire.json [--replace]');process.exit(2);}
const d=JSON.parse(fs.readFileSync(file,'utf8'));
const shell=fs.readFileSync(path.join(root,'src/shell.html'),'utf8');
const terrs=new Set([...shell.matchAll(/terr:'([^']+)'/g)].map(m=>m[1]));
const err=[];
if(!/^dj\d{3,}$/.test(d.id||''))err.push('id : « dj001 », « dj002 »… (série des histoires du jour)');
if(!d.name||d.name.length>70)err.push('name : titre, 70 caractères max');
if(!d.sub)err.push('sub : phrase d\'accroche');
if(!Array.isArray(d.body)||d.body.filter(t=>!/^[#@*]/.test(t)).length<8)err.push('body : au moins 8 paragraphes de texte');
const words=(d.body||[]).filter(t=>!/^[#@*]/.test(t)).join(' ').split(/\s+/).length;
if(words<600)err.push('body : '+words+' mots, 600 minimum pour une lecture de 3 minutes');
if(!terrs.has(d.terr))err.push('terr : un de '+[...terrs].join(', '));
if(!/^#[0-9a-f]{6}$/i.test(d.c||''))err.push('c : couleur #RRGGBB');
if(!d.published_at||isNaN(Date.parse(d.published_at)))err.push('published_at : date ISO, ex. 2027-01-04T05:00:00Z');
if(!d.src)err.push('src : sources');
if(err.length){console.error('Histoire refusée :\n - '+err.join('\n - '));process.exit(1);}
const feed=JSON.parse(fs.readFileSync(FEED,'utf8'));
const i=feed.rows.findIndex(r=>r.id===d.id);
if(i>=0&&!replace){console.error(d.id+' existe déjà (--replace pour la remplacer)');process.exit(1);}
const pos=i>=0?feed.rows[i].pos:Math.max(0,...feed.rows.map(r=>r.pos||0))+1;
const row={id:d.id,series:'dj',pos,status:'published',published_at:new Date(d.published_at).toISOString(),data:Object.assign({},d,{published_at:new Date(d.published_at).toISOString()})};
if(i>=0)feed.rows[i]=row;else feed.rows.push(row);
fs.writeFileSync(FEED,JSON.stringify(feed,null,1));
console.log((i>=0?'remplacée : ':'ajoutée : ')+d.id+' « '+d.name+' » · '+words+' mots · publiée le '+row.published_at+' · '+feed.rows.length+' histoire(s) dans le flux');
