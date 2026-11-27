#!/usr/bin/env node
/* OPSIS — l'app native (instantané embarqué + fichiers data/) reçoit les nouvelles histoires sans mise à jour.  node tools/build.js && node tests/native-live.js */
const {chromium}=require('playwright');const {spawn}=require('child_process');const path=require('path');
const PORT=8792,BASE='http://localhost:'+PORT;let fail=0;
const ok=(c,m)=>{if(!c)fail++;console.log((c?'  ok  ':'  FAIL ')+m);};
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
  const srv=spawn('node',[path.join(__dirname,'../tools/dev-server.js'),String(PORT)],{stdio:'ignore'});await sleep(900);
  const b=await chromium.launch();
  try{
    const ctx=await b.newContext({viewport:{width:430,height:900}});const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
    await p.addInitScript(c=>{window.OPSIS_CONFIG=c;window.Capacitor={isNativePlatform:()=>true,getPlatform:()=>'android',Plugins:{LocalNotifications:{checkPermissions:async()=>({display:'granted'}),requestPermissions:async()=>({display:'granted'}),cancel:async()=>{},schedule:async()=>{},addListener:async()=>{}}}};},{contentTimeoutMs:4000});
    const boot=async()=>{await p.goto(BASE+'/index.html');await p.waitForFunction(()=>window.OPSIS&&OPSIS.store&&OPSIS.store.S&&OPSIS.data&&document.getElementById('main')&&document.getElementById('main').children.length>0,null,{timeout:20000});};
    await boot();
    const day=d=>new Date(Date.now()+d*86400e3).toISOString();
    const before=await p.evaluate(()=>({src:OPSIS.data.source,has:!!OPSIS.stories().dj900}));
    ok(before.src==='snapshot'&&!before.has,'au départ : instantané embarqué (data/), aucune histoire du jour');
    const mk=(id,pos,pub,name)=>({id,series:'dj',pos,published_at:pub,data:{id,name,sub:'Publié sans mise à jour',dates:'1925',country:'Paris',body:['Premier paragraphe de '+name+', assez long pour compter comme un vrai texte de lecture.','Dernier paragraphe.'],terr:'Arnaques',c:'#E8B04A'}});
    const FEED=path.join(__dirname,'../app/data/feed.json'),bak=require('fs').readFileSync(FEED,'utf8');
    const row=(id,pos,pub,name)=>{const r=mk(id,pos,pub,name);return {id,series:'dj',pos,status:'published',published_at:pub,data:Object.assign(r.data,{published_at:pub})};};
    require('fs').writeFileSync(FEED,JSON.stringify({rows:[row('dj900',900,day(-0.01),'Nouvelle histoire native'),row('dj901',901,day(2),'Histoire de dans deux jours')]}));
    process.on('exit',()=>require('fs').writeFileSync(FEED,bak));
    await p.reload();await boot();
    const after=await p.evaluate(()=>({src:OPSIS.data.source,a:!!OPSIS.stories().dj900,f:!!OPSIS.stories().dj901}));
    ok(after.src==='feed'&&after.a&&!after.f,'app native sans Supabase : la nouvelle histoire arrive par le flux, celle du futur reste cachée');
    /* hors ligne : la nouvelle histoire reste disponible (cache local) */
    await ctx.route('**/data/feed.json',r=>r.abort());await p.reload();await boot();
    const off=await p.evaluate(()=>({src:OPSIS.data.source,a:!!OPSIS.stories().dj900}));
    ok(off.a,'hors connexion : la nouvelle histoire reste lisible ('+off.src+')');
    ok(errs.length===0,'aucune erreur JS '+(errs.length?errs.join('|'):''));
  }finally{await b.close();srv.kill();}
  console.log(fail?fail+' échec(s)':'natif live : tout passe');process.exit(fail?1:0);
})();
