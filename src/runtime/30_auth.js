/* OPSIS runtime — comptes : e-mail (code à 6 chiffres), Google, Apple. Passe par l'API d'authentification de Supabase. */
(function(){
var OPSIS=window.OPSIS,CFG=OPSIS.cfg,KEY='opsis.session.v1';
var auth=OPSIS.auth={session:OPSIS.kv.get(KEY)};
auth.token=function(){return auth.session&&auth.session.access_token||null;};
auth.user=function(){return auth.session&&auth.session.user||null;};
auth.enabled=function(){return OPSIS.live;};
function save(s){
  if(s&&s.expires_in&&!s.expires_at)s.expires_at=Math.floor(OPSIS.now()/1000)+s.expires_in;
  auth.session=s||null;if(s)OPSIS.kv.set(KEY,s);else OPSIS.kv.del(KEY);
  OPSIS.emit('auth',auth.user());
}
function call(path,body,method){
  return fetch(CFG.supabaseUrl+path,{method:method||'POST',headers:{apikey:CFG.supabaseAnonKey,'Content-Type':'application/json',Authorization:'Bearer '+(auth.token()||CFG.supabaseAnonKey)},body:body?JSON.stringify(body):undefined})
    .then(function(r){return r.text().then(function(t){var j=t?JSON.parse(t):{};if(!r.ok){var e=new Error(j.msg||j.error_description||j.message||('HTTP '+r.status));e.status=r.status;throw e;}return j;});});
}
/* 1) envoi du code par e-mail */
auth.sendCode=function(email){return call('/auth/v1/otp',{email:email,create_user:true});};
/* 2) vérification du code */
auth.verifyCode=function(email,code){return call('/auth/v1/verify',{type:'email',email:email,token:code}).then(function(s){save(s);return s;});};
/* Google / Apple sur le web : redirection puis retour avec les jetons dans l'adresse */
auth.oauth=function(provider){
  var back=location.href.split('#')[0];
  location.href=CFG.supabaseUrl+'/auth/v1/authorize?provider='+provider+'&redirect_to='+encodeURIComponent(back);
};
/* Apple / Google natifs (Capacitor) : le plugin renvoie un jeton d'identité */
auth.signInWithIdToken=function(provider,idToken,nonce){
  return call('/auth/v1/token?grant_type=id_token',{provider:provider,id_token:idToken,nonce:nonce}).then(function(s){save(s);return s;});
};
auth.refresh=function(){
  var s=auth.session;if(!s||!s.refresh_token)return Promise.resolve(null);
  return call('/auth/v1/token?grant_type=refresh_token',{refresh_token:s.refresh_token}).then(function(n){save(n);return n;}).catch(function(e){if(e.status>=400&&e.status<500)save(null);throw e;});
};
auth.ensureFresh=function(){
  var s=auth.session;if(!s)return Promise.resolve(null);
  if(s.expires_at&&s.expires_at-60<Math.floor(OPSIS.now()/1000))return auth.refresh();
  return Promise.resolve(s);
};
auth.signOut=function(){
  var p=auth.token()?call('/auth/v1/logout',null).catch(function(){}):Promise.resolve();
  return p.then(function(){save(null);});
};
/* suppression du compte (exigée par l'App Store) : efface l'état distant puis le compte */
auth.deleteAccount=function(){
  return auth.ensureFresh().then(function(){return OPSIS.api('/rest/v1/rpc/delete_my_account',{method:'POST',body:{}});}).then(function(){save(null);OPSIS.store.reset();});
};
/* retour d'une redirection OAuth : #access_token=...&refresh_token=... */
(function(){
  if(location.hash.indexOf('access_token=')<0)return;
  var p={};location.hash.slice(1).split('&').forEach(function(x){var i=x.indexOf('=');p[decodeURIComponent(x.slice(0,i))]=decodeURIComponent(x.slice(i+1));});
  if(!p.access_token)return;
  try{history.replaceState(null,'',location.href.split('#')[0]);}catch(e){}
  save({access_token:p.access_token,refresh_token:p.refresh_token,expires_in:+p.expires_in||3600,user:null});
  fetch(CFG.supabaseUrl+'/auth/v1/user',{headers:{apikey:CFG.supabaseAnonKey,Authorization:'Bearer '+p.access_token}}).then(function(r){return r.json();}).then(function(u){var s=auth.session;if(s){s.user=u;save(s);}}).catch(function(){});
})();
})();
