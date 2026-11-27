/* OPSIS runtime — notification quotidienne.
   Natif (Capacitor) : 14 jours de notifications locales programmées sur l'appareil, sans serveur, même hors ligne.
   Web : rappel tant que la page reste ouverte (le vrai push web demande un serveur, voir docs/BACKEND.md). */
(function(){
var OPSIS=window.OPSIS,notif=OPSIS.notif={ids:[],horizon:14,timer:null};
var BASE_ID=7000;
notif.plugin=function(){return OPSIS.plugin('LocalNotifications');};
notif.minOf=function(S){var m=String(S&&S.hour||'').match(/(?::|h\s*)(\d{2})$/);return m&&+m[1]<60?+m[1]:0;};
notif.hourOf=function(S){var h=parseInt(String(S&&S.hour||'7'),10);if(!(h>=0&&h<24))h=7;return Math.max(7,Math.min(21,h));};   /* jamais la nuit : entre 7 h et 22 h */
notif.launch=function(){return (OPSIS.cfg.launchDate||'2027-01-04');};

/* texte du jour : teaser éditorial publié à l'avance (content_meta SCHEDULE : { "2027-01-04": "…" }),
   sinon l'histoire déjà publiée ce jour-là, sinon un message générique (l'histoire de demain n'est pas encore connue de l'appareil) */
notif.entryForDay=function(day,DATA,STORIES){
  var sch=DATA&&DATA.SCHEDULE;
  var ids=Object.keys(STORIES);
  for(var i=0;i<ids.length;i++){var st=STORIES[ids[i]];if(st.daily&&st.at&&OPSIS.day(Date.parse(st.at))===day)return {title:st.title,body:st.sub||'L\'histoire du jour est arrivée.',id:ids[i]};}
  if(sch&&sch[day])return {title:'OPSIS · votre histoire du jour',body:sch[day],id:null};
  var di=OPSIS.ui&&OPSIS.ui.daily&&OPSIS.ui.daily(day),ds=di&&STORIES[di];
  if(ds)return {title:ds.title,body:String(ds.sub||ds.syn||'').slice(0,110),id:di};
  return {title:'OPSIS · votre histoire du jour',body:'Votre histoire du jour est arrivée.',id:null};
};
/* liste des notifications : une par jour au plus, sur 7 jours, puis une seule « histoire pour vous » après 7 jours d'absence, puis plus rien */
notif.AWAY=7;
notif.plan=function(S,DATA,STORIES,nowMs){
  if(!S.notif)return [];
  var h=notif.hourOf(S),now=new Date(nowMs==null?OPSIS.now():nowMs),out=[],today=OPSIS.day(now.getTime()),launch=notif.launch();
  var pre=today<launch,start=pre?launch:today,limit=pre?1:notif.AWAY;   /* avant le lancement : seulement celle du jour J */
  var mk=function(day){var a=day.split('-');return new Date(+a[0],+a[1]-1,+a[2],h,notif.minOf(S),0);};
  for(var i=0;i<limit+2&&out.length<limit;i++){
    var day=OPSIS.dayAdd(start,i),at=mk(day);
    if(at.getTime()<=now.getTime())continue;
    var e=notif.entryForDay(day,DATA,STORIES);
    out.push({id:BASE_ID+out.length,at:at,day:day,title:e.title,body:e.body,sid:e.id});
  }
  /* absence : l'ouverture de l'app renouvelle tout ; si personne ne l'ouvre, une seule relance au jour 8 */
  if(!pre&&S.nBack!==false){
    var rid=OPSIS.ui&&OPSIS.ui.rec&&OPSIS.ui.rec(),rs=rid&&STORIES[rid];
    var lastDay=out.length?out[out.length-1].day:today,day2=OPSIS.dayAdd(lastDay,1),at2=mk(day2);
    out.push({id:BASE_ID+out.length,at:at2,day:day2,title:'Une histoire pour vous',body:rs?rs.title:'Elle vous attend dans OPSIS.',sid:rid||null,back:true});
  }
  return out;
};
notif.permission=function(){
  var p=notif.plugin();
  if(p)return p.checkPermissions().then(function(r){return r.display==='granted'?true:p.requestPermissions().then(function(q){return q.display==='granted';});}).catch(function(){return false;});
  if(typeof Notification==='undefined')return Promise.resolve(false);
  if(Notification.permission==='granted')return Promise.resolve(true);
  if(Notification.permission==='denied')return Promise.resolve(false);
  return Notification.requestPermission().then(function(r){return r==='granted';}).catch(function(){return false;});
};
notif.reschedule=function(){
  var S=OPSIS.store.S,DATA=OPSIS.data,STORIES=OPSIS.stories&&OPSIS.stories();
  if(!S||!DATA||!STORIES)return Promise.resolve([]);
  var p=notif.plugin(),plan=notif.plan(S,DATA,STORIES);
  notif.last=plan;
  clearTimeout(notif.timer);
  if(p){
    var cancel=[];for(var i=0;i<30;i++)cancel.push({id:BASE_ID+i});
    return p.cancel({notifications:cancel}).catch(function(){}).then(function(){
      if(!plan.length)return plan;
      return p.schedule({notifications:plan.map(function(n){return {id:n.id,title:n.title,body:n.body,schedule:{at:n.at,allowWhileIdle:true},extra:{day:n.day,sid:n.sid||''}};})}).then(function(){return plan;});
    }).catch(function(){return plan;});
  }
  /* web : rappel tant que la page est ouverte */
  if(plan.length&&typeof Notification!=='undefined'&&Notification.permission==='granted'){
    var wait=plan[0].at.getTime()-OPSIS.now();
    if(wait>0&&wait<2147483000)notif.timer=setTimeout(function(){try{var nt=new Notification(plan[0].title,{body:plan[0].body,icon:'favicon-192.png'});if(plan[0].sid)nt.onclick=function(){try{window.focus();OPSIS.ui.openStory(plan[0].sid);}catch(e){}};}catch(e){}notif.reschedule();},wait);
  }
  return Promise.resolve(plan);
};
/* le réglage vient d'être activé : demander l'autorisation, sinon le désactiver */
var lastOn=null,lastRead=-1;
OPSIS.on('changed',function(f){
  var on=!!f['set.notif'],hour=f['set.hour'],rc=Object.keys(f).filter(function(k){return k.indexOf('read.')===0;}).length;
  /* première histoire terminée : c'est le bon moment pour demander l'autorisation, pas au lancement */
  if(lastRead>=0&&rc>lastRead&&on&&!OPSIS.kv.get('opsis.notif.asked')){OPSIS.kv.set('opsis.notif.asked',1);lastRead=rc;notif.permission().then(function(){notif.reschedule();});return;}
  lastRead=rc;
  if(on&&lastOn!==true){notif.permission().then(function(ok){
    if(!ok&&OPSIS.store.S){OPSIS.store.S.notif=false;OPSIS.store.commit();if(OPSIS.ui)OPSIS.ui.renderSettings();if(OPSIS.ui)OPSIS.ui.toast('Autorisez les notifications dans les réglages de votre appareil');}
    notif.reschedule();});}
  else notif.reschedule();
  lastOn=on;
});
OPSIS.on('hydrated',function(S){lastOn=!!S.notif;lastRead=Object.keys(S.read||{}).length;setTimeout(notif.reschedule,1500);});
OPSIS.on('merged',function(){notif.reschedule();});
/* toucher la notification (natif) ouvre directement l'histoire */
(function(){var p=notif.plugin();if(p&&p.addListener)p.addListener('localNotificationActionPerformed',function(a){try{var x=a&&a.notification&&a.notification.extra;OPSIS.ui.openStory(x&&x.sid||null);}catch(e){}});})();
/* chaque ouverture renouvelle la fenêtre (7 jours + une relance) */
document.addEventListener('visibilitychange',function(){if(document.visibilityState==='visible')notif.reschedule();});
})();
