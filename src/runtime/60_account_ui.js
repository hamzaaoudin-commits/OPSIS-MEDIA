/* OPSIS runtime — bloc « Compte » dans les réglages */
(function(){
var OPSIS=window.OPSIS,ui={step:'idle',email:'',busy:false,msg:'',confirmDel:false};
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function rerender(){if(OPSIS.ui&&OPSIS.ui.renderSettings)OPSIS.ui.renderSettings();}
function streakHTML(){
  var n=OPSIS.store.streak(),b=OPSIS.store.best();
  return '<div class="opt"><span>Série en cours</span><b class="stk" data-streak="'+n+'">'+n+(n>1?' jours':' jour')+(b>n?' <i>record '+b+'</i>':'')+'</b></div>';
}
OPSIS.accountHTML=function(){
  var h=streakHTML();
  if(!OPSIS.live)return h;
  var u=OPSIS.auth.user(),tok=OPSIS.auth.token();
  if(tok){
    var st=OPSIS.sync.status,label=st==='syncing'?'Synchronisation…':st==='error'?'Hors ligne, en attente':'Synchronisé';
    h+='<div class="opt acct"><span>Connecté<small>'+esc(u&&u.email||'')+'</small></span><span class="sync" data-sync="'+st+'">'+label+'</span></div>'+
      '<div class="opt lgrow"><button data-acct="out">Se déconnecter</button></div>'+
      '<div class="opt lgrow"><button data-acct="del" class="danger">'+(ui.confirmDel?'Confirmer la suppression définitive':'Supprimer mon compte')+'</button></div>';
    if(ui.confirmDel)h+='<p class="acctmsg">Votre compte et vos données synchronisées seront effacés. Cette action est irréversible.</p>';
    return h;
  }
  h+='<div class="opt acct"><span>Compte<small>Gardez vos lectures et votre liste sur tous vos appareils.</small></span></div>';
  if(ui.step==='code'){
    h+='<div class="opt acctrow"><input id="acct-code" inputmode="numeric" autocomplete="one-time-code" maxlength="8" placeholder="Code reçu par e-mail" aria-label="Code reçu par e-mail"><button class="btn red sm" data-acct="verify"'+(ui.busy?' disabled':'')+'>Valider</button></div>'+
      '<div class="opt lgrow"><button data-acct="back">Changer d’adresse e-mail</button></div>';
  }else{
    h+='<div class="opt acctrow"><input id="acct-email" type="email" autocomplete="email" placeholder="Votre e-mail" aria-label="Votre e-mail" value="'+esc(ui.email)+'"><button class="btn red sm" data-acct="send"'+(ui.busy?' disabled':'')+'>Recevoir un code</button></div>'+
      '<div class="acctbtns"><button class="btn light" data-acct="apple">Continuer avec Apple</button><button class="btn glass" data-acct="google">Continuer avec Google</button></div>';
  }
  if(ui.msg)h+='<p class="acctmsg" role="status">'+esc(ui.msg)+'</p>';
  return h;
};
function say(m){ui.msg=m;ui.busy=false;rerender();}
document.addEventListener('click',function(e){
  var b=e.target.closest&&e.target.closest('[data-acct]');if(!b)return;
  var a=b.getAttribute('data-acct');
  if(a==='send'){
    var em=(document.getElementById('acct-email')||{}).value||'';em=em.trim();ui.email=em;
    if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em))return say('Adresse e-mail invalide.');
    ui.busy=true;ui.msg='Envoi du code…';rerender();
    OPSIS.auth.sendCode(em).then(function(){ui.step='code';say('Code envoyé à '+em+'.');}).catch(function(err){say('Envoi impossible : '+err.message);});
  }else if(a==='verify'){
    var c=((document.getElementById('acct-code')||{}).value||'').replace(/\s/g,'');
    if(c.length<6)return say('Saisissez le code reçu.');
    ui.busy=true;ui.msg='Vérification…';rerender();
    OPSIS.auth.verifyCode(ui.email,c).then(function(){ui.step='idle';ui.msg='';ui.busy=false;rerender();if(OPSIS.ui)OPSIS.ui.toast('Connecté. Vos lectures sont synchronisées.');}).catch(function(err){say('Code refusé : '+err.message);});
  }else if(a==='back'){ui.step='idle';ui.msg='';rerender();}
  else if(a==='apple'||a==='google'){
    var nat=window.Capacitor&&window.Capacitor.isNativePlatform&&window.Capacitor.isNativePlatform();
    if(nat&&OPSIS.auth.native){OPSIS.auth.native(a).catch(function(err){say('Connexion impossible : '+err.message);});}
    else OPSIS.auth.oauth(a);
  }else if(a==='out'){OPSIS.auth.signOut().then(function(){OPSIS.store.reset();location.reload();});}   /* appareil partagé : on repart d'un état vide, tout est dans le compte */
  else if(a==='del'){
    if(!ui.confirmDel){ui.confirmDel=true;rerender();return;}
    OPSIS.auth.deleteAccount().then(function(){ui.confirmDel=false;location.reload();}).catch(function(err){ui.confirmDel=false;say('Suppression impossible : '+err.message);});
  }
});
OPSIS.on('auth',rerender);OPSIS.on('sync',rerender);
OPSIS.accountUI=ui;
})();
