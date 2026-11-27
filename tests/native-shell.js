const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await (await b.newContext({viewport:{width:430,height:900}})).newPage();
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.addInitScript(()=>{window.__calls=[];const mk=n=>new Proxy({}, {get:(t,k)=>(a)=>{window.__calls.push([n,k,JSON.stringify(a)||'']);return Promise.resolve(k==='writeFile'?{uri:'file:///cache/x.png'}:{});}});
window.Capacitor={isNativePlatform:()=>true,Plugins:{Share:mk('Share'),Filesystem:mk('Filesystem'),Browser:mk('Browser'),Haptics:mk('Haptics')},registerPlugin:n=>mk(n)};});
await p.goto('file://'+require('path').join(__dirname,'..','app.html')+'');await p.waitForTimeout(1500);
const r=await p.evaluate(async()=>{
 await navigator.share({title:'T',text:'hello',url:'https://x.y/s/1'});
 const f=new File([new Uint8Array([1,2,3])],'top.png',{type:'image/png'});
 const cs=navigator.canShare({files:[f]});await navigator.share({files:[f],title:'Top'});
 window.open('https://example.com/a');
 return {cs,calls:window.__calls.map(c=>c[0]+'.'+c[1]+' '+c[2].slice(0,110)),isInst:typeof isAppInstalled==='function'?isAppInstalled():null};});
console.log(JSON.stringify(r,null,1));console.log('errs',errs);await b.close();})();
