#!/usr/bin/env node
/* OPSIS — pages de partage publiques (couverture + quatrième de couverture + invitation à lire dans l'app).
     node tools/build.js && node tools/share-pages.js
   Produit app/s/<id>/index.html et app/s/og/<id>.jpg (aperçu 1200×630 pour Instagram, WhatsApp, iMessage…).
   Aucune ligne du texte de l'histoire n'est publiée : seulement titre, couverture et quatrième de couverture. */
const fs=require('fs'),path=require('path');const {chromium}=require('playwright');
const BASE=process.env.OPSIS_BASE||'https://opsis-alpha.vercel.app';
const root=path.join(__dirname,'..'),out=path.join(root,'app/s');
const esc=t=>String(t==null?'':t).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
(async()=>{
  const b=await chromium.launch(),p=await b.newPage({viewport:{width:1200,height:630}});
  await p.goto('file://'+path.join(root,'app.html'));await p.waitForTimeout(2000);
  const list=await p.evaluate(()=>{const S=OPSIS.stories(),o=[];Object.keys(S).forEach(id=>{const s=S[id];if(OPSIS.ui.vis(id))o.push({id,title:s.title,kind:s.kind||'',min:s.min,series:s.series||'',terr:s.terr||'',sub:s.sub||''});});return o;});
  const content=JSON.parse(fs.readFileSync(path.join(root,'data/content.json'),'utf8')),covers=JSON.parse(fs.readFileSync(path.join(root,'data/covers.json'),'utf8'));
  fs.rmSync(out,{recursive:true,force:true});fs.mkdirSync(path.join(out,'og'),{recursive:true});
  const css=fs.readFileSync(path.join(root,'src/fonts.css'),'utf8').replace(/url\(fonts\//g,'url(/fonts/');
  const tpl=(s,blurb,og)=>`<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>${esc(s.title)} · OPSIS</title>
<meta name="description" content="${esc(blurb.slice(0,200))}"><meta name="theme-color" content="#09090A">
<meta property="og:type" content="article"><meta property="og:site_name" content="OPSIS"><meta property="og:title" content="${esc(s.title)}"><meta property="og:description" content="${esc(blurb.slice(0,200))}"><meta property="og:image" content="${BASE}/s/og/${s.id}.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg"><style>${css}
*{box-sizing:border-box;margin:0}body{background:#09090A;color:#EDE6DA;font-family:'Hanken Grotesk',system-ui,sans-serif;min-height:100vh;-webkit-font-smoothing:antialiased;background-image:radial-gradient(100% 60% at 80% 0,#3b0a10,#09090A 70%)}
.w{max-width:520px;margin:0 auto;padding:28px 22px 44px;display:flex;flex-direction:column;gap:22px}.logo{font:800 22px 'Big Shoulders Display',Impact,sans-serif;letter-spacing:3px}
.cv{width:62%;max-width:280px;aspect-ratio:2/3;border-radius:10px;overflow:hidden;box-shadow:0 24px 60px rgba(0,0,0,.6);align-self:center}.cv svg{width:100%;height:100%;display:block}
.k{font:700 12px/1 'Hanken Grotesk',sans-serif;letter-spacing:2.2px;color:#F04A50}h1{font:800 clamp(40px,12vw,58px)/.95 'Big Shoulders Display',Impact,sans-serif;text-transform:uppercase;margin-top:10px}
.m{color:#A39E95;font-size:14px;margin-top:10px}.b{font:400 19px/1.55 'Newsreader',Georgia,serif;color:#d8d2c7}
.cta{display:block;text-align:center;background:#D2232C;color:#fff;text-decoration:none;font-weight:700;font-size:17px;padding:17px;border-radius:14px}.n{color:#A39E95;font-size:13px;text-align:center;line-height:1.5}</style></head>
<body><div class="w"><div class="logo">OPSIS</div><div class="cv">${covers[s.id]||''}</div>
<div><p class="k">${esc((s.series||s.kind).toUpperCase())}</p><h1>${esc(s.title)}</h1><p class="m">${esc(s.kind)}${s.min?' · '+s.min+' min de lecture':''}</p></div>
<p class="b">${esc(blurb)}</p><a class="cta" href="/#h=${encodeURIComponent(s.id)}">Lire cette histoire dans l'app</a>
<p class="n">OPSIS · The world is made of stories.<br>L'histoire complète se lit dans l'application.</p></div></body></html>`;
  let n=0;
  for(const s of list){
    const bl=(content.BLURB&&content.BLURB[s.id]&&content.BLURB[s.id].b)||s.sub||'Une histoire vraie à lire dans OPSIS.';
    const d=path.join(out,s.id);fs.mkdirSync(d,{recursive:true});
    fs.writeFileSync(path.join(d,'index.html'),tpl(s,bl));
    /* image d'aperçu : couverture à gauche, titre à droite */
    const tmp=path.join(out,'og','_t.html');fs.writeFileSync(tmp,`<style>${css.replace(/url\(\/fonts\//g,'url(../../fonts/')}*{margin:0;box-sizing:border-box}body{width:1200px;height:630px;background:radial-gradient(90% 100% at 85% 0,#4a0c12,#09090A 70%);color:#EDE6DA;display:flex;align-items:center;gap:56px;padding:0 90px;font-family:'Hanken Grotesk',sans-serif}.cv{flex:none;width:300px;height:450px;border-radius:12px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.6)}.cv svg{width:100%;height:100%;display:block}.k{font:700 20px 'Hanken Grotesk';letter-spacing:4px;color:#F04A50}h1{font:800 92px/.95 'Big Shoulders Display',Impact,sans-serif;text-transform:uppercase;margin-top:18px}.o{font:800 34px 'Big Shoulders Display',Impact,sans-serif;letter-spacing:5px;margin-top:34px;color:#A39E95}</style><div class="cv">${covers[s.id]||''}</div><div><p class="k">${esc((s.series||s.kind).toUpperCase())}</p><h1>${esc(s.title.length>60?s.title.slice(0,57)+'…':s.title)}</h1><p class="o">OPSIS</p></div>`);await p.goto('file://'+tmp);
    await p.evaluate(()=>document.fonts.ready);
    await p.screenshot({path:path.join(out,'og',s.id+'.jpg'),type:'jpeg',quality:82});n++;
  }
  fs.rmSync(path.join(out,'og','_t.html'),{force:true});
  console.log('pages de partage :',n);await b.close();
})();
