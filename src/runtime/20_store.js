/* OPSIS runtime — état utilisateur : sauvegarde locale, horodatage par clé (pour la synchro), série de jours */
(function(){
var OPSIS=window.OPSIS,KEY='opsis.state.v1';
var SET=['len','mode','minutes','fs','notif','hour','theme','font','lh','hideRead','lang','focus','speed','nNew','nResume','stats'];
var store=OPSIS.store={S:null,flat:{},dirty:false};

/* S -> table plate { "read.pt01": true, "saved.eiffel": true, "set.fs": 19, "day.2027-01-04": true } */
function flatten(S){
  var f={};
  Object.keys(S.read||{}).forEach(function(k){if(S.read[k])f['read.'+k]=true;});
  Object.keys(S.saved||{}).forEach(function(k){if(S.saved[k])f['saved.'+k]=true;});
  Object.keys(S.follow||{}).forEach(function(k){if(S.follow[k])f['follow.'+k]=true;});
  SET.forEach(function(k){if(S[k]!==undefined)f['set.'+k]=S[k];});
  Object.keys(S.days||{}).forEach(function(d){f['day.'+d]=true;});
  Object.keys(S.rate||{}).forEach(function(k){if(S.rate[k])f['rate.'+k]=S.rate[k];});
  Object.keys(S.prog||{}).forEach(function(k){if(S.prog[k])f['prog.'+k]=S.prog[k];});
  Object.keys(S.x||{}).forEach(function(k){if(S.x[k]!==undefined&&S.x[k]!==null)f['x.'+k]=JSON.stringify(S.x[k]);});
  return f;
}
/* table plate -> S (sans toucher à la navigation) */
function inflate(S,f){
  S.read={};S.saved={};S.follow={};S.days={};S.rate={};S.prog={};S.x={};
  Object.keys(f).forEach(function(k){
    var v=f[k];if(v===null||v===undefined)return;
    var i=k.indexOf('.'),a=k.slice(0,i),b=k.slice(i+1);
    if(a==='read')S.read[b]=true;else if(a==='saved')S.saved[b]=true;else if(a==='follow')S.follow[b]=true;
    else if(a==='day')S.days[b]=true;else if(a==='set')S[b]=v;
    else if(a==='rate')S.rate[b]=+v;else if(a==='prog')S.prog[b]=+v;else if(a==='x'){try{S.x[b]=JSON.parse(v);}catch(e){}}
  });
}
/* ledger : { clé: {v:valeur|null, t:ms} } — null = suppression (tombstone) */
function load(){var l=OPSIS.kv.get(KEY);return l&&l.ledger?l:{ledger:{},updated:0};}
store.state=load();

/* appelé au démarrage, juste après la création de S */
OPSIS.hydrate=function(S){
  store.S=S;
  var led=store.state.ledger,f={};
  Object.keys(led).forEach(function(k){if(led[k].v!==null&&led[k].v!==undefined)f[k]=led[k].v;});
  if(Object.keys(f).length){
    var keep={read:{penicilline:true}};
    inflate(S,f);
    /* l'histoire de démonstration reste « lue » seulement si elle l'était */
    if(!f['read.penicilline'])delete S.read.penicilline;
  }else{S.days={};}
  S.days=S.days||{};
  store.flat=flatten(S);
  if(!Object.keys(led).length){Object.keys(store.flat).forEach(function(k){led[k]={v:store.flat[k],t:0};});}
  document.documentElement.style.setProperty('--fs',S.fs+'px');
  store.streakFix();
  OPSIS.emit('hydrated',S);
};

/* détecte les changements de S et les inscrit dans le ledger avec un horodatage */
store.commit=function(){
  var S=store.S;if(!S)return false;
  var led=store.state.ledger,cur=flatten(S),prev=store.flat,changed=false,t=OPSIS.now();
  var today=OPSIS.day();
  /* une nouvelle histoire lue compte pour la série du jour */
  Object.keys(cur).forEach(function(k){if(k.indexOf('read.')===0&&!prev[k]&&!led[k]){/* nouvelle lecture */}});
  var newRead=Object.keys(cur).some(function(k){return k.indexOf('read.')===0&&!prev[k];});
  if(newRead&&!S.days[today]){S.days[today]=true;cur['day.'+today]=true;}
  Object.keys(cur).forEach(function(k){if(prev[k]!==cur[k]){led[k]={v:cur[k],t:t};changed=true;}});
  Object.keys(prev).forEach(function(k){if(!(k in cur)){led[k]={v:null,t:t};changed=true;}});
  store.flat=cur;
  if(changed){store.state.updated=t;OPSIS.kv.set(KEY,store.state);OPSIS.emit('changed',cur);}
  return changed;
};
/* fusionne un ledger distant { clé: {v,t} } : le plus récent gagne */
store.merge=function(remote){
  var led=store.state.ledger,changed=false;
  Object.keys(remote||{}).forEach(function(k){
    var r=remote[k];if(!r||typeof r.t!=='number')return;
    if(!led[k]||led[k].t<r.t){led[k]=r;changed=true;}
  });
  if(changed&&store.S){
    var f={};Object.keys(led).forEach(function(k){if(led[k].v!==null&&led[k].v!==undefined)f[k]=led[k].v;});
    var S=store.S,keepNav={tab:S.tab,stack:S.stack,bpage:S.bpage,filter:S.filter};
    inflate(S,f);
    store.flat=flatten(S);store.streakFix();
    OPSIS.kv.set(KEY,store.state);
    OPSIS.emit('merged');
  }
  return changed;
};
store.ledger=function(){return store.state.ledger;};
store.reset=function(){store.state={ledger:{},updated:0};OPSIS.kv.del(KEY);};

/* série : jours consécutifs jusqu'à aujourd'hui (ou hier si rien lu aujourd'hui) */
store.streakFix=function(){};
store.streak=function(){
  var d=store.S&&store.S.days||{},t=OPSIS.day(),n=0;
  if(!d[t])t=OPSIS.dayAdd(t,-1);
  while(d[t]){n++;t=OPSIS.dayAdd(t,-1);}
  return n;
};
store.best=function(){
  var d=Object.keys((store.S&&store.S.days)||{}).sort(),best=0,run=0,prev=null;
  d.forEach(function(x){run=(prev&&OPSIS.dayAdd(prev,1)===x)?run+1:1;if(run>best)best=run;prev=x;});
  return best;
};

/* sauvegarde automatique : sur interaction, sur masquage de la page, et en tâche de fond */
var tmr=null;
function soon(){clearTimeout(tmr);tmr=setTimeout(function(){store.commit();},250);}
['click','input','change','touchend','keyup'].forEach(function(e){document.addEventListener(e,soon,true);});
document.addEventListener('visibilitychange',function(){if(document.visibilityState==='hidden')store.commit();});
window.addEventListener('pagehide',function(){store.commit();});
setInterval(function(){store.commit();},4000);
})();
