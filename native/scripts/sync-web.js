/* Copie la version déployable de l'app (opsis-media/app) dans www/ pour Capacitor.
   Usage : node scripts/sync-web.js [chemin/vers/opsis-media]   (par défaut ../opsis-media) */
const fs=require('fs'),path=require('path');
const cands=[process.argv[2],path.join(__dirname,'..','..','app')].filter(Boolean).map(p=>path.resolve(p));
const src=cands.find(p=>fs.existsSync(path.join(p,'index.html')))||cands[0];
const dst=path.join(__dirname,'..','www');
if(!fs.existsSync(path.join(src,'index.html'))){console.error('index.html introuvable dans',src);process.exit(1);}
fs.rmSync(dst,{recursive:true,force:true});
fs.cpSync(src,dst,{recursive:true,filter:p=>!/^s([\\/]|$)/.test(path.relative(src,p))&&!/sw\.js$/.test(p)});   /* pas de pages de partage ni de service worker dans l'app native */
/* configuration publique de la version native (clés RevenueCat / Supabase / Google : publiques par conception) */
const cfg=JSON.parse(fs.readFileSync(path.join(__dirname,'..','native.config.json'),'utf8'));
const idx=path.join(dst,'index.html');let html=fs.readFileSync(idx,'utf8');
html=html.replace(/<head([^>]*)>/,'<head$1><script>window.OPSIS_CONFIG='+JSON.stringify(cfg)+';</script>');
fs.writeFileSync(idx,html);
console.log('www/ prêt :',fs.readdirSync(dst).join(', '));
