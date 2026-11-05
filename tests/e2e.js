#!/usr/bin/env node
/* OPSIS — tests de bout en bout : démarrage, sauvegarde, comptes, synchro, contenu en direct, notifications, hors ligne.
     node tools/build.js && node tests/e2e.js          (nécessite playwright) */
const {chromium}=require('playwright');
const {spawn}=require('child_process');
const path=require('path');
const PORT=8791,BASE='http://localhost:'+PORT;
let pass=0,fail=0;
const ok=(c,m)=>{if(c){pass++;console.log('  ok  '+m);}else{fail++;console.log('  FAIL '+m);}};
const eq=(a,b,m)=>ok(JSON.stringify(a)===JSON.stringify(b),m+(JSON.stringify(a)===JSON.stringify(b)?'':'  → '+JSON.stringify(a)+' ≠ '+JSON.stringify(b)));
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const LIVE={supabaseUrl:BASE,supabaseAnonKey:'anon-test',contentTimeoutMs:4000};
async function page(ctx,cfg,init){
  const p=await ctx.newPage();p.errs=[];
  p.on('pageerror',e=>p.errs.push(e.message));
  p.on('console',m=>{if(m.type()==='error'&&!/ERR_TUNNEL|Failed to load resource|fonts\./.test(m.text()))p.errs.push(m.text());});
  if(cfg)await p.addInitScript(c=>{window.OPSIS_CONFIG=c;},cfg);
  if(init)await p.addInitScript(init);
  return p;
}
async function boot(p,pathname){await p.goto(BASE+pathname);await p.waitForFunction(()=>window.OPSIS&&window.OPSIS.store&&window.OPSIS.store.S&&document.getElementById('main')&&document.getElementById('main').children.length>0,null,{timeout:20000});}
(async()=>{
  const srv=spawn('node',[path.join(__dirname,'../tools/dev-server.js'),String(PORT)],{stdio:'ignore'});
  await sleep(900);
  const b=await chromium.launch();
  try{
  console.log('1. démarrage et sauvegarde locale');
  {
    const ctx=await b.newContext({viewport:{width:430,height:900}});
    const p=await page(ctx);await boot(p,'/app.html');
    ok(p.errs.length===0,'aucune erreur au démarrage ('+p.errs.join('|')+')');
    const n=await p.evaluate(()=>Object.keys(OPSIS.stories()).length);ok(n>500,'plus de 500 histoires chargées ('+n+')');
    const cov=await p.evaluate(()=>OPSIS.art('ar01').indexOf('<svg')===0);ok(cov,'couverture rendue depuis les données');
    /* réglages par l'interface */
    await p.evaluate(()=>OPSIS.ui.openSettings());
    await p.click('[data-hour="8 h"]');
    await p.evaluate(()=>{OPSIS.store.S.read.ar01=true;OPSIS.store.S.saved.cs03=true;});
    await sleep(500);await p.evaluate(()=>OPSIS.store.commit());
    await p.reload();await boot(p,'/app.html');
    const st=await p.evaluate(()=>({h:OPSIS.store.S.hour,r:!!OPSIS.store.S.read.ar01,s:!!OPSIS.store.S.saved.cs03}));
    eq(st,{h:'8 h',r:true,s:true},'heure, lecture et liste retrouvées après rechargement');
    ok(await p.evaluate(()=>OPSIS.store.streak())===1,'série : 1 jour après une lecture');
    await ctx.close();
  }
  console.log('2. série de jours consécutifs');
  {
    const ctx=await b.newContext();const p=await page(ctx);await boot(p,'/app.html');
    const r=await p.evaluate(()=>{
      const day=d=>Date.parse('2027-03-'+d+'T10:00:00');const S=OPSIS.store.S;const out=[];
      [10,11,12].forEach((d,i)=>{OPSIS.now=()=>day(d);S.read['ar0'+(i+1)]=true;OPSIS.store.commit();});
      out.push(OPSIS.store.streak());
      OPSIS.now=()=>day(13);out.push(OPSIS.store.streak());   // hier lu : la série tient encore
      OPSIS.now=()=>day(15);out.push(OPSIS.store.streak());   // un jour manqué : retombe à 0
      S.read.ar04=true;OPSIS.store.commit();out.push(OPSIS.store.streak(),OPSIS.store.best());
      return out;});
    eq(r,[3,3,0,1,3],'3 jours, tient le lendemain, retombe après une pause, record conservé');
    await ctx.close();
  }
  console.log('3. comptes et synchronisation entre deux appareils');
  {
    const ctxA=await b.newContext({viewport:{width:430,height:900}}),ctxB=await b.newContext({viewport:{width:430,height:900}});
    const A=await page(ctxA,LIVE),B=await page(ctxB,LIVE);
    await boot(A,'/app.html');await boot(B,'/app.html');
    /* connexion par l'interface : e-mail, code, validation */
    await A.evaluate(()=>OPSIS.ui.openSettings());
    await A.fill('#acct-email','lecteur@exemple.fr');await A.click('[data-acct="send"]');
    await A.waitForSelector('#acct-code');await A.fill('#acct-code','000000');await A.click('[data-acct="verify"]');
    await A.waitForFunction(()=>document.querySelector('.acctmsg')&&/refusé/.test(document.querySelector('.acctmsg').textContent));
    ok(true,'un mauvais code est refusé');
    await A.fill('#acct-code','123456');await A.click('[data-acct="verify"]');
    await A.waitForFunction(()=>OPSIS.auth.token()&&OPSIS.sync.status==='ok',null,{timeout:8000});
    ok(await A.evaluate(()=>OPSIS.auth.user().email)==='lecteur@exemple.fr','connecté avec la bonne adresse');
    await A.evaluate(()=>{const S=OPSIS.store.S;S.read.cs01=true;S.read.cs02=true;S.saved.ar05=true;S.fs=22;});
    await A.evaluate(()=>OPSIS.sync.run());
    /* second appareil : même compte par l'API (le code est identique) */
    await B.evaluate(()=>OPSIS.auth.sendCode('lecteur@exemple.fr').then(()=>OPSIS.auth.verifyCode('lecteur@exemple.fr','123456')));
    await B.waitForFunction(()=>OPSIS.sync.status==='ok'&&OPSIS.store.S.read.cs02,null,{timeout:8000});
    const sb=await B.evaluate(()=>({r:!!OPSIS.store.S.read.cs01,s:!!OPSIS.store.S.saved.ar05,fs:OPSIS.store.S.fs}));
    eq(sb,{r:true,s:true,fs:22},'les lectures, la liste et la taille du texte arrivent sur l’autre appareil');
    /* retirer de la liste sur B doit se propager (suppression, pas union) */
    await B.evaluate(()=>{OPSIS.store.S.saved.ar05=false;});await sleep(400);await B.evaluate(()=>OPSIS.store.commit());await B.evaluate(()=>OPSIS.sync.run());
    await A.evaluate(()=>OPSIS.sync.run());await sleep(300);
    ok(!(await A.evaluate(()=>!!OPSIS.store.S.saved.ar05)),'un retrait fait sur B se retrouve sur A');
    ok(await A.evaluate(()=>!!OPSIS.store.S.read.cs01),'…sans perdre les autres données');
    /* conflit : deux modifications du même réglage, la plus récente gagne */
    await A.evaluate(()=>{OPSIS.store.S.hour='6 h';});await sleep(300);await A.evaluate(()=>{OPSIS.store.commit();return OPSIS.sync.run();});
    await sleep(150);await B.evaluate(()=>{OPSIS.store.S.hour='8 h';});await sleep(300);await B.evaluate(()=>{OPSIS.store.commit();return OPSIS.sync.run();});
    await A.evaluate(()=>OPSIS.sync.run());
    eq(await A.evaluate(()=>OPSIS.store.S.hour),'8 h','le réglage le plus récent l’emporte');
    /* déconnexion puis reconnexion : l’état revient du serveur */
    await A.evaluate(()=>OPSIS.auth.signOut());
    ok(await A.evaluate(()=>!OPSIS.auth.token()),'déconnexion');
    /* suppression du compte */
    await B.evaluate(()=>OPSIS.ui.openSettings());
    await B.click('[data-acct="del"]');await B.click('[data-acct="del"]');
    await sleep(1500);await boot(B,'/app.html');
    const dev=await (await fetch(BASE+'/dev/state')).json();
    ok(dev.users.length===0&&Object.keys(dev.states).length===0,'compte et données supprimés côté serveur');
    ok(await B.evaluate(()=>!OPSIS.auth.token()&&!OPSIS.store.S.read.cs01&&!OPSIS.store.S.saved.ar05),'session et état local effacés après suppression');
    ok(A.errs.length+B.errs.length===0,'aucune erreur JavaScript pendant la synchro ('+A.errs.concat(B.errs).join('|')+')');
    await ctxA.close();await ctxB.close();
  }
  console.log('4. contenu publié sans republier l’app');
  {
    const ctx=await b.newContext();const p=await page(ctx,LIVE);await boot(p,'/app.html');
    const before=await p.evaluate(()=>({src:OPSIS.data.source,n:Object.keys(OPSIS.stories()).length,hero:document.querySelector('.bigtitle').textContent}));
    eq([before.src,before.hero],['snapshot','L\'homme qui a vendu la tour Eiffel'],'au départ : instantané embarqué, l’histoire d’Eiffel à la une');
    const all=await (await fetch(BASE+'/rest/v1/stories?limit=1000')).json();
    const base=all.find(r=>r.id==='ar01');
    const day=(d)=>new Date(Date.now()+d*86400e3).toISOString();
    const dj=(id,pos,pub,name)=>({id,series:'dj',pos,published_at:pub,data:{id,name,sub:'Un récit publié ce matin',dates:'1925',country:'Paris',body:['Premier paragraphe de '+name+', assez long pour compter comme un vrai texte de lecture.','!Un retournement au milieu du récit.','Dernier paragraphe, avec la chute.'],terr:'Arnaques',c:'#E8B04A'}});
    await fetch(BASE+'/dev/publish',{method:'POST',body:JSON.stringify(dj('dj001',1,day(-2),'Le récit d’avant-hier'))});
    await fetch(BASE+'/dev/publish',{method:'POST',body:JSON.stringify(dj('dj002',2,day(-0.001),'Le récit du jour'))});
    await fetch(BASE+'/dev/publish',{method:'POST',body:JSON.stringify(dj('dj003',3,day(1),'Le récit de demain'))});
    /* une série classique déjà complète (30) : l'ajout est refusé proprement, la correction d'une histoire existante passe */
    await fetch(BASE+'/dev/publish',{method:'POST',body:JSON.stringify({id:'ar99',series:'ar',pos:99,data:Object.assign({},base.data,{id:'ar99',name:'Hors place'}),published_at:day(-1)})});
    await fetch(BASE+'/dev/publish',{method:'POST',body:JSON.stringify({id:'ar01',series:'ar',pos:0,data:Object.assign({},base.data,{name:'Titre corrigé à distance'}),published_at:'2020-01-01T00:00:00Z'})});
    await p.reload();await boot(p,'/app.html');
    const after=await p.evaluate(()=>({src:OPSIS.data.source,S:OPSIS.stories(),hero:document.querySelector('.bigtitle').textContent,week:[...document.querySelectorAll('.shelf .tile .ttl')].map(x=>x.textContent)}));
    eq(after.src,'live','contenu récupéré depuis la base');
    eq([!!after.S.dj001,!!after.S.dj002,!!after.S.dj003],[true,true,false],'histoires du jour publiées visibles, celle de demain cachée');
    eq(after.hero,'Le récit du jour','la une de l’accueil affiche l’histoire du jour');
    ok(after.week.includes('Le récit d’avant-hier')||after.week.some(x=>/avant-hier/.test(x)),'« Cette semaine » liste les dernières histoires du jour');
    ok(!after.S.ar99,'une série complète ignore l’ajout (30 places)');
    eq(after.S.ar01.title,'Titre corrigé à distance','correction d’une histoire existante appliquée sans republier');
    /* la couverture de secours est générée aux couleurs du thème */
    ok(await p.evaluate(()=>OPSIS.art('dj002').indexOf('#E8B04A')>0),'couverture de secours générée pour une histoire sans dessin');
    /* lecture d'une histoire du jour */
    await p.evaluate(()=>document.querySelector('.hero [data-open]').click());await sleep(500);
    ok(await p.evaluate(()=>/Premier paragraphe/.test(document.body.innerText)),'l’histoire du jour s’ouvre et se lit');
    /* notification : texte du jour = l'histoire publiée ce jour-là */
    const txt=await p.evaluate(()=>{const S=OPSIS.store.S;S.notif=true;S.hour='7 h';return OPSIS.notif.textForDay(OPSIS.day(),OPSIS.data,OPSIS.stories());});
    ok(/Le récit du jour/.test(txt),'la notification du jour reprend le titre de l’histoire publiée');
    /* hors ligne : le cache local suffit */
    await ctx.route(BASE+'/rest/v1/**',r=>r.abort());
    await p.reload();await boot(p,'/app.html');
    const off=await p.evaluate(()=>({src:OPSIS.data.source,t:(OPSIS.stories().dj002||{}).title}));
    eq(off,{src:'cache',t:'Le récit du jour'},'sans réseau : contenu récupéré depuis le cache local');
    const ctx2=await b.newContext();const q=await page(ctx2,LIVE);await ctx2.route(BASE+'/rest/v1/**',r=>r.abort());await boot(q,'/app.html');
    ok(await q.evaluate(()=>OPSIS.data.source==='snapshot'&&Object.keys(OPSIS.stories()).length>500),'premier lancement hors ligne : instantané embarqué');
    ok(p.errs.length+q.errs.length===0,'aucune erreur ('+p.errs.concat(q.errs).join('|')+')');
    await ctx.close();await ctx2.close();
  }
  console.log('5. notification quotidienne');
  {
    const ctx=await b.newContext();
    const fake=()=>{window.__calls=[];window.Capacitor={isNativePlatform:()=>true,Plugins:{LocalNotifications:{
      checkPermissions:async()=>({display:window.__perm||'prompt'}),requestPermissions:async()=>{window.__calls.push(['perm']);return {display:window.__perm==='denied'?'denied':'granted'};},
      cancel:async o=>{window.__calls.push(['cancel',o.notifications.length]);},schedule:async o=>{window.__calls.push(['schedule',o.notifications]);}}}};};
    const p=await page(ctx,null,fake);await boot(p,'/app.html');
    const plan=await p.evaluate(()=>{const S=OPSIS.store.S;S.notif=true;S.hour='7 h';
      return OPSIS.notif.plan(S,OPSIS.data,OPSIS.stories(),new Date(2027,0,5,10,0,0).getTime()).map(n=>({d:OPSIS.day(n.at.getTime()),h:n.at.getHours(),body:n.body}));});
    eq(plan.length,14,'14 jours programmés');
    eq([plan[0].d,plan[0].h,plan[13].d],['2027-01-06',7,'2027-01-19'],'à partir de demain 7 h, sur 14 jours');
    ok(plan.every(x=>x.body.length>5),'chaque notification a un texte');
    const pre=await p.evaluate(()=>{const S=OPSIS.store.S;S.hour='8 h';return OPSIS.notif.plan(S,OPSIS.data,OPSIS.stories(),new Date(2026,10,5,10,0,0).getTime()).length;});
    eq(pre,1,'avant le lancement : une seule notification, le jour J');
    const off=await p.evaluate(()=>{const S=OPSIS.store.S;S.notif=false;return OPSIS.notif.plan(S,OPSIS.data,OPSIS.stories(),Date.now()).length;});
    eq(off,0,'rien de programmé quand la notification est coupée');
    /* activation par l'interface : autorisation demandée puis programmation sur l'appareil */
    await p.evaluate(()=>{OPSIS.store.S.notif=false;OPSIS.store.commit();window.__calls.length=0;});
    await p.evaluate(()=>OPSIS.ui.openSettings());
    await p.click('[data-toggle="notif"]');await sleep(2200);
    const calls=await p.evaluate(()=>window.__calls.map(c=>c[0]));
    ok(calls.includes('perm')&&calls.includes('schedule'),'activer : autorisation demandée, puis notifications programmées ('+calls+')');
    /* première lecture terminée : autorisation demandée une seule fois, au bon moment */
    await p.evaluate(()=>{OPSIS.kv.del('opsis.notif.asked');window.__perm='prompt';const S=OPSIS.store.S;S.notif=true;OPSIS.store.commit();window.__calls.length=0;S.read.ar20=true;});
    await sleep(300);await p.evaluate(()=>OPSIS.store.commit());await sleep(800);
    ok(await p.evaluate(()=>window.__calls.some(c=>c[0]==='perm')),'première lecture terminée : autorisation demandée '+JSON.stringify(await p.evaluate(()=>[window.__calls.map(c=>c[0]),OPSIS.kv.get('opsis.notif.asked'),OPSIS.store.S.notif])));
    await p.evaluate(()=>{window.__calls.length=0;OPSIS.store.S.read.ar21=true;});await sleep(300);await p.evaluate(()=>OPSIS.store.commit());await sleep(800);
    ok(await p.evaluate(()=>!window.__calls.some(c=>c[0]==='perm')),'…et pas une seconde fois');
    /* refus d'autorisation : le réglage se coupe tout seul */
    await p.evaluate(()=>{window.__perm='denied';OPSIS.store.S.notif=false;OPSIS.store.commit();});
    await p.click('[data-toggle="notif"]');await sleep(1500);
    ok(await p.evaluate(()=>OPSIS.store.S.notif===false),'autorisation refusée : réglage remis sur « off »');
    await ctx.close();
  }
  console.log('6. version déployable : service worker et hors ligne');
  {
    const ctx=await b.newContext();const p=await page(ctx);
    await boot(p,'/');
    await p.evaluate(()=>navigator.serviceWorker.ready);await sleep(1200);
    ok(await p.evaluate(()=>navigator.serviceWorker.getRegistrations().then(r=>r.length>0)),'service worker enregistré');
    await p.reload();await sleep(800);
    await ctx.setOffline(true);
    await p.reload();await boot(p,'/').catch(()=>{});
    const okOff=await p.evaluate(()=>!!(window.OPSIS&&OPSIS.store&&OPSIS.store.S)).catch(()=>false);
    ok(okOff,'l’application démarre sans réseau après une première visite');
    await ctx.setOffline(false);await ctx.close();
  }
  }catch(e){fail++;console.log('EXCEPTION',e.message);}
  await b.close();srv.kill();
  console.log('\n'+pass+' réussis, '+fail+' échoués');process.exit(fail?1:0);
})();
