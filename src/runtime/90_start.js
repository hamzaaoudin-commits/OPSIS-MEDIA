/* OPSIS runtime — démarrage : charge le contenu, puis lance l'application */
(function(){
var OPSIS=window.OPSIS;
function fail(e){
  var b=document.getElementById('boot');
  if(b)b.innerHTML='<p>Impossible de charger OPSIS.</p><p class="bootsub">Vérifiez votre connexion puis <button onclick="location.reload()">réessayer</button></p>';
  if(window.console)console.error(String(e&&e.stack||e));
}
OPSIS.loadContent().then(function(DATA){
  OPSIS.data=DATA;
  window.__OPSIS_BOOT(DATA);
  var b=document.getElementById('boot');if(b&&b.parentNode)b.parentNode.removeChild(b);
  OPSIS.emit('ready',DATA);
  if('serviceWorker' in navigator&&/^https?:/.test(location.protocol)&&OPSIS.cfg.serviceWorker!==false){
    navigator.serviceWorker.register((OPSIS.cfg.swUrl||'sw.js')).catch(function(){});
  }
}).catch(fail);
})();
