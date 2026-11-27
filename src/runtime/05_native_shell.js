/* Coque native : partage, liens externes, mailto. Sans effet sur le web. */
(function(){
  var C=window.Capacitor;if(!C||!C.isNativePlatform||!C.isNativePlatform())return;
  function abort(){var e=new Error('Partage annulé');e.name='AbortError';return e;}
  function toB64(file){return new Promise(function(ok,ko){var r=new FileReader();r.onload=function(){ok(String(r.result).split(',')[1]||'');};r.onerror=function(){ko(r.error);};r.readAsDataURL(file);});}
  function safe(n){return String(n||'opsis').replace(/[^\w.\-]+/g,'_').slice(0,60)||'opsis';}
  /* navigator.share : le WebView Android ne l'a pas, et les fichiers passent par le cache de l'app */
  navigator.canShare=function(d){return !!(d&&(d.files&&d.files.length||d.url||d.text||d.title));};
  navigator.share=function(d){
    d=d||{};var S=OPSIS.plugin('Share');if(!S)return Promise.reject(new Error('Partage indisponible'));
    var go=function(url){var o={title:d.title||'OPSIS',dialogTitle:d.title||'OPSIS'};if(d.text)o.text=d.text;if(url||d.url)o.url=url||d.url;
      return S.share(o).catch(function(e){var m=String(e&&e.message||e||'');if(/cancel|annul|dismiss/i.test(m))throw abort();throw e;});};
    var f=d.files&&d.files[0];if(!f)return go();
    var F=OPSIS.plugin('Filesystem');if(!F)return go();
    return toB64(f).then(function(b){return F.writeFile({path:'share/'+Date.now()+'-'+safe(f.name),data:b,directory:'CACHE',recursive:true});}).then(function(r){return go(r.uri);});
  };
  /* liens externes et mailto */
  var wo=window.open;
  window.open=function(u){u=String(u||'');
    if(/^mailto:|^tel:/i.test(u)){location.href=u;return null;}
    if(/^https?:/i.test(u)&&u.indexOf(location.origin)!==0){var B=OPSIS.plugin('Browser');if(B){B.open({url:u});return null;}}
    return wo?wo.apply(window,arguments):null;};
  document.addEventListener('click',function(e){var a=e.target&&e.target.closest&&e.target.closest('a[href]');if(!a)return;var h=a.getAttribute('href')||'';
    if(/^https?:/i.test(h)&&a.href.indexOf(location.origin)!==0){var B=OPSIS.plugin('Browser');if(B){e.preventDefault();B.open({url:a.href});}}},true);
})();
