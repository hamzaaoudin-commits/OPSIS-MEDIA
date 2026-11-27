const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
async function run(name,seed,fn){
const ctx=await b.newContext({viewport:{width:430,height:900}});const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.addInitScript(seed=>{
 window.OPSIS_CONFIG={revenueCatIosKey:'appl_test',entitlementId:'premium'};
 const st={active:!!seed.sub,listener:null,calls:[]};window.__st=st;
 const ci=()=>({customerInfo:{managementURL:'https://apps.apple.com/account/subscriptions',entitlements:{active:st.active?{premium:{willRenew:true,periodType:'NORMAL',store:'APP_STORE',expirationDateMillis:Date.now()+30*864e5,expirationDate:new Date(Date.now()+30*864e5).toISOString()}}:{}}}});
 const P={configure:async a=>{st.calls.push('configure:'+a.apiKey)},addCustomerInfoUpdateListener:async f=>{st.listener=f;return 'id'},getCustomerInfo:async()=>ci(),
  getOfferings:async()=>({current:{monthly:{identifier:'$rc_monthly',product:{priceString:'3,99 €'}},availablePackages:[]}}),
  purchasePackage:async()=>{st.calls.push('purchase');if(st.cancel){const e=new Error('cancelled');e.userCancelled=true;throw e}st.active=true;return ci()},
  restorePurchases:async()=>{st.calls.push('restore');st.active=!!st.hasOld;return ci()},logIn:async()=>ci(),logOut:async()=>ci()};
 window.Capacitor={isNativePlatform:()=>true,getPlatform:()=>'ios',Plugins:{Purchases:P,Browser:{open:async a=>{st.calls.push('browser:'+a.url)}},LocalNotifications:{checkPermissions:async()=>({display:'granted'}),requestPermissions:async()=>({display:'granted'}),cancel:async()=>{},schedule:async()=>{},addListener:async()=>{}}}};
 if(seed.ent)localStorage.setItem('opsis.ent.v1',JSON.stringify(seed.ent));if(seed.skipOnb){localStorage.setItem('opsis.onb','1');}
},seed);
await p.goto('file://'+require('path').join(__dirname,'..','app.html')+'');await p.waitForTimeout(1200);await p.mouse.click(215,450);await p.waitForTimeout(3500);await p.locator('.ob-skip').first().click({force:true,timeout:3000}).catch(()=>{});await p.waitForTimeout(2200);
const r=await fn(p);console.log(name,JSON.stringify(r),errs.length?errs:'');await ctx.close();}
const vis=p=>p.evaluate(()=>{const e=document.querySelector('.pw');return !!e&&e.style.display!=='none'&&e.offsetHeight>0});
await run('1 non abonné → paywall',{},async p=>({pw:await vis(p),text:await p.evaluate(()=>(document.querySelector('.pw')||{}).innerText?.slice(0,160)),calls:await p.evaluate(()=>__st.calls)}));
await run('2 achat → paywall disparaît',{},async p=>{await p.click('#pwgo');await p.waitForTimeout(800);return {pw:await vis(p),calls:await p.evaluate(()=>__st.calls),cache:await p.evaluate(()=>localStorage.getItem('opsis.ent.v1'))}});
await run('3 achat annulé → reste',{},async p=>{await p.evaluate(()=>__st.cancel=true);await p.click('#pwgo');await p.waitForTimeout(800);return {pw:await vis(p),toast:await p.evaluate(()=>document.getElementById('toast').textContent)}});
await run('4 restauration (abonnement existant)',{},async p=>{await p.evaluate(()=>__st.hasOld=true);await p.click('#pwrs');await p.waitForTimeout(800);return {pw:await vis(p)}});
await run('5 restauration sans achat',{},async p=>{await p.click('#pwrs');await p.waitForTimeout(800);return {pw:await vis(p),toast:await p.evaluate(()=>document.getElementById('toast').textContent)}});
await run('6 expiration poussée par le store',{},async p=>{await p.evaluate(()=>{__st.active=true;__st.listener({entitlements:{active:{premium:{willRenew:true}}}});});await p.waitForTimeout(500);const a=await vis(p);await p.evaluate(()=>{__st.listener({entitlements:{active:{}}});});await p.waitForTimeout(500);return {afterActive:a,afterExpired:await vis(p)}});
await run('7 déjà abonné',{sub:1},async p=>({pw:await vis(p)}));
await run('8 gérer abonnement',{},async p=>({manage:await p.evaluate(async()=>{__st.active=true;const r=await OPSIS.billing.manage();return __st.calls.filter(c=>c.startsWith('browser'))})}));
await b.close();})();
