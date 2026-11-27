/* OPSIS runtime — abonnement dans les boutiques (App Store / Google Play) via RevenueCat.
   Apple et Google encaissent et gèrent l'abonnement ; RevenueCat vérifie les reçus et dit à l'appli si l'abonnement est actif.
   Configuration (opsis.config.json) : revenueCatIosKey, revenueCatAndroidKey (clés publiques « appl_… » / « goog_… »), entitlementId (défaut « premium »).
   Sans clé, ou sur le web : aucune barrière de paiement (l'appli reste ouverte). */
(function(){
var OPSIS=window.OPSIS,CFG=OPSIS.cfg,KEY='opsis.ent.v1',GRACE=3*86400000;
var b=OPSIS.billing={ready:false,configured:false,info:null,pkg:null,price:null,err:null};
function C(){return window.Capacitor;}
function native(){var c=C();return !!(c&&c.isNativePlatform&&c.isNativePlatform());}
function plat(){var c=C();return c&&c.getPlatform?c.getPlatform():'web';}
function P(){return OPSIS.plugin('Purchases');}
b.native=native;
b.apiKey=function(){var p=plat();return p==='ios'?CFG.revenueCatIosKey:p==='android'?CFG.revenueCatAndroidKey:null;};
b.entId=function(){return CFG.entitlementId||'premium';};
/* état d'abonnement mémorisé : l'appli fonctionne hors ligne, avec 3 jours de tolérance après la dernière vérification */
b.cached=function(){var e=OPSIS.kv.get(KEY);if(!e)return false;if(e.active&&(!e.expires||e.expires+GRACE>OPSIS.now())&&e.at+7*86400000>OPSIS.now())return true;return false;};
function apply(ci){
  var ent=ci&&ci.entitlements&&ci.entitlements.active&&ci.entitlements.active[b.entId()];
  var active=!!ent;
  b.info=active?{active:true,renews:ent.willRenew!==false,expires:ent.expirationDateMillis||(ent.expirationDate?Date.parse(ent.expirationDate):null),trial:ent.periodType==='TRIAL',store:ent.store}:{active:false};
  OPSIS.kv.set(KEY,{active:active,expires:b.info.expires||null,at:OPSIS.now()});
  OPSIS.emit('entitlement',b.info);
  return active;
}
b.entitled=function(){return b.info?!!b.info.active:b.cached();};
b.init=function(){
  if(b.ready||!native()||!P()||!b.apiKey())return Promise.resolve(false);
  b.configured=true;
  var p=P();
  return p.configure({apiKey:b.apiKey(),appUserID:(OPSIS.auth&&OPSIS.auth.user&&OPSIS.auth.user()&&OPSIS.auth.user().id)||undefined}).then(function(){
    b.ready=true;
    try{p.addCustomerInfoUpdateListener(function(ci){apply(ci);});}catch(e){}
    return Promise.all([p.getCustomerInfo().then(function(r){apply(r.customerInfo||r);}).catch(function(e){b.err=e;}),b.loadOffer()]);
  }).then(function(){return true;}).catch(function(e){b.err=e;return false;});
};
b.loadOffer=function(){
  var p=P();if(!p)return Promise.resolve(null);
  return p.getOfferings().then(function(o){
    var cur=o&&(o.current||(o.offerings&&o.offerings.current));
    var pk=cur&&(cur.monthly||(cur.availablePackages&&cur.availablePackages[0]))||null;
    b.pkg=pk;b.price=pk&&pk.product&&pk.product.priceString||null;return pk;
  }).catch(function(e){b.err=e;return null;});
};
b.purchase=function(){
  var p=P();if(!p)return Promise.reject(new Error('indisponible'));
  var go=b.pkg?Promise.resolve(b.pkg):b.loadOffer();
  return go.then(function(pk){
    if(!pk)throw new Error('Offre indisponible pour le moment');
    return p.purchasePackage({aPackage:pk});
  }).then(function(r){return {ok:apply(r.customerInfo||r)};}).catch(function(e){
    if(e&&(e.userCancelled||/cancel/i.test(String(e.message||''))))return {ok:false,cancelled:true};
    throw e;});
};
b.restore=function(){
  var p=P();if(!p)return Promise.resolve({restored:false});
  return p.restorePurchases().then(function(r){var a=apply(r.customerInfo||r);return {restored:a};});
};
/* le compte OPSIS (Supabase) devient l'identité RevenueCat : même abonnement retrouvé sur tous les appareils */
OPSIS.on('auth',function(u){var p=P();if(!p||!b.ready)return;if(u&&u.id)p.logIn({appUserID:u.id}).then(function(r){apply(r.customerInfo||r);}).catch(function(){});else p.logOut().catch(function(){});});
/* abonnement géré depuis la boutique */
b.manage=function(){var p=P();if(p&&p.showManageSubscriptions)return p.showManageSubscriptions().catch(function(){});return Promise.resolve();};
if(native())OPSIS.on('ready',function(){b.init();});
})();
