const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:390,height:844}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error'&&!/Failed to load resource|ERR_/.test(m.text()))errs.push(m.text())});
await p.goto('file://'+require('path').resolve(__dirname,'..','app.html')+'');await p.waitForTimeout(2500);await p.mouse.click(195,420);await p.waitForTimeout(1600);
const shot=async n=>{await p.waitForTimeout(500);await p.screenshot({path:''+require('os').tmpdir()+'/'+n+'.png'});};
const click=async sel=>{const ok=await p.evaluate(s=>{const e=document.querySelector(s);if(!e)return false;e.click();return true;},sel);if(!ok)console.log('NOEL',sel);await p.waitForTimeout(550);};
const back=()=>click('#layerview [data-back]');
const log=async(n,f)=>console.log(n,JSON.stringify(await p.evaluate(f)));
await log('home shelves',()=>[...document.querySelectorAll('#main .shelf h2')].map(e=>e.innerText.split('\n')[0]).slice(0,9));
await p.evaluate(()=>document.getElementById('main').scrollTo(0,700));await shot('01home');
// search
await click('#main [data-search]');await p.waitForTimeout(500);await shot('02search0');
await p.fill('#q','espion');await p.waitForTimeout(300);await shot('03search1');
await log('search',()=>[document.querySelectorAll('#qres .qrow').length,document.querySelectorAll('#qres .tile').length]);
await p.fill('#q','tyson');await p.waitForTimeout(200);await log('tyson',()=>[...document.querySelectorAll('#qres .qrow')].map(e=>e.innerText));
await p.keyboard.press('Enter');await p.fill('#q','');await p.waitForTimeout(200);await log('hist',()=>[...document.querySelectorAll('#qres .qsec')][0].innerText.slice(0,60));
await back();
// theme subcats
await click('#main [data-terr="10"]');await shot('04theme');await log('subs',()=>[...document.querySelectorAll('#layerview .chips button')].map(e=>e.innerText));
await click('#layerview [data-subf="es"]');await log('sub es',()=>document.querySelectorAll('#layerview .tile').length);await back();
// collection + path
await click('#main [data-col="froide"]');await shot('05col');await back();
await click('#main [data-path="gf"]');await shot('06path');await back();
// reader
await p.evaluate(()=>{const ph=document.querySelector('#phone');const bt=document.createElement('button');bt.setAttribute('data-open','es11');ph.appendChild(bt);bt.click();bt.remove();});await p.waitForTimeout(700);await shot('07reader');
await p.evaluate(()=>{const v=document.getElementById('layerview');v.scrollTop=(v.scrollHeight-v.clientHeight)*0.4;});await p.waitForTimeout(400);
await log('prog',()=>OPSIS.store.S.prog);
await p.evaluate(()=>{const v=document.getElementById('layerview');const e=v.querySelector('.rateb');v.scrollTop=e.offsetTop-200;});await shot('08tail');
await click('#layerview [data-rate="4"]');await log('rate',()=>OPSIS.store.S.rate);
await click('#layerview [data-quiz]');await p.evaluate(()=>{const v=document.getElementById('layerview');const e=v.querySelector('.quiz');v.scrollTop=e.offsetTop-200;});await shot('09quiz');
for(let i=0;i<3;i++){await click('#layerview .qzo');}
await p.evaluate(()=>{const v=document.getElementById('layerview');const e=v.querySelector('.quiz');v.scrollTop=e.offsetTop-200;});await shot('10quizend');
// selection -> quote
await p.evaluate(()=>{const v=document.getElementById('layerview');const ps=v.querySelectorAll('.rtext>p:not(.dl):not(.orn)');const el=ps[2];v.scrollTop=el.offsetTop-300;const r=document.createRange();r.selectNodeContents(el);const s=getSelection();s.removeAllRanges();s.addRange(r);});await p.waitForTimeout(400);await shot('11sel');
await click('.selbar [data-selq]');await log('quotes',()=>(OPSIS.store.S.x.quotes||[]).map(q=>q.t.slice(0,40)));
// quick sheet + light
await click('#layerview [data-quick]');await shot('12quick');
await click('#settingsbox [data-theme="light"]');await click('#settingsbox [data-font="sans"]');await click('#settingsbox [data-closesettings]');
await p.evaluate(()=>{document.getElementById('layerview').scrollTop=0;});await shot('13light_reader');
await p.evaluate(()=>{const v=document.getElementById('layerview');v.scrollTop=900;});await shot('14light_text');
// audio
await click('#layerview [data-audio]');await p.waitForTimeout(500);await log('audio',()=>[document.querySelector('.aubar').classList.contains('on'),'speechSynthesis' in window]);await shot('15audio');
await click('.aubar [data-au="stop"]');
// collection add
await click('#layerview [data-coladd]');await p.fill('#newcol','À raconter');await click('#settingsbox [data-colnew]');await shot('16colsheet');await click('#settingsbox [data-closesettings]');
await click('#layerview [data-report]');await shot('17report');await click('#settingsbox [data-closesettings]');
await click('#layerview [data-finish]');await p.waitForTimeout(600);
await shot('18light_home');
await p.evaluate(()=>document.getElementById('main').scrollTo(0,620));await shot('19light_home2');
// mon espace
await click('#main [data-lib]');await shot('20espace');await p.evaluate(()=>{document.getElementById('layerview').scrollTop=520;});await shot('21espace2');
await click('#layerview [data-quotes]');await shot('22quotes');await click('#layerview [data-qcard="0"]');await p.waitForTimeout(1600);await shot('23card');await click('#sclose');await back();
await click('#layerview [data-set="root"]');await shot('24settings');
for(const k of ['lecture','langue','notifs','abo','confid','widget','compte']){await click('#layerview [data-set="'+k+'"]');await shot('25set_'+k);await back();}
await back();await back();
// dark again + resume
await p.evaluate(()=>{OPSIS.store.S.theme='dark';OPSIS.store.S.font='serif';});
await p.evaluate(()=>{const ph=document.querySelector('#phone');const bt=document.createElement('button');bt.setAttribute('data-open','mq01');ph.appendChild(bt);bt.click();bt.remove();});await p.waitForTimeout(700);
await p.evaluate(()=>{const v=document.getElementById('layerview');v.scrollTop=(v.scrollHeight-v.clientHeight)*0.5;});await p.waitForTimeout(300);await back();
await log('resume shelf',()=>[...document.querySelectorAll('#main .shelf h2')].map(e=>e.innerText.split('\n')[0]).slice(0,4));
await p.evaluate(()=>{const ph=document.querySelector('#phone');const bt=document.createElement('button');bt.setAttribute('data-open','mq01');ph.appendChild(bt);bt.click();bt.remove();});await p.waitForTimeout(900);
await log('resumed scroll',()=>{const v=document.getElementById('layerview');return Math.round(v.scrollTop/(v.scrollHeight-v.clientHeight)*100);});
await p.evaluate(()=>OPSIS.store.commit());
await log('persist keys',()=>Object.keys(OPSIS.store.ledger()).filter(k=>/^(rate|prog|x)\./.test(k)));
console.log('ERR',JSON.stringify(errs));await b.close();})();
