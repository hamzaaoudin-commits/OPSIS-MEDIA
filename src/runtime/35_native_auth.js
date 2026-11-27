/* OPSIS runtime — connexion Apple / Google natives (Capacitor, plugin @capgo/capacitor-social-login).
   Le plugin renvoie un jeton d'identité ; Supabase l'échange contre une session (auth.signInWithIdToken).
   Configuration : googleWebClientId, googleIosClientId (opsis.config.json). */
(function(){
var OPSIS=window.OPSIS,CFG=OPSIS.cfg,auth=OPSIS.auth;
function rnd(){var a=new Uint8Array(16);crypto.getRandomValues(a);return Array.prototype.map.call(a,function(x){return ('0'+x.toString(16)).slice(-2);}).join('');}
function sha(t){return crypto.subtle.digest('SHA-256',new TextEncoder().encode(t)).then(function(b){return Array.prototype.map.call(new Uint8Array(b),function(x){return ('0'+x.toString(16)).slice(-2);}).join('');});}
var inited=false;
function init(P){
  if(inited)return Promise.resolve();
  var o={apple:{}};
  if(CFG.googleWebClientId)o.google={webClientId:CFG.googleWebClientId,iOSClientId:CFG.googleIosClientId||undefined,mode:'online'};
  return P.initialize(o).then(function(){inited=true;});
}
auth.native=function(provider){
  var P=OPSIS.plugin('SocialLogin');
  if(!P)return Promise.reject(new Error('indisponible sur cet appareil'));
  if(provider==='google'&&!CFG.googleWebClientId)return Promise.reject(new Error('Google n\'est pas encore configuré'));
  return init(P).then(function(){
    if(provider==='apple'){
      var raw=rnd();
      return sha(raw).then(function(h){return P.login({provider:'apple',options:{scopes:['email','name'],nonce:h}});}).then(function(r){
        var t=r&&r.result&&r.result.idToken;if(!t)throw new Error('jeton Apple manquant');
        return auth.signInWithIdToken('apple',t,raw);});
    }
    return P.login({provider:'google',options:{scopes:['email','profile']}}).then(function(r){
      var t=r&&r.result&&r.result.idToken;if(!t)throw new Error('jeton Google manquant');
      return auth.signInWithIdToken('google',t);});
  }).then(function(){OPSIS.emit('auth',auth.user());});
};
})();
