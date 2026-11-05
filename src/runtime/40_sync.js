/* OPSIS runtime — synchronisation entre appareils (fusion côté serveur, le plus récent gagne, clé par clé) */
(function(){
var OPSIS=window.OPSIS,sync=OPSIS.sync={status:'idle',last:0,error:null},busy=false,tmr=null,cur=Promise.resolve();
function set(s,e){sync.status=s;sync.error=e||null;OPSIS.emit('sync',s);}
sync.run=function(){
  if(!OPSIS.live||!OPSIS.auth.user()&&!OPSIS.auth.token())return Promise.resolve(false);
  if(busy){return cur.then(function(){return sync.run();});}
  busy=true;set('syncing');
  cur=OPSIS.auth.ensureFresh().then(function(){
    OPSIS.store.commit();
    return OPSIS.api('/rest/v1/rpc/merge_user_state',{method:'POST',body:{p:OPSIS.store.ledger()}});
  }).then(function(merged){
    OPSIS.store.merge(merged||{});sync.last=OPSIS.now();set('ok');return true;
  }).catch(function(e){set('error',e);return false;}).then(function(r){busy=false;return r;});
  return cur;
};
function soon(){if(!OPSIS.auth.token())return;clearTimeout(tmr);tmr=setTimeout(sync.run,3000);}
OPSIS.on('changed',soon);
OPSIS.on('auth',function(u){if(u||OPSIS.auth.token())sync.run();else set('idle');});
document.addEventListener('visibilitychange',function(){if(document.visibilityState==='visible'&&OPSIS.auth.token())sync.run();});
window.addEventListener('online',function(){if(OPSIS.auth.token())sync.run();});
OPSIS.on('hydrated',function(){if(OPSIS.auth.token())sync.run();});
})();
